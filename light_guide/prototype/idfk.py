import json

fileObject = open("data.json", "r")
jsonContent = fileObject.read()
Zones = json.loads(jsonContent)

for i in range(len(Zones)):
    print(Zones[i]["LightStrip"], Zones[i]["Sensor"])
