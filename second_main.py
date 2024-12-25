import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np
all_files = glob.glob(('C:/Users/saada/Desktop/Capstone Project - Coursera/All Months/*.csv'))

combined_df = pd.DataFrame()


def distance_calculation(row):

    lat1, lon1, lat2, lon2 = map(np.radians, [row['start_lat'], row['start_lng'], row['end_lat'], row['end_lng']])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    # Radius of Earth in kilometers
    R = 6371.0
    distance = R * c
    return distance


for csv_file in all_files:
    df = pd.read_csv(csv_file)
    
    df2 = df.assign(distance_km = distance_calculation)
    #print(df2['distance_km'])
    
    combined_df = pd.concat([combined_df, df2])


electric_members = combined_df[(combined_df['rideable_type'] == 'electric_bike') & (combined_df['member_casual'] == 'member')]
electric_casual = combined_df[(combined_df['rideable_type'] == 'electric_bike') & (combined_df['member_casual'] == 'casual')]

classic_members = combined_df[(combined_df['rideable_type'] == 'classic_bike') & (combined_df['member_casual'] == 'member')]
classic_casual = combined_df[(combined_df['rideable_type'] == 'classic_bike') & (combined_df['member_casual'] == 'casual')]



description_me = electric_members['distance_km'].describe()
description_ce = electric_casual['distance_km'].describe()

description_mc = classic_members['distance_km'].describe()
description_cc = classic_casual['distance_km'].describe()

print(description_cc, description_ce, description_mc, description_me)



plt.figure(figsize=(10,6))

plt.bar('Membership - Electric', electric_members['distance_km'].mean(), label = 'Membership - Electric', edgecolor = 'black')
plt.bar('Membership - Casual', electric_casual['distance_km'].mean(), label = 'Membership - Casual', edgecolor = 'black')
plt.bar('Classic - Electric' ,classic_members['distance_km'].mean(), label = 'Classic - Electric', edgecolor = 'black')
plt.bar('Classic - Casual', classic_casual['distance_km'].mean(), label = 'Classic - Casual', edgecolor = 'black')
plt.xlabel('Group of People')
plt.ylabel('Average Distance Travelled (km)')
plt.title('Distance travelled (km) on Bikes between Casual and Non-Casual Bikers, E-bike Vs. Classic')

plt.show()


