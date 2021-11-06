#!/usr/bin/env python
"""
Fetch planet information from nasa.org and store it in a json file.
"""
import numpy as np
import json
import requests
from astropy.time import Time
from astroquery.jplhorizons import Horizons

url = "https://api.le-systeme-solaire.net/rest/bodies?order=perihelion,asc"

r = requests.get(url).json()

# simulating a solar system starting from this date
sim_start_date = "2022-01-01"

data = {}

names = ["Mercure", "Vénus", "La Terre", "Mars",
         "Jupiter", "Saturne", "Uranus", "Neptune"]

planets = []

for object in r["bodies"]:
    if object["isPlanet"] == True and object["name"] in names:
        planets.append(object)

for i, planet in enumerate(planets):
    obj = Horizons(id=i, location="@sun",
                   epochs=Time(sim_start_date).jd, id_type="id").vectors()
    data[planet["id"]] = {
        "name": planet["name"],
        "mass": round(planet["mass"]["massValue"]),
        "pos": [np.double(obj[xi]) * 10 if abs(np.double(obj[xi])) > 1 else np.double(obj[xi]) * 100 for xi in ['x', 'y']],
        "v": [np.double(obj[vxi]) * 100 for vxi in ['vx', 'vy']],
    }

with open("planets.json", 'w') as f:
    json.dump(data, f, indent=4)