file = 'obce_obyvatelia'

import ftfy
def format(s): return ftfy.ftfy(s) if type(s) == str else s
def format_obj(obj: object):
    keys = obj.keys()
    formatted_obj = {}
    for key in keys:
        formatted_obj[key] = format(obj[key])
    
    return formatted_obj

def format_arr_objects(arr): return [format_obj(o) for o in arr]

import json
with open('{}.json'.format(file), 'r') as f:
    _list = json.load(f)
    new_list = []
    for val in _list:
        new_list.append(format_obj(val))

    print(new_list)
    with open('{}_fixed.json'.format(file), 'w') as file_out:
        json.dump(new_list, file_out, ensure_ascii=False)
