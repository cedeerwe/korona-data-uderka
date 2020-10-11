file = 'middle_schools_with_students'

def format(s): return s.format("utf-8")
def format_obj(obj): return {
    'name': format(obj['name']),
    'students': obj['students']
}
def format_arr_objects(arr): return [format_obj(o) for o in arr]

import json
with open('{}.json'.format(file), 'r') as f:
    _dict = json.load(f)
    new_dict = {}
    for key, val in _dict.items():
        new_dict[format(key)] = format_arr_objects(val)

    print(new_dict)
    with open('{}_fixed.json'.format(file), 'w') as file_out:
        json.dump(new_dict, file_out, ensure_ascii=False)
