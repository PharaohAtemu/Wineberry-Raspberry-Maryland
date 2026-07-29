import pandas as pd
import geopandas as gpd
BLACK_RAS_bin = "Black Raspberry Rank"
WINEBERRY_bin = "Wineberry Rank"
BIVAR_COLOR = "bivariate_color"
County_data_dir = "Final_Product/Plant_County_data/maryland_counties.geojson"
#os.path.join(os.path.dirname(__file__), "Plant_County_data", "maryland_counties.geojson")
County_plant_data_dir = "Final_Product/Plant_County_data/County_Data.csv"
#os.path.join(os.path.dirname(__file__), "Plant_County_data", "County_Data.csv")
import base64
from folium.plugins import FloatImage
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
def get_bivariate_color(row):
    if pd.isna(row[BLACK_RAS_bin]) or pd.isna(row[WINEBERRY_bin]):
        return "#cccccc"
    return bivar_colors[(row[BLACK_RAS_bin], row[WINEBERRY_bin])]



def load_biData():
    BLACK_RAS = "# of Black Raspberry"
    WINEBERRY = "# of Wineberry"
    # ---------------------------json of county boundaries---------------------------
    gdf = gpd.read_file(County_data_dir)
    # ---------------------------csv of county data---------------------------
    df = pd.read_csv(County_plant_data_dir)

    # Make names consistent -- normalize apostrophes to handle curly vs straight quotes
    gdf["NAME10"] = gdf["NAME10"].str.replace("'", "'")  # Replace curly apostrophe with straight
    df["County"] = df["County"].str.replace("'", "'")    # Replace curly apostrophe with straight

    # Remove Baltimore City (not a county) SOMEONE DEAL WITH THIS, get rid of tiny box in baltimore city
    gdf = gdf[gdf["NAME10"] != "Baltimore city"]
    df = df.drop(index=23).reset_index(drop=True)

    # ----------------------------Merge data onto county geometries---------------------------
    # since gdf has county names in "NAME10" and df has county names in "County", we merge on those columns
    gdf = gdf.merge(df, left_on="NAME10", right_on="County", how="left") 
    gdf[BIVAR_COLOR] = gdf.apply(get_bivariate_color, axis=1)
    return gdf