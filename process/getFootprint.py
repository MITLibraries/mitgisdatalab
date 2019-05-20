import math
from math import pi
from math import tan
from math import sqrt
import os


# Relative location where the output csv file is stored.
REL_OUTPUT_LOC = 'footprint-output/data-output.csv'

# ============================================================================
# Constants for the width and height of a single image footprint on the ground
# ============================================================================
# Sensor width of the camera (millimeters)
S_W = 12.8333
# Focal length of the camera (millimeters)
F_R = 8.8
# Image width (pixels)
IM_W = 4608
# Image height (pixels)
IM_H = 3456


def main():
    x = 639707.969  
    y = 3823600.569
    coords = (x, y)

    # This is purely a testing value
    heading = -94.3

    corners = get_footprint(heading, x, y)
    write_to_csv(corners, coords)

    width, height = calculate_width_height(109)
    print('Width: ', width)
    print('Height: ', height)


# Given a flight height (relative altitude) and utilizing the constants 
# specified above, the width/height of image footprint is calculated.
def calculate_width_height(alt):
    # Ground sampling distance (centimeters/pixel)
    gsd = (S_W*alt*100) / (F_R*IM_W)

    # Width of single image footprint on ground (meters)
    width = (gsd*IM_W) / 100

    # Height of single image footprint on ground (meters)
    height = (gsd*IM_H) / 100

    return [width, height]


# Given a particular heading and distance the corner is found. 
def get_point(currentHeading, x, y, distance):
    
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

    corners.append(get_point(modHeading, x, y, 50))
    
    # Find the opposite corner of the initial
    oppositeHeading = 180 - abs(yaw)
    corners.append(get_point(oppositeHeading, x, y, 50))

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
   
