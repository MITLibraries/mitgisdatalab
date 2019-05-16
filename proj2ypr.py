import PhotoScan

PROJ_PATH = 'E:/UserFiles/jesusg/testing/lowRes/lowScan.psx'

# Create a PhotoScan document object that will be used for particular project
doc = PhotoScan.app.document

# Assign a project to the PhotoScan document object
doc.open(PROJ_PATH)

chunk = PhotoScan.app.document.chunk

print('\nWorking with the following cameras:\n', chunk.cameras, end='\n\n')

first_cam = chunk.cameras[0].photo.meta
print('Each camera contains the following meta data:\n',
      first_cam.keys(), end='\n\n')

# Iterate through each photo
for camera in chunk.cameras:
    # Access specific photo meta data to save yaw, pitch, and roll
    yaw = float(camera.photo.meta['DJI/GimbalYawDegree'])
    pitch = float(camera.photo.meta['DJI/GimbalPitchDegree'])
    roll = float(camera.photo.meta['DJI/GimbalRollDegree'])
    
    # Save a vector containing yaw, pitch, and roll
    camera.reference.rotation = PhotoScan.Vector([yaw, pitch, roll])

    # Access Absolute and Relative altitudes
    abs_alt = float(camera.photo.meta['DJI/AbsoluteAltitude'])
    rel_alt = float(camera.photo.meta['DJI/RelativeAltitude'])

    

    print(camera.label)
    print('ref_rot: ', camera.reference.rotation)
    print('absolute: %f \t relative: %f' % (abs_alt, rel_alt))
    
    # GPS altitude is a bit more exact than the absolute altitude
    #print('GPS altitude: %f' % float(camera.photo.meta['Exif/GPSAltitude']))
