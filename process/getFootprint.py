import math
from math import pi
from math import tan
from math import sqrt
import os

def GetPoint(currentHeading, X, Y, WidthOrHeight, Distance):
    
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

    print('Current heading:', str(currentHeading) + ',', 'Quadrant:', Quadrant)
    print('Relative heading:', RelativeHeading, end='\n\n') 
    calculatedDistance = 0.0
    Opposite = 1.0
    RadHeading = RelativeHeading * pi / 180.0

    # Incrementally, the hypotenuse (distance) is found by moving along the
    # opposite side one step at a time. Increasing the opposite slowly helps
    # find an adjacent side length, which then allows the use of tan to find
    # the hypotenuse, or current distance away from origin.
    while calculatedDistance < Distance:
        print('Opposite: ' + str(Opposite))
	# New adjacent is calculated given new opposite position
        Adjacent = Opposite / tan(RadHeading)

	# These conditionals ensure that the signs of X/Y coordinates are
        # correct depending on the quadrant specified by the yaw (heading)
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
        print('X:', str(newX), ' :: ', 'Y:', str(newY))
        calculatedDistance = math.sqrt((newX * newX) + (newY * newY))
        print('Calculated Distance: ' + str(calculatedDistance))
        Opposite += 1.0
    
    print('\nFinal distance: ', calculatedDistance, end='\n\n')
    return [newX + X, newY + Y]

# Jesus: please read the XY and heading (yaw) and from a file.  It has to be
# projected coordinates, as from Drone2Map, not what I recall the Photoscan
# output - latitude and longitude (6370990 vs 33.20200).
X = 639707.969  
Y = 3823600.569
Heading = -94.3
if Heading < 0.0:
    ModHeading = 360.0 + Heading
else:
    ModHeading = Heading
#ModHeading = Heading

theValue = GetPoint(ModHeading, X, Y, 0, 50)

#This code finds the point along the heading of the drone (the direction the drone was facing) and then the point in the opposite
#direction.  You need to go 90 degrees in both directions in order to find the corners as we discussed.  I may not see you the
#rest of today but we will work on this tomorrow.
cur_dir = os.path.dirname(os.path.realpath(__file__))
rel_loc = 'footprint-output/data-output.csv'
full_path = os.path.join(cur_dir, rel_loc)

#f = open("home\\jesusg\\edoc\\MIT-GIS-DataLab\\process\\data-output.csv","w")
f = open(full_path, 'w')
f.write("x,y\n")
f.write(str(theValue[0]) + ", " + str(theValue[1]) + "\n")
#distance along heading
f.write(str(X) + ", " + str(Y) + "\n")
OppositeHeading = 180.0 - abs(Heading)
theValue = GetPoint(OppositeHeading, X, Y, 0, 50)
f.write(str(theValue[0]) + ", " + str(theValue[1]) + "\n")
f.write(str(X) + ", " + str(Y) + "\n")


f.close()

#Jesus: you will need 

