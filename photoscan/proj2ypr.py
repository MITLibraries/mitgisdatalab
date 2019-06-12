import PhotoScan


# Path of the project you would like to extract the data from.
PROJ_PATH = ''
# The path where the output (data) will be saved.
OUTPUT_PATH = ''


def main():
    doc = PhotoScan.app.document

    # Assign a project to the PhotoScan document object
    doc.open(PROJ_PATH)

    chunk = PhotoScan.app.document.chunk

    extract_ypr(chunk)


# Given a chunk, yaw, pitch, and roll are found and saved as a csv file
def extract_ypr(chunk):
    image_list = list()
    yaw_list = list()
    pitch_list = list()
    roll_list = list()

    # Iterate through each photo
    for camera in chunk.cameras:
        # Save camera name for reference
        image_list.append(camera.label)

        # Access specific photo meta data to save yaw, pitch, and roll
        yaw = float(camera.photo.meta['DJI/GimbalYawDegree'])
        pitch = float(camera.photo.meta['DJI/GimbalPitchDegree'])
        roll = float(camera.photo.meta['DJI/GimbalRollDegree'])
    
        # Save yaw, pitch, and roll
        yaw_list.append(yaw)
        pitch_list.append(pitch)
        roll_list.append(roll)

    f = open(OUTPUT_PATH, 'w')    
    f.write('image_name,yaw,pitch,roll\n')
    
    for row in zip(image_list, yaw_list, pitch_list, roll_list):
        print(row[0])
        f.write(str(row[0]) + '.JPG,' + str(row[1]) + ','
                + str(row[2]) + ',' + str(row[3]) + '\n')

    f.close()


if __name__ == "__main__":
    main()
