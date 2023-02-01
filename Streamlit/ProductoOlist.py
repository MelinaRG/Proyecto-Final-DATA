import streamlit as st
import base64
import os



#Configuración de la página
st.set_page_config(page_title='TA Tools - Edades', 
                   page_icon='📊', 
                   layout="centered", 
                   initial_sidebar_state="expanded", 
                   menu_items=None)



#Aplicar fondo de pantalla
path_img = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "./assets/fondo.png")

import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local(path_img)       



path_web = 'https://docs.google.com/document/d/1T5kXNatlGFI60dV4AihWUWGGr4ybV2cU/edit?usp=sharing&ouid=110999774945235708227&rtpof=true&sd=true'
st.markdown(f'<iframe src="{path_web}" width="950" height="700"></iframe>', unsafe_allow_html=True)



#Código para visualizar PDF local    
#path = os.path.join(os.path.dirname(
#    os.path.abspath(__file__)), "./assets/Análisis - Proyecto Olist.pdf")
#    
#def show_pdf(file_path):
#    with open(file_path,"rb") as f:
#        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1000" height="800" class_="iframe-center" type="application/pdf"></iframe>'
#    st.markdown(pdf_display, unsafe_allow_html=True)
#
#show_pdf(path)