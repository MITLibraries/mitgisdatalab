import math
from math import pi
from math import tan
from math import sqrt
import os


REL_OUTPUT_LOC = 'footprint-output/data-output.csv'

def main():
    x = 639707.969  
    y = 3823600.569

    coords = (x, y)

    # This is purely a testing value
    heading = -94.3

    corners = get_footprint(heading, x, y)
    write_to_csv(corners, coords)

# Given a particular heading, the corner (up until the specified distance) is
# found. TODO: widthOrHeight is a parameter that is considered.
def get_point(currentHeading, x, y, widthOrHeight, distance):
    
    if currentHeading < 90.0:
        quadrant = 1
        relativeHeading = 90.0 - currentHeading
    elif currentHeading < 180.0:
        quadrant = 2
        relativeHeading = 180.0 - currentHeading
    elif currentHeading < 270.0:
        quadrant = 3
        relativeHeading = 270.0 - currentHeading
    elif currentHeading < 360.0:
        quadrant = 4
        relativeHeading = 360.0 - currentHeading

    print('Current heading:', str(currentHeading) + ',', 'Quadrant:', quadrant)
    print('Relative heading:', relativeHeading, end='\n\n') 
    calculatedDistance = 0.0
    opposite = 1.0
    radHeading = relativeHeading * pi / 180.0

    # Incrementally, the hypotenuse (distance) is found by moving along the
    # opposite side one step at a time. Increasing the opposite slowly helps
    # find an adjacent side length, which then allows the use of tan to find
    # the hypotenuse, or current distance away from origin.
    while calculatedDistance < distance:
        print('Opposite: ' + str(opposite))
	# New adjacent is calculated given new opposite position
        adjacent = opposite / tan(radHeading)

	# These conditionals ensure that the signs of X/Y coordinates are
        # correct depending on the quadrant specified by the yaw (heading)
        if quadrant == 1:
            newX = adjacent
            newY = opposite
        elif quadrant == 2:
            newX = opposite
            newY = adjacent * -1.0
        elif quadrant == 3:
            newX = adjacent * -1.0
            newY = opposite * -1.0
        elif quadrant == 4:
            newX = opposite * -1.0
            newY = adjacent
        print('X:', str(newX), ' :: ', 'Y:', str(newY))
        calculatedDistance = math.sqrt((newX * newX) + (newY * newY))
        print('Calculated Distance: ' + str(calculatedDistance))
        opposite += 1.0
    
    print('\nFinal distance: ', calculatedDistance, end='\n\n')
    return [newX + x, newY + y]

# Given xy and heading (yaw) it finds the footprint
def get_footprint(yaw, x, y):
    corners = list()
    
    # Placing yaw in the 0 - 360 range
    if yaw < 0.0:
        modHeading = 360.0 + yaw
    else:
        modHeading = heading

    corners.append(get_point(modHeading, x, y, 0, 50))
    
    # Find the opposite corner of the initial
    oppositeHeading = 180 - abs(yaw)
    corners.append(get_point(oppositeHeading, x, y, 0, 50))

    return corners

# Write the found footprint to csv file
def write_to_csv(corners, coords):
    # Finding absolute path where returned values are outputted
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(cur_dir, REL_OUTPUT_LOC)


    f = open(full_path, 'w')

    f.write('x,y\n')
    for value in corners:
        f.write(str(value[0]) + ", " + str(value[1]) + "\n")
        f.write(str(coords[0]) + ", " + str(coords[1]) + "\n")

    f.close()

    print('Known corners:')
    print(corners)


if __name__ == '__main__':
    main()
   
# Jesus: please read the XY and heading (yaw) and from a file.  It has to be
# projected coordinates, as from Drone2Map, not what I recall the Photoscan
# output - latitude and longitude (6370990 vs 33.20200).
# Puts the heading on a range from 0 - 360



#This code finds the point along the heading of the drone (the direction the drone was facing) and then the point in the opposite
#direction.  You need to go 90 degrees in both directions in order to find the corners as we discussed.  I may not see you the
#rest of today but we will work on this tomorrow.


#Jesus: you will need 

