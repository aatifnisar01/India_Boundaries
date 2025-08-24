# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 14:11:49 2024

@author: Aatif
"""

import geopandas as gpd
import pandas as pd

# Load the shapefile
shapefile = gpd.read_file('C:/Users/Aatif/Downloads/Indian_states_boundary.geojson')

# Drop the 'id' column
shapefile = shapefile.drop(columns=['id'])

# Load the CSV file
ids = pd.read_csv('C:/Users/Aatif/Downloads/LGD - Local Government Directory, Government of India.csv')

# Merge shapefile with ids
merged = shapefile.merge(ids[['State Name (In English)', 'Census2011 Code']],
                         left_on='Name', right_on='State Name (In English)', how='left')

merged = merged.drop(columns=['State Name (In English)'])

# Update Census2011 Code where Name is 'Telangana'
merged.loc[merged['Name'] == 'Telangana', 'Census2011 Code'] = 28.0
merged.loc[merged['Name'] == 'Dadra and Nagar Haveli and Daman and Diu', 'Census2011 Code'] = 26.0
merged.loc[merged['Name'] == 'Jammu & Kashmir', 'Census2011 Code'] = 1.0
merged.loc[merged['Name'] == 'Andaman & Nicobar', 'Census2011 Code'] = 35.0
merged.loc[merged['Name'] == 'Ladakh', 'Census2011 Code'] = 38.0


merged.columns



# Drop rows where Census2011 Code is NaN
#merged = merged.dropna(subset=['Census2011 Code'])

# Convert 'Census2011 Code' to integer
merged['Census2011 Code'] = merged['Census2011 Code'].astype(int)


# Load the index CSV
index = pd.read_csv('C:/Users/Aatif/Downloads/state_level_inequity_index_modified.csv')

# Remove entire row where state is 'telangana'
index = index[index['state'] != 'telangana']

# Splitting based on discrimination_type
df_sc = index[index['discrimination_type'] == 'SC']
df_st = index[index['discrimination_type'] == 'ST']


# Drop columns 'state', 'discrimination_type', 'state_type' from df_sc
df_sc = df_sc.drop(['state', 'discrimination_type', 'state_type'], axis=1)
# Rename 'inequity_index' to 'SC_inequity_index'
df_sc = df_sc.rename(columns={'inequity_index': 'SC_inequity_index'})


# Drop columns 'state', 'discrimination_type', 'state_type' from df_sc
df_st = df_st.drop(['state', 'discrimination_type', 'state_type'], axis=1)
# Rename 'inequity_index' to 'SC_inequity_index'
df_st = df_st.rename(columns={'inequity_index': 'ST_inequity_index'})


# Merge df_st and df_sc based on state_code
index = pd.merge(df_st, df_sc, on='state_code', suffixes=('_ST', '_SC'))








# Merge index columns into merged based on 'state_code' and 'Census2011 Code'
merged = merged.merge(index[['state_code', 'ST_inequity_index', 'SC_inequity_index']],
                      left_on='Census2011 Code', right_on='state_code', how='left')

# Drop the extra 'state_code' column after merge
merged = merged.drop(columns=['state_code'])



merged['ST_inequity_index'] = merged['ST_inequity_index'].fillna(-1)
merged['SC_inequity_index'] = merged['SC_inequity_index'].fillna(-1)


# Drop the extra 'state_code' column after merge
#merged1 = merged.drop(columns=['geometry'])

# Verify the columns
print(merged.columns)

# Save the DataFrame to CSV
output_path = 'C:/Users/Aatif/Downloads/InequityIndex.csv'  # Replace with your desired output path and file name
merged.to_csv(output_path, index=False)

# SAVE AS SHAPEFILE


# Save the GeoDataFrame to GeoJSON (as an example)
output_path = 'C:/Users/Aatif/Downloads/InequityIndex.geojson'
merged.to_file(output_path, driver='GeoJSON')

# Convert GEOMETRYCOLLECTION to MultiPolygon if needed
merged['geometry'] = merged['geometry'].apply(lambda geom: geom if geom.geom_type.startswith('POLYGON') else None)


# Save the GeoDataFrame to ESRI Shapefile
output_path = 'C:/Users/Aatif/Downloads/InequityIndex'  # Replace with your desired output path and shapefile name
gpd.GeoDataFrame(merged, crs="EPSG:4326", geometry='geometry').to_file(output_path, driver='ESRI Shapefile')
