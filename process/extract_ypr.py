import os
import pandas as pd
from config import * 


def main():
    path = './'
    
    image_list = find_image_paths(path)
    yaw_list = list()
    pitch_list = list()
    roll_list = list()

    print(image_list)
    print(len(image_list))

    for image in image_list:
        yaw, pitch, roll = find_metadata(image)
    
        # Prepare values to be transformed to CSV
        image_list.append(image[-12:])
        yaw_list.append(yaw)
        pitch_list.append(pitch)
        roll_list.append(roll)

    d = {'image_name': image_list, 'yaw': yaw_list,
        'pitch': pitch_list, 'roll': roll_list}

    df = pd.DataFrame(data=d)
    df.head()
    
    df.to_csv(get_full_path('cam_orientation.csv'), index=False)


def find_image_paths(path):
    images = list()

    for r, d, f in os.walk(path):
        for file in f:
            if '.JPG' in file:
                images.append(os.path.join(r, file))

    return images


def find_metadata(image_path):
    # Open the file (JPG)
    image = open(image_path, 'rb')
    data = image.read()

    # Locate the metadata in the file
    xmp_start = data.find(b'<x:xmpmeta')
    xmp_end = data.find(b'</x:xmpmeta')
    xmp_str = data[xmp_start:xmp_end+12]

    return parse_xmp(xmp_str)


def parse_xmp(xmp_str):
    # Make return xmp string a list to iterate through fields
    xmp_list = xmp_str.split()

    # Dict to store the needed metadata
    real_meta = dict()

    for x in xmp_list:
        name_utf = x.decode('utf-8')
        if name_utf[:9] == 'drone-dji':
            # Get the key-value pair for the specific field
            key, value = parse_field(name_utf)

            real_meta[key] = value

    yaw = real_meta['drone-dji:GimbalYawDegree']
    pitch = real_meta['drone-dji:GimbalPitchDegree']
    roll = real_meta['drone-dji:GimbalRollDegree']

    return (yaw, pitch, roll)


def parse_field(field):
    field_elems = field.split('=')
    key = field_elems[0]
    value = convert_value(field_elems[1])

    return key, value


def convert_value(raw_value):
    init_chars = raw_value[:2]

    if init_chars not in ['"+', '"-']:
        return raw_value
    elif init_chars == '"+':
        return float(raw_value[2:-1])
    else:
        return -float(raw_value[2:-1])


if __name__ == '__main__':
    main()
