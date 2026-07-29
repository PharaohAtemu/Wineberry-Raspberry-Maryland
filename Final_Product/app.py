from dash import Dash, html, dcc, Input, Output
from dash import callback_context
import pandas as pd
import geopandas as gpd
from maps.bivariate_CMAP_1 import create_bivariate_map
from maps.ratio_map import create_ratio_map
from line_chart import create_line_chart
from data import load_data
from load_biData import load_biData
import dash_bootstrap_components as dbc

PLANT1 = "Black Raspberry" #Black Raspberry
PLANT2 = "Wineberry" #Wineberry
County_data_dir = "Final_Product/Plant_County_data/maryland_counties.geojson"
Black_Rasp_dir = "Final_Product/Plant_County_data/Black_Raspberry_County_Year_data_cleaned.csv"
WineBerry_dir = "Final_Product/Plant_County_data/Wineberry_County_Year_data.csv"
#County_plant_data_dir = "Final_Product/Plant_County_data/County_Data.csv"


TITLE = "Comparing Black Raspberry and Wineberry Observations in Maryland (2016-2026)"
LINE_GRAPH_TITLE = "Black Raspberry and Wineberry Observations in Maryland (2016-2026)"
LINE_GRAPH_X = "Year"
LINE_GRAPH_Y = "Observations"
#YEARS_SELECTED_TITLE = "" inside of make_selected_year_title()
BIVARITE_TITLE = f"Bivariate Map: [{PLANT2}, {PLANT1}]"
RATIO_TITLE = f"Ratio Map: {PLANT1} / {PLANT2}"

# ---------- Load data ----------
gdf, yearly = load_data(PLANT1, PLANT2, gdf_raw = gpd.read_file(County_data_dir), plant1_df = pd.read_csv(Black_Rasp_dir), plant2_df = pd.read_csv(WineBerry_dir))
Bigdf = load_biData()
default_year = int(gdf["Year"].max())
Selected_Years_list = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]

# ---------- Dash app layout----------
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Button("What is this Tool?", id= "open-help"),
    
    dbc.Modal([
            dbc.ModalHeader(
                dbc.ModalTitle("How To Use This Dashboard"),
                close_button=True
            ),

            dbc.ModalBody([
                html.P("Black Raspberry, Rubus occidentalis, is a berry-producing plant native to Maryland. Wineberry, Rubus phoenicolasius, is a berry-producing plant introduced to North America and considered invasive in Maryland. This dashboard was built for the purpose of comparing iNaturalist observations of these two plants across Maryland counties from 2016 to the beginning of 2026."),
                html.P("Comparisons are done through three different charts."),
                html.P("The line chart atop compares all of Maryland observations of each plant by year. Clicking on the legend to the right allows observation of one plant at a time. Hovering over the dots will show the number of observations for that plant in that year."),
                html.P("The bivariate map on the bottom left shows the combined rank of both plants in each county for all 10 years. Data is normalized by area, to account for availability of plant space, and population, to account for number of opportunities for the plant to be spotted. Darker colors indicate higher observations and lighter colors indicate fewer. The dark red implies high observations of each plant. This graph allows visualization of distribution and abundance of both plants across counties."),
                html.P("The ratio map on the bottom right shows the ratio of observations for Black Raspberry to Wineberry in each county. Bluer colors indicate a higher ratio of Black Raspberry to Wineberry, while redder colors indicate a lower ratio. This allows visualization of the relative abundance of the two plants in each county. "),
                html.P("Hovering over the counties in either map will show the county name and the number of observations for each plant in that county. The maps are interactive, so you can zoom in and out to see more or less detail. Additionally, hovering over the titles of each map will show a tooltip that explains how to interpret the colors on the map. The line chart and maps are all interactive, so you can explore the data in different ways to gain insights into the distribution and abundance of these two plants across Maryland.")
            ]),

            dbc.ModalFooter(
                dbc.Button("Close", id="close-help")
            ),
        ],
        id="help-modal",
        is_open=True,
        size="lg",
        backdrop=True,
        keyboard=True
    ),

    html.H2(TITLE),

    dcc.Graph(
        id="plant-line-chart",
        figure=create_line_chart(yearly, PLANT1, PLANT2, LINE_GRAPH_TITLE, LINE_GRAPH_X, LINE_GRAPH_Y)
    ),
    html.Div([
        html.Div([
            html.H4(BIVARITE_TITLE, id="bivariate-title", style={"color": "darkblue"}),
            html.Iframe(
                id="bivariate-map",
                srcDoc=create_bivariate_map(Bigdf),
                width="100%",
                height="600",
                style={"border": "none"}
            )
        ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),

        html.Div([
            html.H4(RATIO_TITLE, id="ratio-title",  style={"color": "darkblue"}),
            html.Iframe(
                id="ratio-map",
                srcDoc=create_ratio_map(gdf, Selected_Years_list, PLANT1, PLANT2),
                width="100%",
                height="600",
                style={"border": "none"}
                )
            ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"})
    ], style={"width": "100%"})
])

#tooltip for bivarate
tooltip = dbc.Tooltip(
        "This map shows the bivariate relationship between the two plants across Maryland counties. The color of each county represents the combined rank of both plants, normalized by population and area. Darker colors indicate higher ranks for both plants, while lighter colors indicate lower ranks. This allows visual comparison of the distribution and abundance of both plants across counties.",
        target="bivariate-title",
        placement="right"
)

#tooltip for ratio
tooltip2 = dbc.Tooltip(
    f"This map shows the ratio of the observations for the two plants across Maryland counties. The color of each county represents the ratio of {PLANT1} to {PLANT2}. Bluer colors indicate a higher ratio of {PLANT1} to {PLANT2}, while redder colors indicate a lower ratio. This allows visual comparison of the relative abundance of the two plants in each county.",
    target="ratio-title",
    placement="right"
)

@app.callback(
    Output("help-modal", "is_open"),
    [Input("open-help", "n_clicks"), Input("close-help", "n_clicks")],
    [Input("help-modal", "is_open")]
)
def toggle_help_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open

app.layout.children.extend([tooltip, tooltip2])


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=8051)
