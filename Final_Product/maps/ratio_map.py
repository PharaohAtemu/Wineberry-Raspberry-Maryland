import folium
import geopandas as gpd

def create_ratio_map(gdf, Selected_Years_list, PLANT1, PLANT2):
    # modifying data DON'T CHANGE
    # Creates a data frame just like the regular one, except its for just x years
    # ------------------------------------------------------
    year_gdf = gdf[gdf["Year"].isin(Selected_Years_list)]
    agg_gdf = (
        year_gdf
        .groupby("NAME10", as_index=False)
        .agg({
            PLANT1: "sum",
            PLANT2: "sum",
            "geometry": "first"
        })
    )
    agg_gdf["ratio"] = agg_gdf[PLANT1] / agg_gdf[PLANT2]
    agg_gdf["ratio"] = agg_gdf["ratio"].fillna(0)
    agg_gdf["ratio"] = agg_gdf["ratio"].replace([float("inf"), -float("inf")], 0)
    agg_gdf = gpd.GeoDataFrame(agg_gdf, geometry="geometry", crs=gdf.crs)
    # ------------------------------------------------------
    m = folium.Map(
        location=[39.0, -76.7],
        zoom_start=7,
        tiles="cartodbpositron"
    )

    folium.Choropleth(
        geo_data=agg_gdf,
        data=agg_gdf,
        columns=["NAME10", "ratio"],
        key_on="feature.properties.NAME10",
        fill_color= "RdBu",
        fill_opacity=0.75,
        line_opacity=0.4
        #legend_name=f"{PLANT1} / {PLANT2} Ratio in {year}"
    ).add_to(m)

    folium.GeoJson(
        agg_gdf,
        tooltip=folium.GeoJsonTooltip(
            fields=["NAME10", PLANT1, PLANT2, "ratio"],
            aliases=["County:", f"{PLANT1}:", f"{PLANT2}:", "Ratio:"],
            localize=True
        ),
        style_function=lambda feature: {
            "fillColor": "transparent",
            "color": "black",
            "weight": 1,
            "fillOpacity": 0
        }
    ).add_to(m)

    return m._repr_html_()