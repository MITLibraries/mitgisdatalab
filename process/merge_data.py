import pandas as pd


START_PATH = '/home/jesusg/edoc/MIT-GIS-DataLab/'
ARCMAP_CSV = START_PATH + 'arcmap/arcmap_output/arcmap_data.csv'
PHOTOSCAN_CSV = START_PATH + 'photoscan/photoscan_output/photoscan_data.csv'
OUTPUT_PATH = START_PATH + 'process/data/merged_data.csv'

arc_df = pd.read_csv(ARCMAP_CSV)
photo_df = pd.read_csv(PHOTOSCAN_CSV)

# Display data before the merge
print('Arcmap:\n', arc_df.head(), end='\n\n')
print('Photoscan:\n', photo_df.head(), end='\n\n')

# Set a desired output order of columns
order = ['image_name', 'latitude', 'longitude',
        'yaw', 'pitch', 'roll', 'flying_height']

# Merge the two dataframes together
merged_df = pd.merge(arc_df, photo_df, on='image_name')

# Reorder the merged dataframe
merged_df = merged_df[order]

# Display data post-merge
print('Merged data:\n', merged_df.head())

# Export merged data to a csv file
merged_df.to_csv(OUTPUT_PATH, index=False)
