import arcpy
import pandas as pd
from arcpy import env
from nadar import *
from non_nadar import *
from config import *

env.overwriteOutput = True


def main():
    drone_df = pd.read_csv(DRONE_CSV_PATH)
    print(drone_df.head())

    add_poly_cursor = init_add_cursor()

    # The polygon of the foot print
    polygon = None

    for index, row in drone_df.iterrows():
        # Identify which process to perform on the current image
        if (row['pitch'] <= -89.0) and (row['pitch'] >= -91.0):
            # Process for images directly below drone
            polygon = process_nadar(row)
        else:
            # Images not taken directly below the drone
            polygon_path = process_nonnadar(row)

            # Use a cursor to access the polygon
            with arcpy.da.SearchCursor(polygon_path, ['SHAPE@']) as cursor:
                for line in cursor:
                    polygon = line[0]

        add_poly_cursor.insertRow([polygon, row['image_name'][:-4]])

    del add_poly_cursor


def init_add_cursor():
    spatial_ref = arcpy.Describe(TEMPLATE).spatialReference

    arcpy.CreateFeatureclass_management(OUT_PATH, OUT_NAME, GEOMETRY_TYPE,
                                        TEMPLATE, HAS_M, HAS_Z, spatial_ref)

    return arcpy.da.InsertCursor(OUTFILE, ['SHAPE@', 'photoID'])



if __name__ == '__main__':
    main()
