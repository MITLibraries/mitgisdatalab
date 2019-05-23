import pandas as pd
import os

#START_PATH = '/home/jesusg/edoc/MIT-GIS-DataLab/'
START_PATH = os.path.dirname(os.path.realpath(__file__))
ARCMAP_CSV = START_PATH + '/arcmap/arcmap_output/arcmap_data.csv'
PHOTOSCAN_CSV = START_PATH + '/photoscan/lowRes/low_data.csv'
OUTPUT_PATH = START_PATH + '/process/data/merged_data.csv'

arc_df = pd.read_csv(ARCMAP_CSV)
photo_df = pd.read_csv(PHOTOSCAN_CSV)

# Display data before the merge
print 'Arcmap:\n'
print arc_df.head() 
print 'Photoscan:\n'
print photo_df.head() 

# Set a desired output order of columns
order = ['image_name', 'latitude', 'longitude',
        'yaw', 'pitch', 'roll', 'flying_height']

# Merge the two dataframes together
merged_df = pd.merge(arc_df, photo_df, on='image_name')

# Reorder the merged dataframe
merged_df = merged_df[order]

# Display data post-merge
print'Merged data:\n'
print merged_df.data()

# Export merged data to a csv file
merged_df.to_csv(OUTPUT_PATH, index=False)
