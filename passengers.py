import pandas as pd
df = pd.read_csv('Business_Dataset.csv', low_memory=False)

THRESHOLD = 1.5

# Filter to only the year of 2023
df = df[df['Year'] == 2023]

# Remove any instances of (Metropolitan Area) in the destination cities
df['city2'] = df['city2'].str.replace(r'\s*\(Metropolitan Area\)', '', regex=True)

# Get passenger volume for each city across each quarter
passengers_pivot = df.pivot_table(index='city2', columns='quarter', values='passengers', aggfunc='sum').reset_index()
passengers_pivot = passengers_pivot.rename(columns={"city2": "city"})

# Extract the state from the city column
passengers_pivot['state'] = passengers_pivot['city'].str.split(", ").str[1]
passengers_pivot['city'] = passengers_pivot['city'].str.split(", ").str[0]

# Add yearly passenger volume for each city as well
passengers_pivot['total'] = passengers_pivot[[1, 2, 3, 4]].sum(axis=1)

# Determine the minimum and maximum passenger volume
passengers_pivot['min_passengers'] = passengers_pivot.iloc[:,1:5].min(axis=1)
passengers_pivot['max_passengers'] = passengers_pivot.iloc[:,1:5].max(axis=1)

# Determine the quarters in which the minimum and maximum passenger volume was
passengers_pivot['min_quarter'] = passengers_pivot.iloc[:,1:5].idxmin(axis=1)
passengers_pivot['max_quarter'] = passengers_pivot.iloc[:,1:5].idxmax(axis=1)

# Filter by cities that have significant differences between their minimum and maximum passengers between quarters
passengers_pivot = passengers_pivot[passengers_pivot['max_passengers'] > passengers_pivot['min_passengers'] * THRESHOLD]
passengers_pivot = passengers_pivot.sort_values(by='total', ascending=False).reset_index()

# Derive relative differences in passenger volumes between quarters
for i in range(1,5):
    passengers_pivot[f'Q{i}_relative_to_min'] = passengers_pivot[i] / passengers_pivot['min_passengers']

# Extract the maxiumum relative change to the minimum passenger volume
passengers_pivot['max_relative'] = passengers_pivot.iloc[:,12:16].max(axis=1)

passengers_pivot.to_csv('passengers.csv', index=False)