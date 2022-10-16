import json

with open('./courses.json', 'r') as file:
    data = json.load(file)

print(data)