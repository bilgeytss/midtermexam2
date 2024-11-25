import pandas as pd
import geopandas as gpd
import folium
import geodatasets
import matplotlib.pyplot as plt

df1 = pd.read_csv("volcano_data_2010.csv")
df = df1.loc[:, ("Year", "Name", "Country", "Latitude", "Longitude", "Type")]
df.info()

geometry = gpd.points_from_xy(df['Longitude'], df['Latitude'])
geo_df = gpd.GeoDataFrame(
    df[['Year', 'Name', 'Country', 'Latitude', 'Longitude', 'Type']], geometry=geometry
)
print(geo_df.head())

world = gpd.read_file(geodatasets.get_path("naturalearth.land"))
print(df['Type'].unique())

import geopandas as gpd
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(24, 18))
world.plot(ax=ax, alpha=0.4, color="grey")
geo_df.plot(column="Type", ax=ax, legend=True)
plt.title("Volcanoes")
plt.show()

map = folium.Map(location=[13.406, 80.110], tiles="CartoDB Positron", zoom_start=9)
map.save("map.html")

map = folium.Map(location=[13.406, 80.110], tiles="OpenStreetMap", zoom_start=9)
map.save("osm_map.html")

geo_df_list = [[point.xy[1][0], point.xy[0][0]] for point in geo_df.geometry]
for i, coordinates in enumerate(geo_df_list):
    
    if geo_df.Type[i] == "Stratovolcano":
        type_color = "green"
    elif geo_df.Type[i] == "Complex volcano":
        type_color = "blue"
    elif geo_df.Type[i] == "Shield volcano":
        type_color = "orange"
    elif geo_df.Type[i] == "Lava dome":
        type_color = "pink"
    else:
        type_color = "purple"

   
    folium.Marker(
        location=coordinates,
        popup=(
            f"Year: {geo_df.Year[i]}<br>"
            f"Name: {geo_df.Name[i]}<br>"
            f"Country: {geo_df.Country[i]}<br>"
            f"Type: {geo_df.Type[i]}<br>"
            f"Coordinates: {geo_df_list[i]}"
        ),
        icon=folium.Icon(color=type_color),
    ).add_to(map)


map.save("volcano_map.html")

from folium import plugins
map = folium.Map(location=[15, 30], tiles="CartoDB dark_matter", zoom_start=2)
heat_data = [[point.xy[1][0], point.xy[0][0]] for point in geo_df.geometry]
plugins.HeatMap(heat_data).add_to(map)
map.save("volcano_heatmap.html")
import webbrowser
import os

webbrowser.open(f"file://{os.path.abspath('volcano_heatmap.html')}")

