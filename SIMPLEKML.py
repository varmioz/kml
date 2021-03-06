
import math, random
import simplekml
import csv
from webcolors import name_to_hex as nth

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

def simpkml():
# Read the file
    with open("Points.csv", 'rb') as f:
        data=[tuple(line) for line in csv.reader(f)]
        data.remove(data[0])
    # Create an instance of Kml
    kml = simplekml.Kml(open = 1)
    fol = kml.newfolder(name = 'Points from CSV')
    # Create a points
    for cell,lon,lat in data:
        pnt = fol.newpoint(name = cell, description = ("Object - " + cell), coords = [(lon,lat)])
    # Save the KML
    kml.save("Points.kml")
    print str(len(data)), 'points created'

def siteskml():
#create sites under subfolders

    file = "Sites.csv"
    with open(file, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]

    # Create an instance of Kml
    kml = simplekml.Kml(open=1)

    # Create a point for each city. The points' properties are assigned after the point is created
    fold = None
    subfold = None
    for row in data:   
    
        if fold <> row['Folder']:
            fold = row['Folder']
            fol = kml.newfolder(name = fold)
            subfold = row['Subfolder']
            fol1 = fol.newfolder(name=subfold)
            if row['Color'] == 'random': color = "ff%06x" % random.randint(0, 0xFFFFFF)
            else: color = 'ff'+nth(row['Color'])[1:]
        
        if subfold <> row['Subfolder']:
            subfold = row['Subfolder']
            fol1 = fol.newfolder(name=subfold)
            if row['Color'] == 'random': color = "ff%06x" % random.randint(0, 0xFFFFFF)
            else: color = 'ff'+nth(row['Color'])[1:]      

        pnt = fol1.newpoint(name = row['Site'])
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/donut.png'
        pnt.style.iconstyle.scale = 0.8
        pnt.style.iconstyle.color = color
        pnt.style.labelstyle.scale = 0.5
        pnt.style.labelstyle.color = color
        pnt.description = "Date - " + row['Comment']
        pnt.coords = [(row['Lon'], row['Lat'])]


    # Save the KML
    print 'Saving', len(data), 'in file...'
    kml.save("Sites.kml")

def polygon():
#polygon
    pol = kml.newpolygon(name="Atrium Garden",
             outerboundaryis=[(18.43348,-33.98985),(18.43387,-33.99004),(18.43410,-33.98972),
                              (18.43371,-33.98952),(18.43348,-33.98985)],
             innerboundaryis=[(18.43360,-33.98982),(18.43386,-33.98995),(18.43401,-33.98974),
                              (18.43376,-33.98962),(18.43360,-33.98982)])
    pol.style.linestyle.color = simplekml.Color.red
    pol.style.linestyle.width = 5
    pol.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.green)
    #LineString
    ls = kml.newlinestring(name='A LineString')
    ls.coords = [(18.333868,-34.038274,10.0), (18.370618,-34.034421,10.0)]
    ls.altitudemode = simplekml.AltitudeMode.relativetoground
    ls.visibility = 0
    ls.description = "Short description"

# -== Beginning ==-#
print '''
    What do you want:
    1. Simple convertion from file data.cvs to Points.kml
       header "Cell,Longitude,latitude"
    2. Convertion to folders from sites.csv to Sites.kml
       header "Folder,Subfolder,Site,Lon,Lat,Comment,Color"
    3. tbd
    '''
choice = 0
try: choice = int(raw_input ("Your option:"))
except ValueError: print "WTF, it's not a number!!!"
if choice == 1: simpkml()
elif choice == 2: siteskml()
else: print "Type right option"


"""
Cell,Lon,Lat,ANT_DIRECTION,ANT_BEAM_WIDTH,UARFCN,SC,RNC-ID,C-ID,LAC
"""
