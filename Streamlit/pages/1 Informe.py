import streamlit as st

st.set_page_config(page_title='TA Tools - Edades', 
                   page_icon='📊', 
                   layout="centered", 
                   initial_sidebar_state="expanded", 
                   menu_items=None)


st.header('Informe del Análisis de datos')
   

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

show_pdf('post1-compressed.pdf')
    


st.markdown("""
<embed src="https://drive.google.com/viewerng/
viewer?embedded=true&url=https://drive.google.com/file/d/1ZTXhWUK8tRgwE79U8jXtSzphUJDCmHdP/view?usp=sharing" width="800" height="600">
""", unsafe_allow_html=True)