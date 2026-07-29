import pandas as pd
import geopandas as gpd
import folium
import base64
from folium.plugins import FloatImage
from PIL import Image
from io import BytesIO
#from app import Bigdf

COUNTY = "County"
POP = "Population"
AREA = "Area" 
BLACK_RAS_bin = "Black Raspberry Rank"
WINEBERRY_bin = "Wineberry Rank"
BIVAR_COLOR = "bivariate_color"
#County_data_dir = "maryland_counties.geojson"

#from load_biData import load_biData
#----------------------------Variables to play with---------------------------
# Bivariate color map - feel free to modify these colors!
colors = [
    "#e8e8e8", "#AEAEC3", "#74749f",
    "#eeaeae", "#b47489", "#7a3a65",
    "#f47474", "#ba3a4f", "#80002B"
]
# The units we are using - feel free to change the quantitative units!
BLACK_RAS = "# of Black Raspberry"
WINEBERRY = "# of Wineberry"
# ---------------------------json of county boundaries---------------------------
#gdf = load_biData()

# ---------------------------Define a 3x3 bivariate color palette--------------------------------
#    rows = WINEBERRY, cols = BLACK_RAS
bivar_colors = {
    ("Low",  "Low"):  colors[0],
    ("Medium",  "Low"):  colors[1],
    ("High", "Low"):  colors[2],
    ("Low",  "Medium"):  colors[3],
    ("Medium",  "Medium"):  colors[4],
    ("High", "Medium"):  colors[5],
    ("Low",  "High"): colors[6],
    ("Medium",  "High"): colors[7],
    ("High", "High"): colors[8]
}
# So our code does freak out if there's a null
# for null values, we will use light gray (#cccccc)

#gdf = load_biData()
def create_bivariate_map(gdf):
    # ---------------------------Create map---------------------------
    # With bounds to restrict panning and zooming to Maryland
    sw = [37.8, -79.6]
    ne = [39.8, -75.0]
    color_dict = dict(zip(gdf["NAME10"], gdf[BIVAR_COLOR]))
    count1_dict = dict(zip(gdf["NAME10"], gdf[BLACK_RAS]))
    count2_dict = dict(zip(gdf["NAME10"], gdf[WINEBERRY]))
    m = folium.Map(
        location=[39.0, -76.7], # Will center on this location (center of MD essentially)
        zoom_start=7, # How far we're zoomed initially
        min_zoom=7,      # cannot zoom out past this (1 "-" from initial zoom)
        max_bounds=True,  # prevent panning outside bounds
        min_lat=sw[0],    # ^^ the bounds
        max_lat=ne[0],
        min_lon=sw[1],
        max_lon=ne[1],
        maxBoundsViscosity=1.0,
        tiles = "cartodbpositron"
    )


    # ---------------------------Drawing County lines and filling with bivariate colors---------------------------
    folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            "fillColor": color_dict.get(feature["properties"]["NAME10"], "#cccccc"), 
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.8,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["NAME10", BLACK_RAS, WINEBERRY, POP, AREA],
            aliases=["County:", "Black Raspberry:", "Wineberry:", "Population:", "Area:"],
            localize=True
        )
    ).add_to(m)
    with open("Final_Product/maps/Bivar_legend.jpg", "rb") as f:
        img = Image.open(f)
        img = img.resize((200, 200))  # Resize to smaller size
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        encoded = base64.b64encode(buffer.getvalue()).decode()

    data_uri = f"data:image/jpeg;base64,{encoded}"

    FloatImage(data_uri, bottom=60, left=75).add_to(m)

    m.fit_bounds([sw, ne]) # drawing our box around Maryland so we can't pan outside of it

    #m.save("bivariate_map.html") # Save the map to an HTML file (can open in browser)
    return m._repr_html_()

#create_bivariate_map(gdf)