import streamlit as st

st.set_page_config(page_title='Inicio', 
                   page_icon='🚀', 
                   layout="centered", 
                   initial_sidebar_state="collapsed", 
                   menu_items=None)


#body{
#    font-family: 'Poppins', sans-serif;
#    background-color: #b9b9b9;
#    background-image: radial-gradient( ellipse farthest-corner at 40px 40px , #3f8c5e, #3f8c5e 50%, #b9b9b9 50%);
#    background-size:  15px 30px;
#}


st.title('TA Tools :rocket:')

st.header('Esta app proporciona herramientas e información útil para TAs')

st.markdown('En el menú a tu izquierda puedes acceder a distintas métricas de tu grupo:')


st.markdown("""
    Saber qué distribución de edades tienen, sus nacionalidades,
    dispositivo con el que se conectan y los periféricos que disponen.
    También conocer qué temas prefieren hablar durante el SUP y algunos
    datos extra que pueden servirte. 
""")