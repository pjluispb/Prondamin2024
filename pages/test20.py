import pandas as pd
from deta import Deta
import streamlit as st

deta = Deta(st.secrets.deta_key)

st.set_page_config(
    page_title="Minec Reg App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def row_style(row):
    if row['paycon'] == 'SI++':
        return pd.Series('background-color: #7986cb; color:#000000', row.index)
    elif row['paycon'] == 'PENDIENTE X DIFERENCIA':
        return pd.Series('background-color: #ff5079; color:#000000', row.index)
    elif row['paycon'] == 'SI':
        return pd.Series('background-color: #8ede99; color:#000000', row.index)
    elif row['paycon'] == 'PENDIENTE':
        return pd.Series('background-color: #fdd834; color:#000000', row.index)
    else:
        return pd.Series('', row.index)


pronda2024 = deta.Base('Prondamin2024C')
p24 = pronda2024.fetch(limit=5000)
dfp24 = pd.DataFrame(p24.items)

dfp24_color = dfp24.style.apply(row_style, axis=1)
dfp24_color

dfp24_ordenado = dfp24.sort_values(by='paycon', ascending=False)
conteopaycon = dfp24_ordenado['paycon'].value_counts()
conteoclose = dfp24_ordenado['close'].value_counts()
conteodistrito = dfp24_ordenado['distrito'].value_counts()
conteocategoria = dfp24_ordenado['categoría'].value_counts()
conteomodalidad = dfp24_ordenado['modalidad'].value_counts()

'Status Pagos', conteopaycon
'Distritos', conteodistrito
'Categorías', conteocategoria
'Modalidad', conteomodalidad
'cerrados', conteoclose



