import os
import arcpy
from arcpy import env
from arcpy.sa import Viewshed2


env.overwriteOutput = True

def process_nonnadar(row):
    arcpy.CheckOutExtension('Spatial')

    poly_label = generate_polypath(row['image_name'])

    h_start = 360.0 - row['yaw'] - H_OFFSET
    h_end = 360.0 - row['yaw'] + H_OFFSET

    v_upper = row['pitch'] + V_OFFSET
    v_lower = row['pitch'] - V_OFFSET

    obs_offset = row['flying_height']

    # An input observer feature must be created
    input_obs = create_observer((row['longitude'], row['latitude']))

    output_view = Viewshed2(DEM_FILE, input_obs, OUT_AGL, A_TYPE, VERT_ERROR,
                            OUT_A_REL_TABLE, REFRACT_COEFF, SURF_OFFSET,
                            OBS_ELEV, obs_offset, INNER_RADIUS, INNER_3D,
                            OUTER_RADIUS, OUTER_3D, h_start, h_end, v_upper,
                            v_lower, A_METHOD)

    # The created viewshed raster is converted to a polygon
    arcpy.RasterToPolygon_conversion(output_view, poly_label)

    # The polygon from the viewshed is generalized with a 10 meter tolerance
    arcpy.Generalize_edit(poly_label + '.shp', '10 Meters')

    return poly_label + '.shp'


# Coordinates of the drone are turned into a point feature class to be used as
# the observer when generating the viewshed
def create_observer(coords):
    point = arcpy.Point(coords[0], coords[1])
    
    return arcpy.PointGeometry(point)


def generate_polypath(img_name):
    # Remove the .JPG extension from the name
    clean_name = image_name[:-4]

    return LAYER_STORAGE + 'poly_' + clean_name
