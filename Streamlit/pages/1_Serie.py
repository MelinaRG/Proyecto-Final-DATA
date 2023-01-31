import streamlit as st
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import plotly.graph_objects as go
from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
from prophet.serialize import model_to_json, model_from_json

st.title('Serie de tiempo - Ventas diarias :chart_with_upwards_trend:')
st.title('Forecasting :chart:')

# DATABASE #


@st.experimental_singleton
def init_connection():
    return psycopg2.connect("host='datapfpostgres.postgres.database.azure.com' port='5432' dbname='postgres' user='meli@datapfpostgres' password='hola123#'")
# 'postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist'


@st.experimental_memo(ttl=600)
def get_df_transformed():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    results = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    orders = pd.DataFrame(results, columns=column_names)
    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"], format="%Y-%m-%d %H:%M:%S")
    orders['total_order_cost'] = orders['total_order_cost'].astype('float')

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


conn = init_connection()
df_d = get_df_transformed()
conn.close()

st.table(df_d)

# CARGA DEL MODELO #

with open('serialized_model.json', 'r') as fin:
    m = model_from_json(fin.read())
