import json

with open('json_schemas.json','r') as file:
    data = json.load(file)

print(data['comment'])