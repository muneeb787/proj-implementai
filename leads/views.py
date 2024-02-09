from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Lead
from .serializers import LeadSerializer
from vapi_python import Vapi

@api_view(['POST'])
def create_lead(request):
    phone_number = request.data.get('phone_number')
    vapi_call_id = request.data.get('vapi_call_id')
    # status = request.data.get('status')
    print(phone_number)
    # if not phone_number or not vapi_call_id:
    #     return Response({"error": "Please provide phone_number and vapi_call_id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        lead = Lead.objects.create(
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
    payload = {
        "phoneNumberId": "+447456083068",
        'serverUrl': callback_url
    }
    # Make POST request to Vapi endpoint
    # Replace <YOUR_API_KEY> with your actual Vapi API key
    try:
        vapi = create_web_call(api_key='c1422ff5-c691-41d7-8d05-1e59d3cec79f')
        assistant = {
        'firstMessage': 'Hey, how are you?',
        'context': 'You are an employee at a drive thru...',
        'model': 'gpt-3.5-turbo',
        'voice': 'jennifer-playht',
        "recordingEnabled": True,
        "interruptionsEnabled": False
        }

        vapi.start(assistant=assistant)
        # response = requests.post('https://api.vapi.ai/call/phone', json=payload, headers={'Authorization': 'Bearer c1422ff5-c691-41d7-8d05-1e59d3cec79f'})
        # if response.status_code == 200:
        #     return Response({'message': 'Phone call initiated successfully'})
        # else:
        #     print(f"Error: {response.status_code}")
        #     print(response.text)  # Print the response content for further investigation
        #     return Response({'error': 'Failed to initiate phone call'}, status=response.status_code)
    except IntegrityError as e:
        return Response({'error': str(e)})

@api_view(['GET'])
def callback(request, lead_id):
    lead = get_object_or_404(Lead, pk=lead_id)
    lead.status = 'Call completed'
    lead.save()
    return Response({'message': 'Lead status updated successfully'})
