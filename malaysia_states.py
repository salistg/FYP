import json
import urllib.request

import pandas as pd
import plotly.express as px  # (version 4.7.0)

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ---------- Import and clean data (importing csv into pandas)

header_list = ["state", "year"]
df = pd.read_csv("https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_state.csv",
                 sep=r'\s*,\s*',
                 encoding='ascii', engine='python', index_col=False)

# extracting the year and month from the dates
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# grouping data by state and year, shows the total number of cases for each state by year
df = df.groupby(['state', 'year'])[['cases_new']].sum()
df.reset_index(inplace=True)
df.reset_index(drop=True)
# print(df[:5])

# ------------------------------------------------------------------------------
# App layout
# what goes here is: dash components (graphs, dropdowns, checkboxes) and any HTML needed
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="select_year",
                 options=[
                     {"label": "2020", "value": 2020},
                     {"label": "2021", "value": 2021}],
                 multi=False,
                 value=2020,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='cases_map', figure={})

])


# inside figure -> chloropleth
# value should match what it looks like in the csv file

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='cases_map', component_property='figure')],
    [Input(component_id='select_year', component_property='value')]
)
# have to put this function after every callback
# each input connects to an argument
# we have one input (select_year) so we will only have one argument
# if we have more input, then we'll have more agruments
# the argument refers to the component_property (here in this case, option_slctd is the value of the year)
def update_graph(option_selected):
    # print(option_selected)
    # print(type(option_selected))

    container = "The year chosen by user was: {}".format(option_selected)

    # filtering the data
    # making a copy of it so that the data itself is not altered
    dff = df.copy()
    # only take rows of the year the user selected
    # dff = dff[dff['date'].dt.year == option_selected]
    dff = dff[dff['year'] == option_selected]
    # to only show the cases_new data
    # dff = dff[{'state', 'cases_new'}]
    print(dff[:5])

    # Plotly Express

    def read_geojson(url):
        with urllib.request.urlopen(url) as url:
            jdata = json.loads(url.read().decode())
        return jdata

    state_map = "https://raw.githubusercontent.com/salistg/administrative_malaysia_state_province_boundary/main" \
                "/malaysia_singapore_brunei_administrative_malaysia_state_province_boundary.geojson "
    jdata = read_geojson(state_map)

    fig = px.choropleth_mapbox(dff,
                               geojson=jdata,
                               featureidkey='properties.locname',
                               locations='state',
                               color='cases_new',
                               color_continuous_scale='burg_r',
                               zoom=6.5,
                               center={'lat': 4.2105, 'lon': 101.9758},
                               mapbox_style='carto-positron')

    fig.update_layout(title_text='',
                      title_x=0.5,
                      coloraxis_reversescale=True)

    # the number of returns depends on the number of outputs specified in the app callback
    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
