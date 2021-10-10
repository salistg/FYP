import urllib

import pandas as pd
from datetime import date
from datetime import timedelta
import plotly.express as px
import requests as requests
import malaysia_states as ms
import json
from urllib.request import urlopen


def clean_and_save_timeseries(df):
    drop_columns = ['Lat',
                    'Long',
                    'Province/State']

    df.drop(columns=drop_columns, inplace=True)

    df_grouped = df.groupby(['Country/Region'], as_index=False).sum()
    df_grouped = df_grouped.set_index('Country/Region').transpose()
    df_grouped.reset_index(level=0, inplace=True)
    df_grouped.rename(columns={'index': 'Date'}, inplace=True)
    df_grouped['Date'] = pd.to_datetime(df_grouped['Date'])

    return df_grouped


def clean_and_save_worldwide(df):
    drop_columns = ['FIPS',
                    'Lat',
                    'Long_',
                    'Combined_Key',
                    'Admin2',
                    'Province_State']

    df.drop(columns=drop_columns, inplace=True)

    df_cases = df.groupby(['Country_Region'], as_index=False).sum()

    return df_cases


# line chart of the development of infections over time


def get_msia_lineplot(df):
    fig_ts = px.line(data_frame=df,
                     x="Date",
                     y="Malaysia")

    fig_ts.update_layout(xaxis_type='date',
                         xaxis={
                             'title': 'Date'
                         },
                         yaxis={
                             'title': 'Confirmed Cases',
                             'type': 'linear',
                         },
                         title_text='Covid-19 Cases in Malaysia')

    return fig_ts


# a simple horizontal bar chart for cases per state


def get_msia_barchart(df):
    # mdf.sort_values(by=['cases_new'], ascending=True, inplace=True)

    fig_fs = px.bar(data_frame=df,
                    x='cases_new',
                    y='state',
                    hover_data=['cases_new'],
                    height=600,
                    orientation='h',
                    labels={'cases_new': 'Total cases'},
                    template='ggplot2')

    fig_fs.update_layout(xaxis={
        'title': 'Number of cases'
    },
        yaxis={
            'title': 'State',
        },
        title_text='Covid-19 Cases Per State in Malaysia')

    return fig_fs


# creating a pie chart for cases per state


def get_msia_piechart(df):
    fig_fs_pie = px.pie(data_frame=df,
                        values='cases_new',
                        names='state',
                        title='Distribution of Cases Per State',
                        template='ggplot2')
    return fig_fs_pie


# a world map with the distribution of cases per country (scatter plot)


def get_ww_scatter(df):
    fig_geo_ww = px.scatter_geo(data_frame=df,
                                locations="Country_Region",
                                hover_name="Country_Region",
                                hover_data=['Confirmed', 'Recovered', 'Deaths'],
                                size="Confirmed",
                                locationmode='country names',
                                text='Country_Region',
                                scope='world',
                                labels={
                                    'Country_Region': 'Country',
                                    'Confirmed': 'Confirmed Cases',
                                    'Recovered': 'Recovered Cases',
                                    'Deaths': 'Deaths',
                                },
                                projection="equirectangular",
                                size_max=35,
                                template='ggplot2', )

    fig_geo_ww.update_layout(
        title_text='Covid-19 Confirmed Cases Around the World',
        title_x=0.5,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        )
    )

    return fig_geo_ww


# choropleth of all countries

def get_ww_chloropleth(df):
    fig_chloro_ww = px.choropleth(data_frame=df,
                                  locations="Country_Region",
                                  hover_data=['Confirmed', 'Recovered', 'Deaths'],
                                  locationmode='country names',
                                  scope='world',
                                  labels={
                                      'Country_Region': 'Country',
                                      'Confirmed': 'Confirmed Cases',
                                      'Recovered': 'Recovered Cases',
                                      'Deaths': 'Confirmed Deaths',
                                  },
                                  color='Confirmed',
                                  color_continuous_scale='sunset',
                                  # projection="mercator"
                                  )

    fig_chloro_ww.update_layout(title_text='',
                                title_x=0.5,
                                coloraxis_reversescale=False,
                                autosize=False,
                                margin=dict(
                                    l=0,
                                    r=0,
                                    b=0,
                                    t=0,
                                    pad=4,
                                    autoexpand=True
                                ),
                                width=1400,
                                #     height=400,
                                )

    # countries_map = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    # with urlopen('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json') as response:
    #     countries = json.load(response)

    # def read_geojson(url):
    #     with urllib.request.urlopen(url) as url:
    #         jdata = json.loads(url.read().decode())
    #     return jdata
    #
    # countries_map = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    # jdata = read_geojson(countries_map)
    #
    # fig = px.choropleth_mapbox(df,
    #                            geojson=jdata,
    #                            featureidkey='properties.name',
    #                            locations='Country_Region',
    #                            color='Confirmed',
    #                            color_continuous_scale='burg_r',
    #                            # zoom=6.5,
    #                            # center={'lat': 4.2105, 'lon': 101.9758},
    #                            mapbox_style='carto-positron')
    #
    # fig.update_layout(title_text='',
    #                   title_x=0.5,
    #                   coloraxis_reversescale=True)

    return fig_chloro_ww
    # return fig


def get_world_data(df):
    total_cases = df['Confirmed'].sum()
    total_deaths = df['Deaths'].sum()
    total_recoveries = df['Recovered'].sum()
    total_active = df['Active'].sum()

    data = {'Cases': total_cases,
            'Deaths': total_deaths,
            'Recoveries': total_recoveries,
            'Active': total_active}

    return data


def get_country_names(df):
    list_of_countries = df['Country_Region']

    return list_of_countries
