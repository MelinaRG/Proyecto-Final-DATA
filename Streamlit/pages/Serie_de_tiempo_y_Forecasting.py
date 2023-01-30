import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
""" import plotly.graph_objects as go
from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
from prophet.serialize import model_to_json, model_from_json """


st.title('Serie de tiempo - Ventas diarias :chart_with_upwards_trend:')

st.title('Forecasting :chart:')

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    # Engine con las credenciales
    engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')
    orders = pd.read_sql_table('orders', engine)
    # Cerrar la conexión
    engine.dispose()
    
    #Trasformaciones
    orders.dropna(subset=['total_order_cost'], inplace = True)
    df_ts = orders[orders['order_status'].isin(['delivered','shipped','invoiced'])]
    df_ts = df_ts[['order_purchase_timestamp','total_order_cost']]
    df_ts.rename(columns={'order_purchase_timestamp':'ds','total_order_cost':'y'}, inplace=True)
    df_ts.sort_values(by=['ds'], inplace=True, ignore_index=True)
    df_ts.set_index('ds', inplace = True)
    df_d = df_ts.resample('D').sum()
    df_d[df_d['y']==0] = np.nan
    df_d = df_d.interpolate()
    df_d = df_d.loc['2017-01-01':'2018-08-31']
    
    return df_d

df_d = init_connection()

st.header('Serie de tiempo - Datos reales')
st.area_chart(df_d, x=df_d.index, y = df_d['y'])

