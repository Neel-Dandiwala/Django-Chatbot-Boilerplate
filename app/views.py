import os
from django.shortcuts import render
from twilio.twiml.messaging_response import Body, Message, MessagingResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import dialogflow
from google.api_core.exceptions import InvalidArgument


credential_path = "dialogflow_private_key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

DIALOGFLOW_PROJECT_ID = 'whatsappchatbot-ijju'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'
session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

def reply(actual_message):
    text_input = dialogflow.types.TextInput(text=actual_message, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        return response.query_result.fulfillment_text
    except InvalidArgument:
        raise

@csrf_exempt
def index(request):
    if request.method == 'POST':
        incoming_message = request.POST['Body'].lower()
        
        twilio_response = MessagingResponse()
        actual_message = twilio_response.message('')
        
        
        # if incoming_message == 'hello':
        #     response = "Welcome to the ChatBot experience"
        #     actual_message.body(str(response))   
        
        responseDF = reply(incoming_message)
        actual_message.body(str(responseDF))
        
        
        print(str(twilio_response))
        return HttpResponse(str(twilio_response))
        
        
