def split_by_char(someString, charForSplit):

    if someString != str(someString):
        status = "error"
        result = ""
        return status, result

    #Check if any part of string is not a number
    for x in str(someString):
        if x.isalpha():
            status = "error"
            result = ""
            return status, result
    
    if len(charForSplit) == 0:
        status = "error"
        result = ""
        return status, result
    
    #is chat for splitting is missing from the string
    if charForSplit not in someString:
        status = "error"
        result = ""
        return status, result

    
    
    status = "stringWasSplitted"
    result = someString.split(charForSplit)
    return status, result

def rounding_number(number):
    return (round(number * 2) / 2)