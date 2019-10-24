def without_accent(string):
    result = ""
    for i in range(0,len(string)):
        if string[i] in ["é","è","ê"]:
            letter = "e"
        elif string[i] in ["à", "â"]:
            letter = "a"
        else:
            letter = string[i]
        result += letter
    return result
