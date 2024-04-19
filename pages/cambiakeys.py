
import streamlit as st
import pandas as pd
from deta import Deta
from PIL import Image



deta = Deta(st.secrets["deta_key"])


def replace_value(value):
    if pd.isnull(value):
        return ['-']
    else:
        return [str(value)]

uploaded_file = st.file_uploader("Subir archivo CSV", type=["csv"]) 
if uploaded_file is not None:
    # Lee el archivo CSV en un DataFrame
    dfu = pd.read_csv(uploaded_file) 
    dfu
    dfu['CédulaOLD'] = dfu['CédulaOLD'].astype(str)
    dfu['CédulaNEW'] = dfu['CédulaNEW'].astype(str)
    dfu['Teléfono'] = dfu['Teléfono'].apply(replace_value)
    dfu['Correo'] = dfu['Correo'].apply(replace_value)
    'dfu = ', dfu
    cedulas = dfu["CédulaOLD"]  

# # Carga el Pronda
Prondamin24 = deta.Base('Prondamin2024C')
Pronda24 = Prondamin24.fetch(limit=5000).items
dfPronda24 = pd.DataFrame(Pronda24)

'cedulas = ', cedulas
'dfPronda24 = ', dfPronda24

dfProndaSel = dfPronda24[dfPronda24['key'].isin(cedulas)]
'dfProndaSel = '
dfProndaSel




