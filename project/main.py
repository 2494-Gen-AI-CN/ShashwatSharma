
import json
import turtle
import urllib.request
import webbrowser
import geocoder
from pathlib import Path
from datetime import datetime

# Get the folder where this file is saved
folder = Path(__file__).resolve().parent

# Get astronaut information
def get_astronauts():
    url = "https://corquaid.github.io/international-space-station-APIs/JSON/people-in-space.json"

    try:
        response = urllib.request.urlopen(url, timeout=10)
        data = json.loads(response.read())
        response.close()

        file = open(folder / "iss.txt", "w")

        # Keep only the astronauts on the ISS ("iss" is True for ISS crew)
        iss_crew = []
        for person in data["people"]:
            if person["iss"]:
                iss_crew.append(person)

        file.write("There are currently " + str(len(iss_crew)) +
                   " astronauts on the ISS:\n\n")

        for person in iss_crew:
            line = person["name"] + " (" + person["country"] + ")"

            # Mark the Canadian astronaut
            if person["country"] == "Canada":
                line = line + "  <-- Canadian"

            file.write(line + "\n")

        # Get approximate location
        g = geocoder.ip("me")
        file.write("\nYour latitude and longitude: " + str(g.latlng))

        file.close()

        webbrowser.open((folder / "iss.txt").as_uri())
        print("Astronaut information saved")

        return iss_crew

    except Exception as e:
        print("Error getting astronaut information:", e)
        return []


# Create the world map
screen = turtle.Screen()

screen.setup(width=1280, height=720)
screen.screensize(1280, 720)

screen.title("ISS Live Tracker")
screen.setworldcoordinates(-180, -90, 180, 90)

screen.bgpic(str(folder / "images" / "map.gif"))

# Add the ISS image
iss_image = str(folder / "images" / "iss.gif")
screen.register_shape(iss_image)

iss = turtle.Turtle()
iss.shape(iss_image)
iss.penup()

# Invisible turtle that writes the "ISS" label next to the icon
label = turtle.Turtle()
label.hideturtle()
label.penup()
label.color("yellow")

# Invisible turtle that writes the info box in the bottom-left corner
info = turtle.Turtle()
info.hideturtle()
info.penup()
info.color("white")
info.goto(-175, -85)


# Get ISS location from API
def get_iss_location():
    url = "https://api.wheretheiss.at/v1/satellites/25544"

    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.load(response)

    return data


# Update ISS location on the map
def update_iss():
    try:
        data = get_iss_location()

        lat = float(data["latitude"])
        lon = float(data["longitude"])
        altitude = data["altitude"]
        speed = data["velocity"]

        # Move the ISS icon
        iss.goto(lon, lat)

        # Move the "ISS" label so it stays next to the icon
        label.clear()
        label.goto(lon + 6, lat - 3)
        label.write("ISS", font=("Arial", 14, "bold"))

        current_time = datetime.fromtimestamp(data["timestamp"])

        # Build the info text: station, live location, then the crew
        text = "International Space Station (ISS)\n"
        text = text + "Latitude: " + str(round(lat, 2)) + "\n"
        text = text + "Longitude: " + str(round(lon, 2)) + "\n"
        text = text + "Altitude: " + str(round(altitude, 2)) + " km\n"
        text = text + "Speed: " + str(round(speed, 2)) + " km/h\n"
        text = text + "Time: " + str(current_time) + "\n\n"
        text = text + "Crew on board (" + str(len(crew)) + "):\n"

        for person in crew:
            text = text + "  " + person["name"] + " (" + person["country"] + ")\n"

        # Redraw the info box on the map
        info.clear()
        info.write(text, font=("Arial", 12, "normal"))

        # Show the same info in the terminal
        print("\n" + text)

    except Exception as e:
        print("Error getting ISS location:", e)

    # Update every 5 seconds
    screen.ontimer(update_iss, 5000)


# Run the project
crew = get_astronauts()
update_iss()
screen.mainloop()
