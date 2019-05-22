import math
import arcpy
from math import pi
from math import tan
from math import sqrt
import os
from arcpy import env
env.overwriteOutput = True

def writeTheFile(arrayForPoly):

    # Set local variables
    outPath = "C:\\Users\\Daniel\\Desktop\\Work\\Work\\IndexingProject\\OutData\\"
    outName = "IndexShapefile.shsp"
    outFile = outPath + outName
    geometry_type = "POLYGON"
    template = "C:\\Users\\Daniel\\Desktop\\Work\\Work\\IndexingProject\\OutData\\template.shp"
    has_m = "DISABLED"
    has_z = "DISABLED"

    # Use Describe to get a SpatialReference object
    spatial_reference = arcpy.Describe("C:\\Users\\Daniel\\Desktop\\Work\\Work\\IndexingProject\\OutData\\template.shp").spatialReference

    # Execute CreateFeatureclass
    arcpy.CreateFeatureclass_management(outPath, outName, geometry_type, template, has_m, has_z, spatial_reference)
    addPolyCursor = arcpy.da.InsertCursor(outFile, ['SHAPE@', 'photoID'])
    polygon = arcpy.Polygon(arrayForPoly)
    addPolyCursor.insertRow([polygon, '297'])
    del addPolyCursor

def GetPoint(currentHeading, X, Y, WidthOrHeight, Distance):
    print currentHeading
    if currentHeading < 90.0:
        Quadrant = 1
        RelativeHeading = 90.0 - currentHeading
    elif currentHeading < 180.0:
        Quadrant = 2
        RelativeHeading = 180.0 - currentHeading
    elif currentHeading < 270.0:
        Quadrant = 3
        RelativeHeading = 270.0 - currentHeading
    elif currentHeading < 360.0:
        Quadrant = 4
        RelativeHeading = 360.0 - currentHeading
    # print str(X) + "," + str(Y) + ", " + str(currentHeading)

    calculatedDistance = 0.0
    Opposite = 1.0
    RadHeading = RelativeHeading * pi / 180.0
    while calculatedDistance < Distance:
        #print "Opposite: " + str(Opposite)
        Adjacent = Opposite / tan(RadHeading)
        #print "Quadrant: " + str(Quadrant)
        if Quadrant == 1:
            newX = Adjacent
            newY = Opposite
        elif Quadrant == 2:
            newX = Opposite
            newY = Adjacent * -1.0
        elif Quadrant == 3:
            newX = Adjacent * -1.0
            newY = Opposite * -1.0
        elif Quadrant == 4:
            newX = Opposite * -1.0
            newY = Adjacent
        #print str(newX) + " :: " + str(newY)
        calculatedDistance = math.sqrt((newX * newX) + (newY * newY))
        #print "Calculated Distance: " + str(calculatedDistance)
        Opposite += 1.0
    
    # print calculatedDistance    
    return [newX + X, newY + Y]

#Jesus: please read the XY and heading (yaw) and from a file.  It has to be projected coordinates, as from Drone2Map, not what I recall the
# Photoscan output - latitude and longitude (6370990 vs 33.20200).
X = 640297.412572  
Y = 3822531.071888
Heading = 90.225403
Width = 40.0/2.0
Height = 30.0/2.0

if Heading < 0.0:
    ModHeading = 360.0 + Heading
else:
    ModHeading = Heading#ModHeading = Heading
print ModHeading
theValue = GetPoint(ModHeading, X, Y, 0, 50)

# make an array to store each polygon in
arrayForPoly = arcpy.Array()

f = open("C:\\users\\daniel\\Desktop\\work\\work\\IndexingProject\\data\\data.csv","w")
f.write("x,y,z\n")
theValue = GetPoint(ModHeading, X, Y, 0, Height)
f.write(str(theValue[0]) + ", " + str(theValue[1]) + ",10\n")

forwardX = theValue[0]
forwardY = theValue[1]
print str(theValue[0]) + " :: " + str(theValue[1])

forwardRightHeading = ModHeading + 90
if forwardRightHeading > 360.0:
    forwardRightHeading = forwardRightHeadin - 360.0
theValue = GetPoint(forwardRightHeading, forwardX, forwardY, 0, Width)
print str(theValue[0]) + " :: " + str(theValue[1])
f.write(str(theValue[0]) + ", " + str(theValue[1]) + ",1\n")
arrayForPoly.add(arcpy.Point(theValue[0], theValue[1])) # first coordinate
startX = theValue[0]
startY = theValue[1]


forwardLeftHeading = ModHeading - 90
if forwardLeftHeading > 360.0:
    forwardLeftHeading = forwardLeftHeadin - 360.0
theValue = GetPoint(forwardLeftHeading, forwardX, forwardY, 0, Width)
print str(theValue[0]) + " :: " + str(theValue[1])
f.write(str(theValue[0]) + ", " + str(theValue[1]) + ",2\n")
arrayForPoly.add(arcpy.Point(theValue[0], theValue[1])) # second coordinate

if ModHeading > 180.0:
    OppositeHeading = ModHeading - 180
else:
    OppositeHeading = ModHeading + 180
theValue = GetPoint(OppositeHeading, X, Y, 0, Height)
print str(theValue[0]) + " :: " + str(theValue[1])
f.write(str(theValue[0]) + ", " + str(theValue[1]) + ",-10\n")
backwardX = theValue[0]
backwardY = theValue[1]

backwardRightHeading = OppositeHeading + 90
if backwardRightHeading > 360.0:
    backwardRightHeading = backwardRightHeading - 360.0
theValue = GetPoint(backwardRightHeading, backwardX, backwardY, 0, Width)
print str(theValue[0]) + " :: " + str(theValue[1])
f.write(str(theValue[0]) + ", " + str(theValue[1]) + ",3\n")
arrayForPoly.add(arcpy.Point(theValue[0], theValue[1])) # third coordinate

backwardLeftHeading = OppositeHeading - 90
if backwardLeftHeading > 360.0:
    backwardLeftHeading = backwardLeftHeading - 360.0
theValue = GetPoint(backwardLeftHeading, backwardX, backwardY, 0, Width)
print str(theValue[0]) + " :: " + str(theValue[1])
f.write(str(theValue[0]) + ", " + str(theValue[1]) + ",4\n")
arrayForPoly.add(arcpy.Point(theValue[0], theValue[1])) # fourth coordinate
arrayForPoly.add(arcpy.Point(startX, startY)) # back to first coordinate

f.close()

writeTheFile(arrayForPoly)

