import PhotoScan
from os import listdir

PHOTO_PATH = 'E:/UserFiles/jesusg/testing/SpoonOnlyImages/'
PROJ_PATH = 'E:/UserFiles/jesusg/testing/thirdRes/pyproj.psx'

all_photos = [PHOTO_PATH + f for f in listdir(PHOTO_PATH)]
print('All files:\n', all_photos)


doc = PhotoScan.app.document
chunk = doc.addChunk()

chunk.addPhotos(all_photos)
chunk.matchPhotos(accuracy=PhotoScan.LowestAccuracy, generic_preselection=True,
                  reference_preselection=True)
chunk.alignCameras()
chunk.buildDepthMaps(quality=PhotoScan.LowestQuality, filter=PhotoScan.AggressiveFiltering)
chunk.buildDenseCloud()
# Currently working on the build mesh phase
# chunk.buildModel(surface_type='')



"""
try:
    doc.save(PROJ_PATH)

except RuntimeError:
    PhotoScan.app.messageBox('Unable to save project')
"""
