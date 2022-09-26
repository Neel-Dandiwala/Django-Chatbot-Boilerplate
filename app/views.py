from django.shortcuts import render
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def index(request):
    if request.method == 'POST':
        incoming_message = request.POST['Body'].lower()
        
        twilio_response = MessagingResponse()
        actual_message = twilio_response.message()
        
        if incoming_message == 'Hello':
            response = "Hey How are you"
            actual_message.body(response)
            
        return HttpResponse(str(twilio_response))
        
