
import math
import simplekml
import csv

R = 6378.1 #Radius of the Earth in km

def coord_calc (lat1, lon1, degree, d):
    # coordinates lon2,lat2 base on angle and distance from point lon1,lat1
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    brng = math.radians(degree)

    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
             math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    return [lat2,lon2]


def dist_calc(lat2,lon2,lat1,lon1):
    #calculation distance
    dlon = math.radians(lon2) - math.radians(lon1) 
    dlat = math.radians(lat2) - math.radians(lat1)
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    km = R * (2 * math.asin(math.sqrt(a)))
    return km

file = "Cell.csv"
with open(file, 'rb') as f:
    data=[tuple(line) for line in csv.reader(f)]
    data.remove(data[0])

# Create an instance of Kml
kml = simplekml.Kml(open=1)

# Create a point for each city. The points' properties are assigned after the point is created
for cell,lon,lat,direction,beam,UARFCN,SC,RNC,cellid,LAC in data:
    pnt = kml.newpoint()
    pnt.name = cell
    pnt.description = "RNC - " + RNC + "LAC - " + LAC
    pnt.coords = [(lon, lat)]
    pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pal2/icon26.png'

# Save the KML
print len(data)
kml.save("T00 Point.kml")


"""
Cell,Lon,Lat,ANT_DIRECTION,ANT_BEAM_WIDTH,UARFCN,SC,RNC-ID,C-ID,LAC
"""




