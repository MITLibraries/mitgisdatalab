import math
from math import pi
from math import tan
from math import sqrt
import pandas as pd
import os


# Relative location where the output csv file is stored.
REL_OUTPUT_LOC = 'footprint-output/mod-output.csv'

# Location where the drone data lives
DRONE_CSV_PATH = 'data/merged_data.csv'

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
    # Obtain path for drone csv data
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(cur_dir, DRONE_CSV_PATH)

    drone_df = pd.read_csv(full_path)
    print('Current Data being processed:\n', drone_df.head()) 

    x = 640297.412572  
    y = 3822531.071888
    coords = (x, y)

    # This is purely a testing value
    heading = 90.225403

    # TODO: Uncomment the code below
    #width, height = calculate_width_height(109)
    # Delete the below two lines
    width = 40.0 / 2.0
    height = 30.0 / 2.0

    poly_array, corners = get_footprint(calculate_headings(heading), coords,
                                        width, height)

    write_to_csv(corners)


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
def get_point(cur_heading, x, y, distance):
    rel_heading, quadrant = get_heading(cur_heading)
  
    calc_distance = 0.0
    opposite = 1.0
    rad_heading = rel_heading * pi / 180.0

    # Incrementally, the hypotenuse (distance) is found by moving along the
    # opposite side one step at a time. Increasing the opposite slowly helps
    # find an adjacent side length, which then allows the use of tan to find
    # the hypotenuse, or current distance away from origin.
    while calc_distance < distance:
	# New adjacent is calculated given new opposite position
        adjacent = opposite / tan(rad_heading)

	# These conditionals ensure that the signs of X/Y coordinates are
        # correct depending on the quadrant specified by the yaw (heading)
        newX, newY = assign_xy_signs(quadrant, adjacent, opposite)

        calc_distance = math.sqrt((newX * newX) + (newY * newY))
        opposite += 1.0
    
    return [newX + x, newY + y]


# Return the adjusted heading that will be used for tan operations
def get_heading(heading):
    if heading < 90.0:
        quadrant = 1
        rel_heading = 90.0 - heading
    elif heading < 180.0:
        quadrant = 2
        rel_heading = 180.0 - heading
    elif heading < 270.0:
        quadrant = 3
        rel_heading = 270.0 - heading
    elif heading < 360.0:
        quadrant = 4
        rel_heading = 360.0 - heading
    
    return [rel_heading, quadrant]


# Get the xy pair with correct signs depending on quadrant
def assign_xy_signs(quad, adj, opp):
    if quad == 1:
        newX = adj
        newY = opp
    elif quad == 2:
        newX = opp
        newY = adj * -1.0
    elif quad == 3:
        newX = adj * -1.0
        newY = opp * -1.0
    elif quad == 4:
        newX = opp * -1.0
        newY = adj

    return [newX, newY]




# Find all the headings needed to obtain the footprint
# TODO: When finding left headings, will heading ever be over 360? Wondering
# this because the degrees are substracted from referance heading
def calculate_headings(init_heading):
    heading_dict = dict()
    
    # Find the first needed heading (known as modified heading)
    if init_heading < 0.0:
        mod_heading = 360.0 + init_heading
    else:
        mod_heading = init_heading
    # Save the modified heading to the dictionary
    heading_dict['mod'] = mod_heading 

    # Find the second needed heading (known as forward right heading)
    fwd_right_heading = mod_heading + 90.0
    if fwd_right_heading > 360.0:
        fwd_right_heading = fwd_right_heading - 360.0
    # Save the forward right heading into the dictionary
    heading_dict['fwdr'] = fwd_right_heading

    # Third heading (forward left heading)
    fwd_left_heading = mod_heading - 90.0
    if fwd_left_heading > 360.0:
        fwd_left_heading = fwd_left_heading - 360.0
    # Save into dictionary
    heading_dict['fwdl'] = fwd_left_heading

    # Similar operations need to be perfored on the opposite side of footprint
    if mod_heading > 180.0:
        opposite_heading = mod_heading - 180.0
    else:
        opposite_heading = mod_heading + 180.0
    heading_dict['opp'] = opposite_heading

    bkwd_right_heading = opposite_heading + 90.0
    if bkwd_right_heading > 360.0:
        bkwd_right_heading = bkwd_right_heading - 360.0
    heading_dict['oppr'] = bkwd_right_heading

    bkwd_left_heading = opposite_heading - 90.0
    if bkwd_left_heading > 360.0:
        bkwd_left_heading = bkwd_left_heading - 360.0
    heading_dict['oppl'] = bkwd_left_heading

    return heading_dict

# Given xy and heading dictionary it finds the footprint
def get_footprint(heading_dict, coords, width, height):
    corners = list()
    poly_array = None
    
    # NOTE: heading_dict contains all needed headings with the labes as the
    # following: 'mod', 'fwdr', 'fwdl', 'opp', 'oppr', 'oppl'

    fwd_coord = get_point(heading_dict['mod'], coords[0],
                        coords[1], height)
    corners.append(fwd_coord)
    
    # The value is saved here to be added to the polygon FIRST
    # TODO: Must be added to array_for_poly
    first_poly_point = get_point(heading_dict['fwdr'], fwd_coord[0], 
                                fwd_coord[1], width)
    corners.append(first_poly_point)

    # Saved to be added to the polygon SECOND
    # TODO: Must be added to array_for_poly
    second_poly_point = get_point(heading_dict['fwdl'], fwd_coord[0],
                                fwd_coord[1], width)
    corners.append(second_poly_point)

    # Repeat the process for the opposite side of the polygon
    bkwd_coord = get_point(heading_dict['opp'], coords[0],
                                coords[1], height)
    corners.append(bkwd_coord)

    # THIRD POLYGON
    # TODO: Must be added to array_for_poly
    third_poly_point = get_point(heading_dict['oppr'], bkwd_coord[0],
                                bkwd_coord[1], width)
    corners.append(third_poly_point)

    # FOURTH POLYGON
    # TODO: Must be added to array_for_poly
    fourth_poly_point = get_point(heading_dict['oppl'], bkwd_coord[0],
                                bkwd_coord[1], width)
    corners.append(fourth_poly_point)

    return [poly_array, corners]


# Write the found footprint to csv file
def write_to_csv(corners):
    # Finding absolute path where returned values are outputted
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(cur_dir, REL_OUTPUT_LOC)


    f = open(full_path, 'w')

    f.write('x,y,photoID\n')
    for value in corners:
        f.write(str(value[0]) + ', ' + str(value[1]) + '\n')
    f.close()


if __name__ == '__main__':
    main()
   
