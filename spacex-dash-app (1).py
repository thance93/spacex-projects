# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# List of launch sites
launch_sites = spacex_df["Launch Site"].unique().tolist()

options = [{"label": "ALL", "value": "ALL"}] + [{"label": site, "value": site} for site in launch_sites]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div([
    html.H1(
        "SpaceX Launch Records Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),

    # Dropdown
    dcc.Dropdown(
        id="site-dropdown",
        options=options,
        value="ALL",
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    # Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # Range slider
    dcc.RangeSlider(
        id="payload-slider",
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],
        marks={
            0: "0",
            2500: "2.5K",
            5000: "5k",
            7500: "7.5K",
            10000: "10k"
        },
        tooltip={"placement": "bottom", "always_visible": True}
    ),

    html.Br(),

    # Scatter plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback (Pie Chart)
@app.callback(
    Output("success-pie-chart", "figure"),
    Input("site-dropdown", "value")
)
def update_pie_chart(selected_site):

    if selected_site == "ALL":
        fig = px.pie(
            spacex_df,
            names="Launch Site",
            values="class",
            title="Total Successful Launches for All Sites"
        )
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == selected_site]
        fig = px.pie(
            filtered_df,
            names="class",
            title=f"Success vs Failure for Site: {selected_site}"
        )

    return fig

@app.callback(
    Output("success-payload-scatter-chart", "figure"),
        [Input("site-dropdown", "value"),
        Input("payload-slider", "value")]
)
def update_scatter_plot(selected_site, payload_range):

    low, high = payload_range

    filtered_df = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= low) &
        (spacex_df["Payload Mass (kg)"] <= high)
    ]

    if selected_site != "ALL":
        filtered_df = filtered_df[filtered_df["Launch Site"] == selected_site]

    fig = px.scatter(
        filtered_df,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        title="Payload vs. Launch Outcome",
        hover_data=["Launch Site", "Payload Mass (kg)", "class"]
    )

    return fig

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# Run the app
if __name__ == '__main__':
    app.run()
