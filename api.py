#!/usr/bin/env python
"""
Fetch planet information from nasa.org and store it in a json file.
"""
import numpy as np
import json
from astropy.time import Time
# from astroquery.jplhorizons import Horizons

# from astroquery import open_exoplanet_catalogue as oec
# from astroquery.open_exoplanet_catalogue import findvalue
import xml.etree.ElementTree as ET
import urllib.request
import gzip
import io

# simulating a solar system starting from this date
sim_start_date = "2022-01-01"

data = dict(info="Database for queried planets, with position, velocity, moons, etc.",
            startDate=sim_start_date)

url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"

oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(
    urllib.request.urlopen(url).read())))

# Output mass and radius of all planets
for planet in oec.findall(".//planet[name='Earth']/*"):
    print("\t" + planet.tag + ":", planet.text)

# catalog = oec.get_catalogue()

# for planet in catalog.findall(".//planet[name='Earth']/*"):
#     print("\t" + planet.tag + ":", planet.text)

# names = ['Mercury', 'Venus', 'Earth', 'Mars']
# sizes = [0.38, 0.95, 1., 0.53]
# nasaids = [1, 2, 3, 4]   # The 1st, 2nd, 3rd (399 and 301), 4th planet in solar system

# data = dict(info="Solar planets database, including positions and velocities at the given date",
#             date=sim_start_date)
# for i in range(len(nasaids)):
#     nasaid = nasaids[i]
#     obj = Horizons(id=nasaid, location="@sun", epochs=Time(sim_start_date).jd, id_type='id').vectors()
#     data[str(nasaid)] = {
#         "name": names[i],
#         "size": sizes[i],
#         "r": [np.double(obj[xi]) for xi in ['x', 'y', 'z']],
#         "v": [np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']]
#     }

with open("planets.json", 'w') as f:
    json.dump(data, f, indent=4)
