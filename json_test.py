import json


def is_valid_json(json_str):
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False


def check(json_str):
    if is_valid_json(json_str):
        json_obj = json.loads(json_str)
        return (json_obj['action'], json_obj['list'], json_obj['target'])   
    
    else:
        return tuple()
    

def check_01packbag(json_str):
    if is_valid_json(json_str):
        json_obj = json.loads(json_str)
        return (json_obj['action'], json_obj['lv'], json_obj['lw'], json_obj['target'])   
    else:
        return tuple()






