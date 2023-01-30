import streamlit as st

st.set_page_config(page_title='Olist', 
                   page_icon=None, 
                   layout="centered", 
                   initial_sidebar_state="auto", 
                   menu_items=None)


import base64

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('background.png')


st.title('TA Tools :rocket:')

st.header('Esta app proporciona herramientas e información útil para TAs')

st.markdown('En el menú a tu izquierda puedes acceder a distintas métricas de tu grupo:')


st.markdown("""
    Saber qué distribución de edades tienen, sus nacionalidades,
    dispositivo con el que se conectan y los periféricos que disponen.
    También conocer qué temas prefieren hablar durante el SUP y algunos
    datos extra que pueden servirte. 
""")