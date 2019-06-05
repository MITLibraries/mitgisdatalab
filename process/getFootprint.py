import arcpy
import pandas as pd
from arcpy import env
from nadar import *
from non_nadar import *
from config import *

env.overwriteOutput = True


def main():
    drone_df = pd.read_csv(get_full_path(DRONE_CSV_PATH))
    print('Current Data being processed:\n', drone_df.head())

    spatial_ref = arcpy.Describe(TEMPLATE).spatialReference
    arcpy.CreateFeatureclass_management(OUT_PATH, OUT_NAME, GEOMETRY_TYPE,
                                        TEMPLATE, HAS_M, HAS_Z, spatial_ref)
    add_poly_cursor = arcpy.da.InsertCursor(OUTFILE, ['SHAPE@', 'photoID'])


    for index, row in drone_df.iterrows():
        if (row['pitch'] >= -89.0) and (row['pitch'] <= -91.0):
            polygon = process_nonnadar(row)
        else:
            polygon = process_nadar(row)

        add_poly_cursor.insertRow([polygon, row['image_name']])

    del add_poly_cursor


# Write the found footprint to csv file
def write_to_csv(corners):
    f = open(get_full_path(REL_OUTPUT_LOC), 'w')

    f.write('x,y,photoID\n')
    for value in corners:
        f.write(str(value[0]) + ', ' + str(value[1]) + '\n')
    f.close()


if __name__ == '__main__':
    main()

