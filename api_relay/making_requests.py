import requests
import json
import twilio.rest
#from twilio.rest import Client

def make_request_params(**kwargs):
    try:
        apiUrl = kwargs["apiUrl"]
    except:
        return ({"testing_apis function": "The main url for the API is missing"})

    try:
        apiEndpoint = kwargs["apiEndpoint"]
        # Add an endpoint to the api
        fullAPIUrl = apiUrl + apiEndpoint
    except:
        return ({"testing_apis": "The API endpoint for te API is missing"})

    try:
        params1 = kwargs["params"]
        result = requests.get(fullAPIUrl, params=params1)
    except:
        return ({"testing_api": "Missing API data"})


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