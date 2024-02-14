from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from .models import Lead
from .serializers import LeadSerializer
import requests
import uuid
import csv


@api_view(['POST'])
def create_lead_from_csv(request):
    file = request.FILES.get('file')
    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    # Validate file size and type
    if file.size > 10485760:  # 10 MB limit
        return Response({"error": "File size exceeds limit"}, status=413)
    if not file.name.endswith('.csv'):
        return Response({"error": "Invalid file format (must be CSV)"}, status=400)
    
    csv_parser = FileUploadParser()
    decoded_file = file.read().decode('utf-8').splitlines()
    csv_reader = csv.reader(decoded_file)
    leads_created = 0
    for row in csv_reader:
        if len(row) != 3:
            return Response({"error": "Invalid CSV format. Each row must have 3 columns."}, status=400)
        name, phone_number, vapi_call_id = row
        try:
            Lead.objects.create(
                name=name,
                phone_number=phone_number,
                vapi_call_id=vapi_call_id
            )
            leads_created += 1
        except IntegrityError as e:
            # Handle integrity errors if necessary
            print(f"Integrity error for row: {row}")
    
    return Response({"message": f"{leads_created} leads created successfully"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def create_lead(request):
    name = request.data.get('name')
    phone_number = request.data.get('phone_number')
    vapi_call_id = request.data.get('vapi_call_id')
    # status = request.data.get('status')
    print(phone_number)
    # if not phone_number or not vapi_call_id:
    #     return Response({"error": "Please provide phone_number and vapi_call_id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        lead = Lead.objects.create(
            name = name,
            phone_number=phone_number,
            # status=status,
            # vapi_call_id=vapi_call_id
        )
        print(lead)
        return Response({"message": "Lead created successfully"}, status=status.HTTP_201_CREATED)
    except IntegrityError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_lead_by_id(request, lead_id):
    lead = get_object_or_404(Lead, pk=lead_id)
    serializer = LeadSerializer(lead)
    return Response(serializer.data)

@api_view(['GET'])
def get_leads_list(request):
    leads = Lead.objects.all()
    serializer = LeadSerializer(leads, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def initiate_phone_call(request, lead_id):
    lead = get_object_or_404(Lead, pk=lead_id)
    phone_number = lead.phone_number
    callback_url = "http://127.0.0.1:8000/callback/{}".format(lead_id)
    url = "https://api.vapi.ai/call/phone"

    phone_number_id = str(uuid.uuid4())
    payload = {
        "customer": {
        "name": "name",
        "number": "+447456083068",
        },
        'assistantId': "7efc3637-4cb0-4e05-b109-9d0b3c689f82",
        "maxDurationSeconds": 10,
        "assistant": {
        "serverUrl" : "http://127.0.0.1:8000/leads/callback",
        },
        # "metadata": {},
        # "phoneNumber": {
        #     "assistantId": "<string>",
        #     "name": "<string>",
        #     "twilioAccountSid": "<string>",
        #     "twilioAuthToken": "<string>",
        #     "twilioPhoneNumber": "<string>"
        # },
        "phoneNumberId": "805d4ff2-3b02-44c5-a722-534005571453",
    }

    
    headers = {
        "Authorization": "Bearer c1422ff5-c691-41d7-8d05-1e59d3cec79f",
        "Content-Type": "application/json"
    }

        # Make POST request to Vapi endpoint
        # Replace <YOUR_API_KEY> with your actual Vapi API key
    try:
        response = requests.request("POST", url, json=payload, headers=headers)
        # response = requests.post('https://api.vapi.ai/call/phone', json=payload, headers={'Authorization': 'Bearer c1422ff5-c691-41d7-8d05-1e59d3cec79f'})
        if response.status_code == 201:
            print(response.text)  
            return Response({'message': 'Phone call initiated successfully'})
        else:
            print(f"Error: {response.status_code}")
            print(response.text)  # Print the response content for further investigation
            return Response({'error': 'Failed to initiate phone call'}, status=response.status_code)
    except IntegrityError as e:
        return Response({'error': str(e)})

@api_view(['GET'])
def callback(request, lead_id):
    print("Call completed")
    lead = get_object_or_404(Lead, pk=lead_id)
    lead.status = 'Call completed'
    lead.save()
    return Response({'message': 'Lead status updated successfully'})
