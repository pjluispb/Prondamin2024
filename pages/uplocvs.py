
import streamlit as st
import pandas as pd
from deta import Deta

def check_csv_header(header):
    required_columns = ['Fecha', 'Descripcion', 'Referencia', 'Egreso', 'Ingreso']
    return all(column in header for column in required_columns)
    
# Carga el archivo CSV desde el usuario
uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])

if uploaded_file is not None:
    # Lee el archivo CSV en un DataFrame
    df = pd.read_csv(uploaded_file)
    dfingresoXpm = df[df['DESCRIPCION'] == 'NC - PAGO MOVIL INTERBANCARIO']
    dfingresoXtrans = df[df['DESCRIPCION'] == 'NC - TRANSFERENCIA DE FONDOS VIA INTERNET']
    frames = [dfingresoXpm, dfingresoXtrans]

    dfingreso = pd.concat(frames)
    # Muestra el DataFrame
    st.write(dfingreso)


# lee csv desde detadrive
# deta = Deta(st.secrets["deta_key"])
# drive2024 = deta.Drive("datoscvsminec")
# dicPminec2024 =  drive2024.list()
# dicPminec2024

# response = drive2024.get("data2024-01bkp.csv")
# content = response.read()
# type(content)

# # content
# df = pd.read_csv(response)
# df = pd.read_csv(content)
# df
