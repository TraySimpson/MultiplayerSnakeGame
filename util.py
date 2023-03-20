def get_tuple_from_string(data):
    if (data == "None"):
        return None
    return tuple(map(int, data.replace("(","").replace(")","").split(', ')))