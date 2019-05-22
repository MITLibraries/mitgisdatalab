import pandas as pd
import arcpy
import os


shapefile = 'E:\\UserFiles\\jesusg\\drone2map\\firstd2m_pointsWithElev\\pointswelev.shp'
REL_OUTPUT_LOC = 'arcmap_output/arcmap_data.csv'

try:
    with arcpy.da.SearchCursor(shapefile, ("ImageName", "Latitude", "Longitude", "flyingHeig")) as cursor:
        image_list = list()
        lat_list = list()
        long_list = list()
        flyingHeig_list = list()
        for row in cursor:
            image_list.append(row[0])
            lat_list.append(row[1])
            long_list.append(row[2])
            flyingHeig_list.append(row[3])

        # Data is saved as a dictionary
        d = {'image_name': image_list, 'latitude': lat_list, 
            'longitude': long_list, 'flying_height': flyingHeig_list}

        # Dictionary is transformed into a pandas dataframe
        df = pd.DataFrame(data=d)
        df.head()

        # Obtain desired file path
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        full_path = os.path.join(cur_dir, REL_OUTPUT_LOC)

        # Export data as a csv
        df.to_csv(full_path)

        del cursor
except:
    print(arcpy.GetMessages())
    raise
