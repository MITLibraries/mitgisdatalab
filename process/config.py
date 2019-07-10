import os


# Given a relative path, the full path is returned
def get_full_path(rel_path):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    
    return os.path.join(cur_dir, rel_path)

# ============================================================
# Constants that actually need to be changed.
# Be sure to either use '/' or '\\' when entering a directory.
# ============================================================
# Path to the directory where all the photos you wish to process are stored.
PHOTOS_DIR = 'E:/UserFiles/jesusg/testing/SpoonOnlyImages'

# Shapefile containing lat, long for all images
# Path to the products/D2M.gdb/ImagePoints which something that is obtained
# through Drone2Map processing.
PTS_SHP = 'E:\\UserFiles\\jesusg\\testing\\produce_products_test\\products\\D2M.gdb\\ImagePoints'

# Digital surface model used for flying height
# 2D digital surface model found in the products of Drone2Map.
DSM_FLIGHT = 'E:\\UserFiles\\jesusg\\testing\\produce_products_test\\products\\2D\\produce_products_test_DSM.tif'

# Here goes the digital elevation model used when performing the Viewshed2 ArcPy
# command. Could be the same as above if no resolution changes are made.
DEM_FILE = ''


# ============= #
# Configuations #
# ============= #

# =======================================================================
# Below this line are relative paths and variables that do not have to be
# changed, but can be.
# =======================================================================

# Location where the drone data lives
DRONE_META_PATH = get_full_path('data/merged_data.csv')


# =========================================================================
# Constants needed for obtaining all required data in CSV format
# =========================================================================
# Shapefile containing lat, long, and flying height. This is an intermidiate
# file created with the llh_extraction.py script to get needed values.
FLIGHT_PTS_SHP = get_full_path('data/temp/LocNdHeight.shp')

# Where the data is extracted and saved in csv format
ARCMAP_CSV = get_full_path('data/arcmap_data.csv')

# Location of yaw, pitch, and roll values
YPR_CSV = get_full_path('data/ypr_data.csv')

# Merged csv data
MERGED_CSV = get_full_path('data/merged_data.csv')

# ============================================================================
# Constants for the width and height of a single image footprint on the ground
# Constants set below are specific to the DJI Phantom 4 camera.
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
OUT_PATH = get_full_path('data/index/')
OUT_NAME = 'index_shapefile.shp'
OUTFILE = OUT_PATH + OUT_NAME
GEOMETRY_TYPE = 'POLYGON'
TEMPLATE = get_full_path('data/templates_shp/template.shp')
HAS_M = 'DISABLED'
HAS_Z = 'DISABLED'


# ==============================================
# Variables needed for handling non-nadar images
# Mainly for Viewshed2 command.
# ==============================================
# Where non-nadar layers are stored and manipulated to produce a polygon. Used
# in RasterToPolygon and Generalize_edit.
LAYER_STORAGE = get_full_path('data/temp/')

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
OUTER_RADIUS = 200.0
OUTER_3D = '#'

A_METHOD = 'ALL_SIGHTLINES'

# Horizontal and vertical offsets to be used for finding angle ranges
H_OFFSET = 30.0
V_OFFSET = 23.0 


# =================================
# Working with metadata of the JPEG
# =================================
# Tuple of EXIF tags we do not care about (There are more)
BAD_META = ('JPEGThumbnail', 'Image ImageDescription', 'Image Make',
            'Image Model', 'Image Orientation', 'Image XResolution',
            'Image YResolution', 'Image ResolutionUnit', 'Image Software')

# Tuple of EXIF tags we care about
GOOD_META = ('GPS GPSAltitudeRef', 'GPS GPSAltitude', 'EXIF SubjectDistanceRange')
