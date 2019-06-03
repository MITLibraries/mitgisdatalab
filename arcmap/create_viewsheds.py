import os
import arcpy
import pandas as pd
from arcpy import env
from arcpy.sa import Viewshed2


env.overwriteOutput = True

# Check out the ArcGIS Spatual Analyst extension license
arcpy.CheckOutExtension('Spatial')

cur_dir = os.path.dirname(os.path.realpath(__file__))

DATA_PATH = cur_dir + '/../process/data/merged_data.csv'
input_ras = cur_dir + '/../../layers/DEM/dem30a'
input_obs = cur_dir + '/../../layers/test_point.gdb/Export_Output'
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
    pitched_df = df[df['pitch'] not in range(-89, -91, .1)]
    pitched_df.head()

    # Find horizontal and vertical angle ranges using yaw and pitch

    # Create a point feature class using the latitude and longitude

    # Find the viewshed of the image


# Run the viewshed2
output_view = Viewshed2(in_raster=input_ras, in_observer_features=input_obs,
                        analysis_type=a_type,
                        observer_offset=obs_offset,
                        horizontal_start_angle=h_start,
                        horizontal_end_angle=h_end,
                        vertical_upper_angle=v_upper,
                        vertical_lower_angle=v_lower,
                        analysis_method=a_method)


output_view.save(output_path)
