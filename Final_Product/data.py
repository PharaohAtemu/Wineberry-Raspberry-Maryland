import pandas as pd
import geopandas as gpd




def load_data(PLANT1, PLANT2, gdf_raw, plant1_df, plant2_df):

    #plant1_df = plant1_df.drop(columns=["Unnamed: 0"], errors="ignore")
    plant1_df = plant1_df.drop(columns=["Unnamed: 0"], errors="ignore")
    plant1_long = plant1_df.melt( # will look back into, seems to be redudent with what I already have
        id_vars="County",
        var_name="Year",
        value_name=PLANT1
    )
    plant1_long["Year"] = plant1_long["Year"].astype(int)

    #plant2_df = plant2_df.drop(columns=["Unnamed: 0"], errors="ignore")
    plant2_df = plant2_df.drop(columns=["Unnamed: 0"], errors="ignore")
    plant2_long = plant2_df.melt(
        id_vars="County",
        var_name="Year",
        value_name=PLANT2
    )
    plant2_long["Year"] = plant2_long["Year"].astype(int)


    #merge plant1 and plant2 dataframes on County and Year
    plant_data = plant1_long.merge(
        plant2_long,
        on=["County", "Year"],
        how="outer"
    ).fillna(0)


    #merge with geodata

    
    #merge with geodata
    gdf_raw = gdf_raw.copy()
    gdf_raw["County_merge_key"] = gdf_raw["NAME10"]
    gdf_raw.loc[
        gdf_raw["NAMELSAD10"] == "Baltimore city",
        "County_merge_key"
    ] = "Baltimore city"
    
    gdf = gdf_raw.merge(
        plant_data,
        left_on="County_merge_key",
        right_on="County",
        how="left"
    )

    yearly = (
        gdf.groupby("Year")[[PLANT1, PLANT2]]
        .sum()
        .reset_index()
        .sort_values("Year")
    )

    # Exclude Baltimore city from the map
    gdf = gdf[gdf["County_merge_key"] != "Baltimore city"]
    return gdf, yearly
