import math
from math import pi
from math import tan
from math import sqrt
import os

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
    
    print 'Calc distance:' + str(calculatedDistance)   
    return [newX + X, newY + Y]

#Jesus: please read the XY and heading (yaw) and from a file.  It has to be projected coordinates, as from Drone2Map, not what I recall the
# Photoscan output - latitude and longitude (6370990 vs 33.20200).
X = 640243.351  
Y = 3822558.249
# Handle possible zero case
Heading = 0.1
Width = 114.0/2.0
Height = 86.0/2.0

if Heading < 0.0:
    ModHeading = 360.0 + Heading
else:
    ModHeading = Heading
    
print ModHeading

#theValue = GetPoint(ModHeading, X, Y, 0, 50)


f = open("E:\\UserFiles\\jesusg\\data.csv","w")
f.write("x,y,point_id\n")
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

forwardLeftHeading = ModHeading - 90
if forwardLeftHeading > 360.0:
    forwardLeftHeading = forwardLeftHeadin - 360.0

print 'third get_point'
theValue = GetPoint(forwardLeftHeading, forwardX, forwardY, 0, Width)
print str(theValue[0]) + " :: " + str(theValue[1])
f.write(str(theValue[0]) + ", " + str(theValue[1]) + ",2\n")

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

backwardLeftHeading = OppositeHeading - 90
if backwardLeftHeading > 360.0:
    backwardLeftHeading = backwardLeftHeading - 360.0
theValue = GetPoint(backwardLeftHeading, backwardX, backwardY, 0, Width)
print str(theValue[0]) + " :: " + str(theValue[1])
f.write(str(theValue[0]) + ", " + str(theValue[1]) + ",4\n")

f.close()


