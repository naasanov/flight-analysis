import pandas as pd
df = pd.read_csv('Business_Dataset.csv', low_memory=False)

THRESHOLD = 1.25

# Filter to only the year of 2023
df = df[df['Year'] == 2023]

# Get the average fare per mile for each route
df['fare per mile'] = df['fare'] / df['nsmiles']

# Remove any instances of (Metropolitan Area) in the destination cities
df['city2'] = df['city2'].str.replace(r'\s*\(Metropolitan Area\)', '', regex=True)

# Get fare per mile for each city across each quarter
fares_pivot = df.pivot_table(index='city2', columns='quarter', values='fare per mile', aggfunc='mean').reset_index()
fares_pivot.iloc[:, 1:] = fares_pivot.iloc[:, 1:].round(2)
fares_pivot = fares_pivot.rename(columns={"city2": "city"})

# Extract the state from the city column
fares_pivot['state'] = fares_pivot['city'].str.split(", ").str[1]
fares_pivot['city'] = fares_pivot['city'].str.split(", ").str[0]

# Determine the minimum and maximum average fare per mile
fares_pivot['min_fare'] = fares_pivot.iloc[:,1:5].min(axis=1)
fares_pivot['max_fare'] = fares_pivot.iloc[:,1:5].max(axis=1)

# Determine the quarters in which the minimum and maximum fare per mile was
fares_pivot['min_quarter'] = fares_pivot.iloc[:,1:5].idxmin(axis=1)
fares_pivot['max_quarter'] = fares_pivot.iloc[:,1:5].idxmax(axis=1)

# Filter by cities that have significant differences between their minimum and maximum passengers between quarters
fares_pivot = fares_pivot[fares_pivot['max_fare'] > fares_pivot['min_fare'] * THRESHOLD]
fares_pivot = fares_pivot.sort_values(by='min_fare').reset_index()

# Derive relative differences in fare per mile between quarters
for i in range(1,5):
    fares_pivot[f'Q{i}_relative_to_min'] = fares_pivot[i] / fares_pivot['min_fare']
pd.set_option('display.max_columns', None)

# Extract the maxiumum relative change to the minimum fare per mlie
fares_pivot['max_relative'] = fares_pivot.iloc[:,11:15].max(axis=1)

fares_pivot.to_csv('fares.csv', index=False)