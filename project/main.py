import json
import turtle
import urllib.request
import time
import webbrowser
import geocoder 

url = "http://api.open-notify.org/astros.json"
response = urllib.request.urlopen(url)
result = json.loads(response.read())
file = open("iss.txt", "w")
file.write("There are currently " +
             str(result["number"]) + " astronauts on the international space station: \n\n")
people = result["people"]
for p in people:
    file.write(p['name'] + " - on board" + "\n")

# print long and Lat

g = geocoder.ip('me')
file.write("\n your current lat / lat is: " + str(g.lating))
file.close()
webbrowser.open("iss.txt")
