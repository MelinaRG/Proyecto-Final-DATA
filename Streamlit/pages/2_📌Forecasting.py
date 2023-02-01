import base64
import streamlit as st
import os
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import plotly.graph_objects as go
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
from prophet.serialize import model_to_json, model_from_json
from datetime import datetime, timedelta
from PIL import Image
import time
import os


# DATABASE #

@st.experimental_singleton
def init_connection():
    """Initialize connection to database

    Returns:
        connection to postgres sql database
    """
    # return psycopg2.connect("host='datapfpostgres.postgres.database.azure.com' port='5432' dbname='postgres' user='meli@datapfpostgres' password='hola123#'")

    return psycopg2.connect("host='dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com' port='5432' dbname='olist' user='olist' password='IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1'")


# 'postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist'
with st.spinner('Conectando a la base de datos'):
    # DATABASE CONNECTION #
    conn = init_connection()


@st.experimental_memo(ttl=600)
def get_df_transformed():
    """Bring and transform a table from database and convert to dataframe

    Returns:
        DataFrame: daily orders
    """
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

# PREFICCION #


def predicción(df_fechas):
    df_pred = model.predict(df_fechas)
    return df_pred


def df_rango_fechas(start, end):
    lista_fechas = [start + timedelta(days=d)
                    for d in range((end - start).days+1)]
    ds = pd.DataFrame({'ds': lista_fechas})
    return ds

# LAYOUT PRINCIPAL #


def main():
    # TITULOS
    st.title('Forcasting de ventas :chart_with_upwards_trend:')
    st.markdown('---')

    # CARGA DEL DATAFRAME
    with st.spinner('Extrayendo datos...'):
        df_d = get_df_transformed()
        conn.close()
    st.success('Datos cargados exitosamente!')
    st.markdown(""" Es importante analizar y entender la evolución y el comportamiento de 
                los datos reales de venta a lo largo del tiempo. Por eso se presentan los componentes
                de la serie a partir de la predicción correspondiente.""")

    # SIDEBAR
    with st.sidebar:
        st.header('For our client:')
        st.image(logo_olist)
        st.header('Made with :heart: by:')
        st.image(logo_racont)

    st.header('Predicción con rango de fechas')

    # Slicer
    start_date = st.date_input(label="Fecha de inicio",
                               value=datetime.strptime("2017-06-13", "%Y-%m-%d"))
    end_date = st.date_input(label="Fecha de fin",
                             value=datetime.strptime("2018-12-18", "%Y-%m-%d"))  # , format="Y-%m-%d"

    if start_date < end_date:
        st.success('Start date: `%s`\n\nEnd date:`%s`' %
                   (start_date, end_date))
        slider = st.slider(
            'Selecciona el rango de fechas de predicción', min_value=start_date, value=(start_date, end_date))
        st.write("Tu rango de predicción es:", slider)
        # Dataframe de fechas

        if st.button(label='Aplicar'):
            ds = df_rango_fechas(slider[0], slider[1])
            df_predict = model.predict(ds)
            st.write(df_predict)
        else:
            st.write('Click en el boton')

    else:
        st.error('Error: End date must fall after start date.')


if __name__ == "__main__":
    main()
