
import streamlit as st
import pandas as pd
from deta import Deta
from PIL import Image



deta = Deta(st.secrets["deta_key"])

uploaded_file = st.file_uploader("Subir archivo CSV", type=["csv"]) 
dfu = pd.read_csv(uploaded_file)
dfu
# Carga el Pronda
try:
    Prondamin24 = deta.Base('Prondamin2024C')
    Pronda24 = Prondamin24.fetch(limit=5000)
    dfPronda24 = pd.DataFrame(Pronda24.items)
    #st.dataframe(dfPronda24)
except:
    'Problemas cargando Pronda'

'---'
dfPronda24

cedulasOLD = set(dfu['CédulaOLD'])
cedulasOLD



