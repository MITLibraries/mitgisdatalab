import arcpy
from math import pi
from math import tan
from math import sqrt
from config import *


def process_nadir(row):
    # Longitude and latitude may be switched in arcmap data OR this script
    coords = (row['longitude'], row['latitude'])
    heading = row['yaw']

    width, height = calculate_width_height(row['flying_height'])
    width = width/2  * 0.75
    height = height/2 * 0.75

    poly_array, corners = get_nadir_footprint(calculate_headings(heading),
                                coords, width, height)

    # Turn poly_array into a polygon and add to the shapefile
    return arcpy.Polygon(poly_array)



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
def get_nadir_footprint(heading_dict, coords, width, height):
    corners = list()
    poly_ptarray = arcpy.Array()

    # NOTE: heading_dict contains all needed headings with the labes as the
    # following: 'mod', 'fwdr', 'fwdl', 'opp', 'oppr', 'oppl'

    fwd_coord = get_point(heading_dict['mod'], coords[0],
                        coords[1], height)
    corners.append(fwd_coord)

    # The point is saved here to be added to the polygon FIRST
    first_poly_point = get_point(heading_dict['fwdr'], fwd_coord[0], 
                                fwd_coord[1], width)
    corners.append(first_poly_point)
    poly_ptarray.add(arcpy.Point(first_poly_point[0], first_poly_point[1]))

    # Saved to be added to the polygon SECOND
    second_poly_point = get_point(heading_dict['fwdl'], fwd_coord[0],
                                fwd_coord[1], width)
    corners.append(second_poly_point)
    poly_ptarray.add(arcpy.Point(second_poly_point[0], second_poly_point[1]))

    # Repeat the process for the opposite side of the polygon
    bkwd_coord = get_point(heading_dict['opp'], coords[0],
                                coords[1], height)
    corners.append(bkwd_coord)

    # THIRD POLYGON POINT
    third_poly_point = get_point(heading_dict['oppr'], bkwd_coord[0],
                                bkwd_coord[1], width)
    corners.append(third_poly_point)
    poly_ptarray.add(arcpy.Point(third_poly_point[0], third_poly_point[1]))

    # FOURTH POLYGON POINT
    fourth_poly_point = get_point(heading_dict['oppl'], bkwd_coord[0],
                                bkwd_coord[1], width)
    corners.append(fourth_poly_point)
    poly_ptarray.add(arcpy.Point(fourth_poly_point[0], fourth_poly_point[1]))

    # The first point needs to be added again to complete the polygon's shape
    poly_ptarray.add(arcpy.Point(first_poly_point[0], first_poly_point[1]))

    return [poly_ptarray, corners]


# Given a particular heading and distance the corner is found. 
def get_point(cur_heading, x, y, distance):
    rel_heading, quadrant = get_heading(cur_heading)

    calc_distance = 0.0
    opposite = 0.0001
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

        calc_distance = sqrt((newX * newX) + (newY * newY))
        opposite += 0.001

    return [newX + x, newY + y]


