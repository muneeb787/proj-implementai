from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'name' ,'phone_number' , 'vapi_call_id', 'status', 'created_on' ,]
