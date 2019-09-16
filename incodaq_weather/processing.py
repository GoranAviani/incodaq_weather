def split_by_char(someString, charForSplit):
    
    try:
        isString = isinstance(someString, str)
    except:
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
