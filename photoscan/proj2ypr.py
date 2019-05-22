import pandas as pd
import PhotoScan


PROJ_PATH = 'E:/UserFiles/jesusg/testing/lowRes/lowScan.psx'
OUTPUT_PATH = 'E:/UserFiles/jesusg/testing/lowRes/low_data.csv'


def main():
    # Create a PhotoScan document object that will be used for particular project
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
        roll_list.append(row)

    # Dictionary is created using the data
    d = {'image_name': image_list, 'yaw': yaw_list,
        'pitch': pitch_list, 'roll': roll_list}

    # Dictionary is used to create the pandas dataframe
    df = pd.DataFrame(data=d)
    
    # Newly created dataframe is exported to a csv file
    df.to_csv(OUTPUT_PATH)


# Given a camera's metadata the altitudes are examined
def analyze_altitudes(camera):
    # Access Absolute, Relative, and GPS altitudes
    abs_alt = float(camera.photo.meta['DJI/AbsoluteAltitude'])
    rel_alt = float(camera.photo.meta['DJI/RelativeAltitude'])
    gps_alt = float(camera.photo.meta['Exif/GPSAltitude'])
    
    print(camera.label, 'has the following altitudes:')
    print('Absolute: %f\n Relative: %f' % (abs_alt, rel_alt))
    
    # GPS altitude is a bit more exact than the absolute altitude
    print('GPS altitude: %f' % gps_alt)


