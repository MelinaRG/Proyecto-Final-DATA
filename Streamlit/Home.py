import streamlit as st
from PIL import Image
import os


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
    st.header('For our client:')
    st.image(logo_olist)
    st.header('Made with :heart: by:')
    st.image(logo_racont)

st.header('Esta aplicación está construida para realizar el deploy del modelo de Machine Learning construido para el marketplace Olist')
st.markdown('👈En el menú a tu izquierda puedes acceder al menú correspondiente')


st.markdown('* Link **importante**')