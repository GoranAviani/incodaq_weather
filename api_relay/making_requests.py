import requests
import json
import twilio.rest
#from twilio.rest import Client

def make_request_params(**kwargs):
    try:
        apiUrl = kwargs["apiUrl"]
    except:
        return "error"

    try:
        apiEndpoint = kwargs["apiEndpoint"]
        # Add an endpoint to the api
        fullAPIUrl = apiUrl + apiEndpoint
    except:
        return "error" 

    try:
        params1 = kwargs["params"]
        result = requests.get(fullAPIUrl, params=params1)
    except:
        return "error"


    if result.status_code in (400, 401, 402, 403, 404):
        return result

    return result.json()

def twilio_api(userMobileNumber, processedForecastMessage, twilioAccountSid, twilioAuthToken, myTwilioTelephone):
    
    client1 = twilio.rest.Client(twilioAccountSid, twilioAuthToken)

    message1 = client1.messages \
                    .create(
                        body=processedForecastMessage,
                        from_= myTwilioTelephone,
                        to=userMobileNumber
                    )
    #print(message1.status)