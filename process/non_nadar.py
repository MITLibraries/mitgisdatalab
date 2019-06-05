import os
import arcpy
import pandas as pd
from arcpy import env
from arcpy.sa import Viewshed2


env.overwriteOutput = True

def process_nonnadar(row):
    arcpy.CheckOutExtension('Spatial')

    h_start = 360.0 - row['yaw'] - H_OFFSET
    h_end = 360.0 - row['yaw'] + H_OFFSET

    v_upper = row['pitch'] + V_OFFSET
    v_lower = row['pitch'] - V_OFFSET

    obs_offset = row['flying_height']

    # An input observer feature must be created
    input_obs = create_observer((row['longitude'], row['latitude']))

    # Create a buffer around 


    output_view = Viewshed2(in_raster=INPUT_RAS,
                            in_observer_features=INPUT_OBS,
                            analysis_type=A_TYPE,
                            observer_offset=obs_offset,
                            horizontal_start_angle=h_start,
                            horizontal_end_angle=h_end,
                            vertical_upper_angle=v_upper,
                            vertical_lower_angle=v_lower,
                            analysis_method=A_METHOD)
    
    # Save the viewshed
    output_view.save(OUTPUT_PATH + 'vs_' + row['image_name'])


# Coordinates of the drone are turned into a point feature class to be used as
# the observer when generating the viewshed
def create_observer(coords):
    point = arcpy.Point(coords[0], coords[1])
    
    return arcpy.PointGeometry(point)

