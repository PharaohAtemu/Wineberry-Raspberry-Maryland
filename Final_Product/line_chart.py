
import plotly.graph_objects as go
#plant1 and plant2 are the names of the plants
def create_line_chart(yearly, PLANT1, PLANT2, LINE_GRAPH_TITLE, LINE_GRAPH_X, LINE_GRAPH_Y):
    line_fig = go.Figure()

    line_fig.add_trace(go.Scatter(
        x=yearly["Year"],
        y=yearly[PLANT1],
        mode="lines+markers",
        name=PLANT1
    ))

    line_fig.add_trace(go.Scatter(
        x=yearly["Year"],
        y=yearly[PLANT2],
        mode="lines+markers",
        name=PLANT2
    ))

    line_fig.update_layout(
        title=LINE_GRAPH_TITLE,
        xaxis_title=LINE_GRAPH_X,
        yaxis_title=LINE_GRAPH_Y,
        template="plotly_white"
    )

    return line_fig