import json

with open('date_and_time_table.json','r') as json_file:
    data = json.load(json_file)
    print(data)