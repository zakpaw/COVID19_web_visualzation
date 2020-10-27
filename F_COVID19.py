from datetime import datetime
import streamlit as st
import plotly.express as px
import pandas as pd


st.write('<h1 style="text-align:center">F COVID-19</h1>', 
         unsafe_allow_html=True)         


@st.cache
def preper_data():
    URL = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/data.csv'
    df = pd.read_csv(URL, parse_dates=['dateRep'], index_col='dateRep')
    df = df[df.index <= datetime.today().strftime('%Y-%m-%d')]

    to_drop = ['day', 'month', 'year', 'geoId', 'continentExp',
               'Cumulative_number_for_14_days_of_COVID-19_cases_per_100000']
    df.drop(to_drop, axis=1, inplace=True)

    df.columns = ['cases', 'deaths', 'country', 'country_code', 'population']
    df.sort_index(inplace=True)

    df['death % of population'] = df.deaths*100/df.population
    df['infected % of population'] = df.cases*100/df.population
    return df


df = preper_data()

countries = st.multiselect('Choose countriess',
                           sorted(df.country.unique()), ['Poland'])

features = [c for c in df.columns if c not in ['country', 'country_code']]
feature = st.selectbox('Choose feature', features, 1)
if not countries:
    st.error('Please select at least one country.')
else:
    data = df[df.country.isin(countries)]
    fig = px.line(data,
                  x=data.index.values,
                  y=feature,
                  color='country',
                  hover_name='country_code',
                  labels={'x': ''})

    st.write('<h3 style="text-align:center"> {}: {}</h3>'
             .format(feature.strip('_').title(),
                     ' vs '.join([i.replace('_', ' ') for i in countries])),
             unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)

st.write("""
         <h4 style="text-align:center">
         <a href="https://opendata.ecdc.europa.eu/covid19">Source of data</a>
         </h4>
         """, unsafe_allow_html=True)
