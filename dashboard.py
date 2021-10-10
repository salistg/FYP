from datetime import timedelta, date

import dash

import dash_core_components as dcc
import dash_html_components as html
import requests
from dash.dependencies import Input, Output

# Module with help functions
import world as graphs

import pandas as pd

time_series = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
              "/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv "
csv_file = pd.read_csv(time_series)

df_ww = graphs.clean_and_save_timeseries(csv_file)

today = date.today()
yesterday = today - timedelta(days=1)
before_yesterday = today - timedelta(days=2)
tdate = today.strftime("%m-%d-%Y")
ydate = yesterday.strftime("%m-%d-%Y")
bfrydate = before_yesterday.strftime("%m-%d-%Y")

#dates in malaysia format according to MOH
tdate_m = today.strftime("%Y-%m-%d")
ydate_m = yesterday.strftime("%Y-%m-%d")

# print("Today's date:", tdate)
# print("Yesterday's date:", ydate)
# print("Today's date (MSIA Format):", tdate_m)
# print("Yesterday's date (MSIA Format):", ydate_m)

daily_cases_today = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                    "/csse_covid_19_daily_reports/" + tdate + ".csv "
daily_cases_yday = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                   "/csse_covid_19_daily_reports/" + ydate + ".csv "
daily_cases_bfryday = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                   "/csse_covid_19_daily_reports/" + bfrydate + ".csv "
# print(daily_cases_yday)

if requests.get(daily_cases_today):
    dcf = pd.read_csv(daily_cases_today)
elif requests.get(daily_cases_yday):
    dcf = pd.read_csv(daily_cases_yday)
else:
    dcf = pd.read_csv(daily_cases_bfryday)

df_total = graphs.clean_and_save_worldwide(dcf)

msia_state_cases = "https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_state.csv"
mdf = pd.read_csv(msia_state_cases)

if (mdf['date'] == tdate_m).any():
    mdf = mdf.loc[mdf['date'] == tdate_m]
else:
    mdf = mdf.loc[mdf['date'] == ydate_m]

df_msia = mdf
df_msia.sort_values(by=['cases_new'], ascending=True, inplace=True)

# df_ww = pd.read_csv('data/worldwide_timeseries.csv')
# df_total = pd.read_csv('data/total_cases_worldwide.csv')
# df_msia = pd.read_csv('data/total_cases_malaysia.csv')

fig_geo_ww = graphs.get_ww_scatter(df_total)
fig_msia_bar = graphs.get_msia_barchart(df_msia)
fig_msia_pie = graphs.get_msia_piechart(df_msia)
fig_msia_line = graphs.get_msia_lineplot(df_ww)
fig_choro_ww = graphs.get_ww_chloropleth(df_total)

ww_facts = graphs.get_world_data(df_total)

fact_string = '''There are a total of {} cases worldwide.
  Of these, {} people have passed away and {} are recovered.
  Thus, officially {} people are actively suffering from COVID-19.'''

fact_string = fact_string.format(ww_facts.get('Cases'),
                                 ww_facts.get('Deaths'),
                                 ww_facts.get('Recoveries'),
                                 ww_facts.get('Active'))

countries = graphs.get_country_names(df_total)

dd_options = []
for key in countries:
    dd_options.append({
        'label': key,
        'value': key
    })

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='COVID-19 Dashboard', style={'textAlign': 'center'}),
    html.H2(children='Worldwide Distribution of COVID-19 Cases', style={'textAlign': 'center'}),

    # World and Facts
    # html.Div(children=[

    html.Div(children=[

        dcc.Graph(figure=fig_choro_ww),

    ], style={'display': 'flex',
              'flexDirection': 'column',
              'width': '100%'}),

    # html.Div(children=[
    #
    #     html.H3(children='Numbers'),
    #     html.P(children=fact_string)
    #
    # ], style={'display': 'flex',
    #           'flexDirection': 'column',
    #           'width': '33%'})

    # ], style={'display': 'flex',
    #           'flexDirection': 'row',
    #           'flexwrap': 'wrap',
    #           'width': '100%'}),

    # Combobox and Checkbox
    html.Div(children=[
        html.Div(children=[
            # combobox
            dcc.Dropdown(
                id='countries_dropdown',
                options=dd_options,
                value=['Malaysia'],
                multi=True
            ),

        ], style={'display': 'flex',
                  'flexDirection': 'column',
                  'width': '66%'}),

        html.Div(children=[
            # Radio-Buttons
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            ),

        ], style={'display': 'flex',
                  'flexDirection': 'column',
                  'width': '33%'})
    ], style={'display': 'flex',
              'flexDirection': 'row',
              'flexwrap': 'wrap',
              'width': '100%'}),

    # Lineplot and Facts
    html.Div(children=[
        html.Div(children=[

            # Line plot: Infections
            dcc.Graph(figure=fig_msia_line, id='infections_line'),

        ], style={'display': 'flex',
                  'flexDirection': 'column',
                  'width': '100%'}),

    ], style={'display': 'flex',
              'flexDirection': 'row',
              'flexwrap': 'wrap',
              'width': '100%'}),

    # Malaysia
    html.H2(children='Numbers of Malaysia', style={'textAlign': 'center'}),

    html.Div(children=[
        html.Div(children=[

            # Barchart Malaysia
            dcc.Graph(figure=fig_msia_bar),

        ], style={'display': 'flex',
                  'flexDirection': 'column',
                  'width': '50%'}),

        html.Div(children=[

            # Pie Chart Malaysia
            dcc.Graph(figure=fig_msia_pie),

        ], style={'display': 'flex',
                  'flexDirection': 'column',
                  'width': '50%'})
    ], style={'display': 'flex',
              'flexDirection': 'row',
              'flexwrap': 'wrap',
              'width': '100%'})
])


# Interactive Line Chart
@app.callback(
    Output('infections_line', 'figure'),
    [Input('countries_dropdown', 'value'), Input('yaxis-type', 'value')])
def update_graph(countries, axis_type):
    countries = countries if len(countries) > 0 else ['Malaysia']
    data_value = []
    for country in countries:
        data_value.append(dict(
            x=df_ww['Date'],
            y=df_ww[country],
            type='lines',
            name=str(country)
        ))

    title = ', '.join(countries)
    title = 'COVID-19 Cases: ' + title
    return {
        'data': data_value,
        'layout': dict(
            yaxis={
                'type': 'linear' if axis_type == 'Linear' else 'log'
            },
            hovermode='closest',
            title=title
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
