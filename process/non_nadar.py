import os
#import arcpy
import pandas as pd
#from arcpy import env
#from arcpy.sa import Viewshed2
#from osgeo import ogr


#env.overwriteOutput = True

# Check out the ArcGIS Spatual Analyst extension license
#arcpy.CheckOutExtension('Spatial')

cur_dir = os.path.dirname(os.path.realpath(__file__))

DATA_PATH = cur_dir + '/../process/data/merged_data.csv'
H_OFFSET = 35
V_OFFSET = 10


input_ras = cur_dir + '/../../layers/DEM/dem30a'
#input_obs = cur_dir + '/../../layers/test_point.gdb/Export_Output'
output_path = cur_dir + '/../../layers/view_output/Viewshe_dem50'
a_type = 'FREQUENCY'
obs_offset = "65.0"
h_start = "229.0"
h_end = "299.0"
v_upper = "-25.0"
v_lower = "-45.0"
a_method = 'ALL_SIGHTLINES'


def main():
    # Read in merged_data.csv
    df = pd.read_csv(DATA_PATH)

    # Get the data of images with a non ~-90 pitch
    print(df['pitch'][0])
    pitched_df = df[df['pitch'].between(-89.0, -91.0, inclusive=True)]
    print(pitched_df.head())

    # Find horizontal and vertical angle ranges using yaw and pitch
    view_list = process_images(pitched_df)

    # Create a point feature class using the latitude and longitude

    # Find the viewshed of the image


def process_images(pitched_df):
    # NOTE: possibly switch to a dictionary datastructure to keep track of name
    v_dict = dict()

    for image in pitched_df.iterrows():
        h_start = image['yaw'] - H_OFFSET
        h_end = image['yaw'] + H_OFFSET

        v_upper = image['pitch'] + V_OFFSET
        v_lower = image['pitch'] - V_OFFSET

        obs_offset = image['flying_height']

        # An input observer feature must be created
        input_obs = create_observer()


        output_view = 'aViewshed'
        """
        output_view = Viewshed2(in_raster=INPUT_RAS,
                                in_observer_features=INPUT_OBS,
                                analysis_type=A_TYPE,
                                observer_offset=obs_offset,
                                horizontal_start_angle=h_start,
                                horizontal_end_angle=h_end,
                                vertical_upper_angle=v_upper,
                                vertical_lower_angle=v_lower,
                                analysis_method=A_METHOD)
        """
        v_dict[image['image_name']] = output_view


def save_viewshed(viewshed_list):
    # TODO: Depending on data structure, save viewshed with image name part of
    # the file name.
    output_view.save(output_path)


if __name__ == '__main__':
    main()
