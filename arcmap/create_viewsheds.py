import os
import arcpy
from arcpy.sa import Viewshed2


# Check out the ArcGIS Spatual Analyst extension license
arcpy.CheckOutExtension('Spatial')

cur_dir = os.path.dirname(os.path.realpath(__file__))

input_ras = cur_dir + '/../../layers/DEM/dem30a'
input_obs = cur_dir + '/../../layers/test_point.gdb/Export_Output'
output_agl = cur_dir + '/../../layers/view_output/Viewshe_dem50'
a_type = 'FREQUENCY'
verticalError = "#"
outAnalysisRelationTable = "#"
refractCoeff = "#"
surfaceOffset = "#"
observerElevation = "#"
obs_offset = "65.0"
innerRadius = "#"
innerIs3D = "#"
outerRadius = "#"
outerIs3D = "#"
h_start = "229.0"
h_end = "299.0"
v_upper = "-25.0"
v_lower = "-45.0"
#a_method = 'PERIMETER_SIGHTLINES'
a_method = 'ALL_SIGHTLINES'


# The input raster must be processed. Assigned a vertical coordinate system.
spatial_ref = arcpy.Describe(input_ras).spatialReference
print('Spatial references of the input raster:\n', spatial_ref)

# Run the viewshed2
output_view = Viewshed2(input_ras, input_obs, output_agl, a_type, verticalError,
                        outAnalysisRelationTable, refractCoeff, surfaceOffset,
                        observerElevation, obs_offset, innerRadius, innerIs3D,
                        outerRadius, outerIs3D, h_start, h_end, v_upper,
                        v_lower, a_method)
##output_view = Viewshed2(in_raster=input_ras, in_observer_features=input_obs,
##                        out_agl_raster=output_agl, analysis_type=a_type,
##                        observer_offset=obs_offset,
##                        horizontal_start_angle=h_start,
##                        horizontal_end_angle=h_end,
##                        vertical_upper_angle=v_upper,
##                        vertical_lower_angle=v_lower,
##                        analysis_method=a_method)


#output_view.save(output_agl)