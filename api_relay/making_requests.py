import requests
import json
import twilio.rest
# import the logging library
import logging

def make_request(**kwargs):
    info_logger = "info_logger"
    error_logger = "error_logger"
    try:
        sourceOfCall = kwargs["sourceOfCall"]
        if sourceOfCall == "darksky":
            info_logger = "darksky_info_logger"
            error_logger = "darksky_error_logger"
        elif sourceOfCall == "rechaptcha":
            info_logger = "rechaptcha_info_logger"
            error_logger = "rechaptcha_error_logger"
        elif sourceOfCall == "locationiq":
            info_logger = "locationiq_info_logger"
            error_logger = "locationiq_error_logger"
    except:
        logging.getLogger("error_logger").error("make_request made without source of call: %s", kwargs)




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
            logging.getLogger(info_logger).info("Api request: %s", str(fullAPIUrl))
            result = requests.get(fullAPIUrl, params=params1)
            logging.getLogger(info_logger).info("Api response: %s", result.json())
        except:
            logging.getLogger(error_logger).error("Not succesfull params get api response: %s", result.json())
            return "error"

    elif paramsData == "data" and getPost == "post":
        try:
            data1 = kwargs["data"]
            #data1 = kwargs.get('data')
            result = requests.post(fullAPIUrl, data=data1)
            logging.getLogger(info_logger).info("Successful data post api response: %s", result.json())
        except:
            logging.getLogger(error_logger).error("Not succesfull data post api response: %s", result.json())
            return "error"

    if result.status_code in (400, 401, 402, 403, 404):
        logging.getLogger("error_logger").error("40x Api response is: %s", result.json())
        return result

    return result.json()

#depreciated due to make_request fun
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

    #test log
    logging.getLogger("error_logger").error("test api responce logger: %s", result.json())
    return result.json()

def twilio_api(userMobileNumber, processedForecastMessage, twilioAccountSid, twilioAuthToken, myTwilioTelephone):
    try:
        client1 = twilio.rest.Client(twilioAccountSid, twilioAuthToken)

        message1 = client1.messages \
                        .create(
                            body=processedForecastMessage,
                            from_= myTwilioTelephone,
                            to=userMobileNumber
                        )
    except:
        logging.getLogger("error_logger").error("Twilio message response logger: %s", message1)

    #print(message1.status)
    #print(message1)