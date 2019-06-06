import os


# =============
# Configuations
# =============

# Relative location where the output csv file is stored. Outputting a csv is
# not necessary for finding the footprint of the images
REL_OUTPUT_LOC = 'footprint-output/mod-output.csv'

# Location where the drone data lives
DRONE_CSV_PATH = 'data/merged_data.csv'

# Where the shapefile will be saved
SHP_PATH = 'data/'
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


# Given a relative path, the full path is returned
def get_full_path(rel_path):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    
    return os.path.join(cur_dir, rel_path)


# ============================================
# Variables set for shapefile/polygon creation
# ============================================
OUT_PATH = get_full_path(SHP_PATH)
OUT_NAME = 'index_shapefile.shp'
OUTFILE = OUT_PATH + OUT_NAME
GEOMETRY_TYPE = 'POLYGON'
TEMPLATE = get_full_path('data/templates_shp/template.shp')
HAS_M = 'DISABLED'
HAS_Z = 'DISABLED'


# ==============================================
# Variables needed for handling non-nadar images
# ==============================================
DEM_FILE = get_full_path('../layers/DEM/spoondem_1m')

# Where non-nadar layers are stored and manipulated to produce a polygon. Used
# in RasterToPolygon and Generalize_edit.
LAYER_STORAGE = get_full_path('data/non_nadar_layers/')

OUT_AGL = '#'
A_TYPE = 'FREQUENCY'
VERT_ERROR = '#'
OUT_A_REL_TABLE = '#'
REFRACT_COEFF = '#'
SURF_OFFSET = '#'
OBS_ELEV = '#'

# This aspect is being determined by the lower vertical angle
INNER_RADIUS = '#'
INNER_3D = '#'

# The maximum distance from which visibility is determined.
OUTER_RADIUS = 80.0
OUTER_3D = '#'

A_METHOD = 'ALL_SIGHTLINES'

# Horizontal and vertical offsets to be used for finding angle ranges
H_OFFSET = 30.0
V_OFFSET = 23.0 
