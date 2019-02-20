# -*-coding: utf-8 -*-
import json

model = {}
with open("/TIVOLI/flask_ICBC/frontend/src/components/testdata/diamond.json",'r') as f:
    a = json.loads(f)
    for x in a:
        name = x['name']


print("sdsa")
print(model)