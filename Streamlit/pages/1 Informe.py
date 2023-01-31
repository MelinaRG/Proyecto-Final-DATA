import streamlit as st

st.set_page_config(page_title='TA Tools - Edades', 
                   page_icon='📊', 
                   layout="centered", 
                   initial_sidebar_state="expanded", 
                   menu_items=None)


# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
# Display a static table


header_style = '''
    <style>
        th{
            background-color: yellow;
        }
    </style>
'''
st.markdown(header_style, unsafe_allow_html=True)


st.header('Indicadores de tu grupo')
   

st.markdown("""
<embed src="https://drive.google.com/viewerng/
viewer?embedded=true&url=https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf" width="600" height="480">
""", unsafe_allow_html=True)


with open("post1-compressed.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="Descarga PDF", 
        data=PDFbyte,
        file_name="pandas-clean-id-column.pdf",
        mime='application/octet-stream')