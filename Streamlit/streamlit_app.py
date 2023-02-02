import base64
import streamlit as st
from PIL import Image
import os

# CONFIGURACION DE LA PAGINA #
# Aplicar fondo de pantalla
# Configuración de la página
st.set_page_config(page_title='Proyecto Olist',
                   page_icon='📊',
                   layout="centered",
                   initial_sidebar_state="expanded",
                   menu_items=None)

# ISOLOGO #
logo_path_racont = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "./assets/isologo.png")
logo_racont = Image.open(logo_path_racont)
logo_path_olist = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "./assets/logo_olist.png")
logo_olist = Image.open(logo_path_olist)


st.title('Bienvenido! :rocket:')

# SIDEBAR
with st.sidebar:
    st.subheader('For our client:')
    st.image(logo_olist, width=60)
    st.subheader('Made with :heart: by:')
    st.image(logo_racont, width=90)

st.markdown('---')
st.subheader('Aplicación para Análisis de serie de tiempo de venta diaria de Olist y deploy del modelo de Machine Learning para Forecasting')
st.markdown('👈 **Páginas**')
st.markdown(
    '* En el menú a tu izquierda puedes acceder a las páginas del análisis y predicción correspondiente')
st.markdown(
    '* Al renderizar las paginas se conectan a la base de datos trayendo la data histórica de ordenes de compra (datos de venta) y se re realiza una breve transformación para poder realizar las gráficas')
st.markdown(
    "* Visita el link al repositorio del proyecto [:link:](https://github.com/MelinaRG/Proyecto-Final-DATA)")
