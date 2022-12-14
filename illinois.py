import dash
import json
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from urllib.request import urlopen

app = dash.Dash(
    __name__,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0, maximum-scale=2.5, minimum-scale=1.0"
        }
    ],

    external_stylesheets=[
        'https://codepen.io/chriddyp/pen/bWLwgP.css'
    ],

    external_scripts=[],
    suppress_callback_exceptions=True
)

app.title = 'IL COVID-19'

with urlopen('https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/illinois-counties.geojson') as response:
    counties = json.load(response)

# Search through dataset
county_id_map = {}
for feature in counties['features']:
    feature['id'] = feature['properties']['co_fips']
    county_id_map[feature['properties']['name']] = feature['id']

df = pd.read_csv("illinoisData.csv")
df['id'] = df['County'].apply(lambda x: county_id_map[x])

### Build a figure for dataset
fig = px.choropleth(df, geojson=counties, locations='id', color='Total Cases', scope="usa", color_continuous_scale="YlOrRd", hover_name='County')
fig.update_geos(fitbounds='locations', visible=False)
fig.show()

app.layout = html.Div([
        html.H1("Total COVID-19 Cases by Illinois County",
            style = {
                'textAlign': 'center'
            }),

        html.Div("Data Last Updated: 10/11/2022",
        style = {
                'textAlign': 'center'
            }),

        dcc.Graph(id='graph', figure=fig, responsive=True,
        style = {
                'height' : '80vh',
            }),
])

if __name__ == "__main__":
    app.run_server(host='0.0.0.0')