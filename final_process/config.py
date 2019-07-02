import os


# Given a relative path, the full path is returned
def get_full_path(rel_path):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    
    return os.path.join(cur_dir, rel_path)


# =============
# Configuations
# =============
# Relative location where the output csv file is stored. Outputting a csv is
# not necessary for finding the footprint of the images
REL_OUTPUT_LOC = 'footprint-output/mod-output.csv'

# Location where the drone data lives
DRONE_CSV_PATH = get_full_path('data/merged_data.csv')

# Where the shapefile will be saved
SHP_PATH = 'data/index/'

# =========================================================================
# Constants needed for obtaining all required data in CSV format
# =========================================================================
# Shapefile containing lat, long for all images
PTS_SHP = 'E:\\UserFiles\\jesusg\\testing\\produce_products_test\\products\\D2M.gdb\\ImagePoints'

# Digital surface model used for flying height
DSM_FLIGHT = 'E:\\UserFiles\\jesusg\\testing\\produce_products_test\\products\\2D\\produce_products_test_DSM.tif'

# Shapefile containing lat, long, and flying height
FLIGHT_PTS_SHP = 'E:/UserFiles/jesusg/mitgisdatalab-master/process/data/arcmap_temp/LocNdHeight.shp'

# Where the data is extracted and saved in csv format
ARCMAP_CSV = get_full_path('data/arcmap_data.csv')

# Location of yaw, pitch, and roll values
YPR_CSV = get_full_path('data/ypr_data.csv')

# Merged csv data
MERGED_CSV = get_full_path('data/merged_data.csv')

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


# ==================================================
# Variables set for final shapefile/polygon creation
# ==================================================
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
DEM_FILE = get_full_path('../../layers/DEM/spoondem_1m')

# Where non-nadar layers are stored and manipulated to produce a polygon. Used
# in RasterToPolygon and Generalize_edit.
LAYER_STORAGE = get_full_path('data/non_nadir_temp/')

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


# =================================
# Working with metadata of the JPEG
# =================================
# Be sure to either use '/' or '\\' when entering a directory
PHOTOS_DIR = 'E:/UserFiles/jesusg/testing/SpoonOnlyImages'


# Tuple of EXIF tags we do not care about
BAD_META = ('JPEGThumbnail', 'Image ImageDescription', 'Image Make',
            'Image Model', 'Image Orientation', 'Image XResolution',
            'Image YResolution', 'Image ResolutionUnit', 'Image Software')

GOOD_META = ('GPS GPSAltitudeRef', 'GPS GPSAltitude', 'EXIF SubjectDistanceRange')
