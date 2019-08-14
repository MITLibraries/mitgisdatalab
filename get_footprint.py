import arcpy
import pandas as pd
from arcpy import env
from nadir import *
from non_nadir import *
from config import *

env.overwriteOutput = True


def main():
    drone_df = pd.read_csv(DRONE_META_PATH)

    add_poly_cursor = init_add_cursor()

    # The polygon of the foot print
    polygon = None

    for index, row in drone_df.iterrows():
        # Identify which process to perform on the current image
        if (row['pitch'] <= -89.0) and (row['pitch'] >= -91.0):
            # Process for images directly below drone
            polygon = process_nadir(row)
        else:
            # Images not taken directly below the drone
            polygon_path = process_nonnadir(row)

            # Use a cursor to access the polygon
            with arcpy.da.SearchCursor(polygon_path, ['SHAPE@']) as cursor:
                for line in cursor:
                    polygon = line[0]

        add_poly_cursor.insertRow([polygon, row['image_name'][:-4], row['latitude'], row['longitude'], row['yaw'], row['pitch'], row['roll'], row['flying_height'], row['elevation']])

    del add_poly_cursor


def init_add_cursor():
    spatial_ref = arcpy.Describe(TEMPLATE).spatialReference

    arcpy.CreateFeatureclass_management(OUT_PATH, OUT_NAME, GEOMETRY_TYPE,
                                        TEMPLATE, HAS_M, HAS_Z, spatial_ref)

    return arcpy.da.InsertCursor(OUTFILE, ['SHAPE@', 'photoID', 'latitude', 'longitude', 'yaw', 'pitch', 'roll', 'fly_height', 'elevation'])



if __name__ == '__main__':
    main()

