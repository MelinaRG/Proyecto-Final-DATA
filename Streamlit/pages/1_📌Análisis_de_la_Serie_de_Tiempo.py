import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import psycopg2
import sqlite3 as sql
import plotly.graph_objects as go
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
from prophet.serialize import model_to_json, model_from_json
from PIL import Image
import os
import time


# DATABASE CALL #

@st.experimental_singleton(show_spinner=False)
def init_connection():
    """Initialize connection to database

    Returns:
        connection to postgres sql database
    """
    # Engine con las credenciales
    # return connection
    return psycopg2.connect(**st.secrets["postgres"])


with st.spinner('Conectando a la base de datos'):
    # DATABASE CONNECTION #
    conn = init_connection()


@st.experimental_memo(ttl=600, show_spinner=False)
def get_df_transformed():
    """Bring and transform a table from database and convert to dataframe

    Returns:
        DataFrame: daily orders
    """
    #orders = pd.read_sql_table('orders', conn)
    # orders["order_purchase_timestamp"] = pd.to_datetime(
    # orders["order_purchase_timestamp"], format="%Y-%m-%d %H:%M:%S")
    #orders['total_order_cost'] = orders['total_order_cost'].astype('float')
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
    return df_d


# ISOLOGO #
logo_path_racont = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "../assets/isologo.png")
logo_racont = Image.open(logo_path_racont)
logo_path_olist = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "../assets/logo_olist.png")
logo_olist = Image.open(logo_path_olist)

# CARGA DEL MODELO #
model_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "../forecast_olis.json")
model = model_from_json(open(model_path, 'r').read())

# PREDICCION #


def predicción(df_fechas):
    df_pred = model.predict(df_fechas)
    return df_pred

# PLOTEO #


def main():
    # TITULO
    st.title('Análisis de la Serie de tiempo - Ventas de Olist :bar_chart:')
    st.markdown('---')
    # SIDEBAR
    with st.sidebar:
        st.subheader('For our client:')
        st.image(logo_olist, width=60)
        st.subheader('Made with :heart: by:')
        st.image(logo_racont, width=90)
    # CARGA DEL DATAFRAME
    with st.spinner('Extrayendo datos...'):
        # DATABASE CONNECTION #
        df_d = get_df_transformed()
        conn.close()
    st.success('Datos cargados exitosamente!')
    # INTRODUCCIÓN
    st.subheader('Componentes de Tendencia y Estacionales')
    st.markdown(""" Es importante analizar y entender la evolución y el comportamiento de 
                los datos reales de venta a lo largo del tiempo. Por eso se presentan los componentes
                de la serie a partir de la predicción correspondiente.""")
    st.markdown(
        """ * **Estacionalidad:** periodos de tiempo con una oscilación en los valores de la variable """)
    st.markdown(
        """ * **Tendencia:** periodos de tiempo con una oscilación en los valores de la variable """)

    # PLOTEO TIMESERIES
    df_d = df_d.reset_index()
    ds = df_d[['ds']]
    df_pred = model.predict(ds)
    plot_pred = plot_plotly(model, df_pred)
    plot_comp = plot_components_plotly(model, df_pred)

    st.subheader('Ploteo Predicción')
    st.plotly_chart(plot_pred, sharing="streamlit", theme="streamlit")
    st.subheader('Ploteo Componentes')
    st.plotly_chart(plot_comp, sharing="streamlit", theme="streamlit")


if __name__ == "__main__":
    main()
