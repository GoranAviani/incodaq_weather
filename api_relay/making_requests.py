import requests
import json
import twilio.rest
# import the logging library
import logging

def make_request(**kwargs):
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
        paramsData = kwargs["paramsData"]
        getPost = kwargs["getPost"]
    except:
        return "error"

    if paramsData == "params" and getPost == "get":
        try:
            params1 = kwargs["params"]
            result = requests.get(fullAPIUrl, params=params1)
            logging.getLogger("darksky_info_logger").info("Dark Sky successful response: %s", result.json())
        except:
            logging.getLogger("error_logger").error("Api response is: %s", result.json())
            return "error"

    elif paramsData == "data" and getPost == "post":
        try:
            data1 = kwargs["data"]
            #data1 = kwargs.get('data')
            result = requests.post(fullAPIUrl, data=data1)
            #TODO recaptcja logger
            logging.getLogger("darksky_info_logger").info("recaptcha successful response: %s", result.json())
        except:
            logging.getLogger("error_logger").error("Recaptcha api response is: %s", result.json())
            return "error"

    if result.status_code in (400, 401, 402, 403, 404):
        logging.getLogger("error_logger").error("40x Api response is: %s", result.json())
        return result

    return result.json()

#TODO depreciated due to make_requests
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
        logging.getLogger("darksky_info_logger").info("Dark Sky successful response: %s", result.json())
    except:
        logging.getLogger("error_logger").error("Api response is: %s", result.json())
        return "error"


    if result.status_code in (400, 401, 402, 403, 404):
        logging.getLogger("error_logger").error("40x Api response is: %s", result.json())
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
    #print(message1)