import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import psycopg2
import sqlite3 as sql
import plotly.graph_objects as go
from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
from prophet.serialize import model_to_json, model_from_json


st.title('Serie de tiempo - Ventas diarias :chart_with_upwards_trend:')

st.title('Forecasting :chart:')

# Initialize connection.
# Uses st.experimental_singleton to only run once.


@st.experimental_singleton(show_spinner=True)
def init_connection():
    # Engine con las credenciales
    engine = create_engine(
        'postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')
    connection = engine.connect()
    return connection


@st.experimental_memo(ttl=600)
def get_df_transformed(_conn):
    # Extraigo el dataframe orders
    db_conn = _conn.connection
    cursor = db_conn.cursor()
    query = 'SELECT * FROM orders'
    cursor.execute(query)
    results = cursor.fetchall()
    # Traigo los columns names de cursor.description
    column_names = [column[0] for column in cursor.description]
    orders = pd.DataFrame(results, columns=column_names,
                          dtype={'total_order_cost': 'float'})
    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"], format="%Y-%m-%d %H:%M:%S")

    # Trasformaciones
    orders.dropna(subset=['total_order_cost'], inplace=True)
    df_ts = orders[orders['order_status'].isin(
        ['delivered', 'shipped', 'invoiced'])]
    df_ts = df_ts[['order_purchase_timestamp', 'total_order_cost']]
    df_ts.rename(columns={'order_purchase_timestamp': 'ds',
                 'total_order_cost': 'y'}, inplace=True)
    df_ts.sort_values(by=['ds'], inplace=True, ignore_index=True)
    df_ts.set_index('ds', inplace=True)
    df_d = df_ts.resample('D').sum()
    df_d[df_d['y'] == 0] = np.nan
    df_d = df_d.interpolate()
    df_d = df_d.loc['2017-01-01':'2018-08-31']

    # Cierre de conexiones
    cursor.close()
    return df_d


connection = init_connection()
df_d = get_df_transformed(connection)

connection.close()

st.header('Serie de tiempo - Datos reales')
st.area_chart(df_d, x=df_d.index, y=df_d['y'])
