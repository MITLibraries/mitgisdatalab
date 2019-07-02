import pandas as pd
import os
from config import *


def main():
    arc_df = pd.read_csv(ARCMAP_CSV)
    photo_df = pd.read_csv(YPR_CSV)

    # Set a desired output order of columns
    order = ['image_name', 'latitude', 'longitude',
            'yaw', 'pitch', 'roll', 'flying_height']

    # Merge the two dataframes together
    merged_df = pd.merge(arc_df, photo_df, on='image_name')

    # Reorder the merged dataframe
    merged_df = merged_df[order]

    # Display data post-merge
    print'Merged data:\n'
    print merged_df.head()

    # Export merged data to a csv file
    merged_df.to_csv(MERGED_CSV, index=False)


if __name__ == '__main__':
    main()
