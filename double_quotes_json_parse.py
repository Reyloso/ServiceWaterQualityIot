import json
def double_quotes_parse(data):
    good_characters = [":","{","}",","]
    result = ""
    for key, value in enumerate(data):

        if ((value == "\"" and data[key-1] not in good_characters) and (value == "\"" and data[key+1] not in good_characters) or (value == "\"" and data[key-1] == "," and data[key-2] != "\"")):
            result += '\''   
        else:
            result += value        
    #print(result)
    json_string = "{0}".format(result)
    data_list = json.loads(json_string)
    print("data list", data_list)
    return data_list
