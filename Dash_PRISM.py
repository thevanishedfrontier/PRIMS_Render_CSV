#%%
## Author A. Moore
## This point of this program is to scrape publicly available information
## from the PRISM website, and compile it into a an interactive chloropleth map

import plotly.express as px
import pandas as pd
import json
import dash
from urllib.request import urlopen
from dash import dcc, html, Input, Output, dash_table

merged_data = pd.read_csv('Prism_dataframe.csv')


with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    json_counties = json.load(response)
## Creating the dash app
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Interactive Dashboard of PRISM clients by county"),

    ## Dropdown menu to toggle between decade, and nuber of programs
    html.Label("Select data to display:"),
    dcc.Dropdown(
        id="data-toggle",
        options=[
            {"label": "Decade", "value": "decade"},
            {"label": "Number of Programs", "value": "Number of Programs"}
        ],
        value="decade",  ## Default value
        clearable=False
    ),

    ## Graph to display the choropleth map
    dcc.Graph(
        id="choropleth-map",
        style={"width": "100vw", "height": "100vh"}
    )
])

## Callback to repopulate data when drop town is toggled
@app.callback(
    Output("choropleth-map", "figure"),
    [Input("data-toggle", "value")]
)
def update_map(selected_column):
    ## Change what information is displayed in hover data
    hover_data = {
        "Program Participation": selected_column == "Number of Programs",
        "fips_code": False  ## Exclude fips code from hover data
    }

    ## Generating the chloropleth map
    fig = px.choropleth(
        merged_data,
        geojson=json_counties,
        locations="fips_code",
        color=selected_column,
        scope="usa",
        hover_name="counties",
        hover_data=hover_data
    )

    ## Update bounds to exclude other states
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
    ## Set background to white
        plot_bgcolor="white",
        geo=dict(bgcolor="white")
    )


    return fig

## Run the dash app
if __name__ == "__main__":
    app.run_server(debug=True)
