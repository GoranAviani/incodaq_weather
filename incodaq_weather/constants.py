GREEN_STRING = "green"
RED_STRING = "red"
YELLOW_STRING = "yellow"

CITY_COUNTRY_NEGATIVE_STATUS = "City and Country are required fields for weather forecast"
ADDRESS_NEGATIVE_STATUS = "Address is required to receive a more precise forecast"
MOBILE_NUMBER_NEGATIVE_STATUS = "Your account has no mobile number"
FORECAST_TIME_NEGATIVE_STATUS = "Forecast time is not set"
MOBILE_NUMBER_VALIDATED_NEGATIVE_STATUS = "Your mobile phone is not validated"
SMS_MESSAGE_NEGATIVE_STATUS = "To receive messages select that inside your mobile configuration"

CITY_COUNTRY_POSITIVE_STATUS = "City and Country are inputed"
ADDRESS_POSITIVE_STATUS = "Address is inputed"
MOBILE_NUMBER_POSITIVE_STATUS = "You have inputed a mobile number"
FORECAST_TIME_POSITIVE_STATUS = "Forecast time is set"
MOBILE_NUMBER_POSITIVE_NEGATIVE_STATUS = "your mobile phone has been validated"
SMS_MESSAGE_POSITIVE_STATUS = "You have selected to receive forecast text messages"


API_URLS = {'darksky_forecast': "https://api.darksky.net/forecast/{}/{},{}",
            'locationiq_v1':"https://eu1.locationiq.com/v1/search.php",
            'google_recaptcha': "https://www.google.com/recaptcha/api/siteverify"}