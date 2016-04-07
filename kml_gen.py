# using tuples from csv file in order "Cell,Lon,Lat"
import simplekml
import csv

# Read the file
with open("data.csv", 'rb') as f:
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