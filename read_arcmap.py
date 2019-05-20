import arcpy


shapefile = 'E:\\UserFiles\\jesusg\\drone2map\\firstd2m_pointsWithElev\\pointswelev.shp'

try:
    with arcpy.da.SearchCursor(shapefile, ("ImageName", "Latitude", "Longitude", "flyingHeig")) as cursor:
        for row in cursor:
            print 'ImageName' + str(row[0])
            print 'Lat:' + str(row[1])
            print 'Long:' + str(row[2])
            print 'flyingHeig:' + str(row[3])
        del cursor
except:
    print arcpy.GetMessages()
    raise
