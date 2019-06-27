import os 
import exifread
import pandas as pd
from config import * 


def main():
    path = './'
    
    image_paths = find_image_paths(path)

    # Initialize lists needed for each relevant metadata field
    image_list, yaw_list, pitch_list, roll_list = ([] for i in range(4))
    yaw_flist, pitch_flist, roll_flist = ([] for i in range(3))
    abs_list, rel_list = ([] for i in range(2))

    for path in image_paths:
        # Relevent xmp data is returned
        rel_xmp = find_xmp_metadata(path)
    
        # Prepare values to be transformed to CSV
        image_list.append(path[-12:]); yaw_list.append(rel_xmp['yaw']);
        pitch_list.append(rel_xmp['pitch']); roll_list.append(rel_xmp['roll']);
        yaw_flist.append(rel_xmp['yawf']); 
        pitch_flist.append(rel_xmp['pitchf']);
        roll_flist.append(rel_xmp['rollf']);
        abs_list.append(rel_xmp['abs_alt']);
        rel_list.append(rel_xmp['rel_alt']);

        exif_list = find_exif_metadata(path)

        '''
        for x in xmp_list:
            print(x)

        for e in exif_list:
            print(e)
        '''

    d = {'image_name': image_list, 'yaw': yaw_list,
        'pitch': pitch_list, 'roll': roll_list,
        'absolute_altitude': abs_list, 'relative_altitude': rel_list}

    df = pd.DataFrame(data=d)
    print(df.head())
    
    df.to_csv(get_full_path('cam_meta_extract.csv'), index=False)


def find_image_paths(path):
    images = list()

    for r, d, f in os.walk(path):
        for file in f:
            if '.JPG' in file:
                images.append(os.path.join(r, file))

    return images


def find_xmp_metadata(image_path):
    # Open the file (JPG)
    image = open(image_path, 'rb')
    data = image.read()

    # Locate the metadata in the file
    xmp_start = data.find(b'<x:xmpmeta')
    xmp_end = data.find(b'</x:xmpmeta')
    xmp_str = data[xmp_start:xmp_end+12]

    image.close()

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
            key, value = parse_xmpfield(name_utf)

            real_meta[key] = value

    print('xmp_meta_extracted:\n', real_meta)
    # Dictionary created to store and return relevata xmp metadata
    rel_xmp = dict()

    rel_xmp['yaw'] = real_meta['drone-dji:GimbalYawDegree']
    rel_xmp['pitch'] = real_meta['drone-dji:GimbalPitchDegree']
    rel_xmp['roll'] = real_meta['drone-dji:GimbalRollDegree']
    rel_xmp['yawf'] = real_meta['drone-dji:FlightYawDegree']
    rel_xmp['pitchf'] = real_meta['drone-dji:FlightPitchDegree']
    rel_xmp['rollf'] = real_meta['drone-dji:FlightRollDegree']
    rel_xmp['abs_alt'] = real_meta['drone-dji:AbsoluteAltitude']
    rel_xmp['rel_alt'] = real_meta['drone-dji:RelativeAltitude']
    xmp_list = real_meta.keys()

    return rel_xmp


def find_exif_metadata(image_path):
    f = open(image_path, 'rb')

    tags = exifread.process_file(f)

    exif_dict = dict()
    tag_list = list()

    for tag in tags.keys():
        tag_list.append(tag)
        if tag not in BAD_META:
            exif_dict[tag] = tags[tag]

    f.close()

    return tag_list


def parse_xmpfield(field):
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
