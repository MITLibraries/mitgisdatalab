import pandas as pd
import os
import arcpy
from arcpy.sa import ExtractValuesToPoints
from arcpy import env
from config import *

env.overwriteOutput = True

def main():
    # Look at Digital Elevation Model and Flight Point layer to get flyingheight
    arcpy.CheckOutExtension('Spatial')

    ExtractValuesToPoints(PTS_SHP, DSM_FLIGHT, FLIGHT_PTS_SHP, 'NONE', 'VALUE_ONLY')

    
    try:
        # Need to do a little math to find actual flying height, also get altitude
        # NOTE
        with arcpy.da.SearchCursor(FLIGHT_PTS_SHP, ("ImageName", "Latitude", "Longitude", "Altitude", "RASTERVALU")) as cursor:
            image_list = list()
            lat_list = list()
            long_list = list()
            flyingHeig_list = list()
            elevation_list = list()
            for row in cursor:
                image_list.append(row[0])
                lat_list.append(row[1])
                long_list.append(row[2])
                flyingHeig_list.append(row[3] - row[4])
                elevation_list.append(row[4])

            # Data is saved as a dictionary
            d = {'image_name': image_list, 'latitude': lat_list, 
                'longitude': long_list, 'flying_height': flyingHeig_list,
                 'elevation': elevation_list}

            # Dictionary is transformed into a pandas dataframe
            df = pd.DataFrame(data=d)
            df.head()

            # Export data as a csv
            df.to_csv(ARCMAP_CSV, index=False)

            del cursor
    except:
        print(arcpy.GetMessages())
        raise


if __name__ == '__main__':
    main()
