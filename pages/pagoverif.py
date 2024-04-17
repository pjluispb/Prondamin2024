import pandas as pd
import streamlit as st
from deta import Deta
from PIL import Image

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

deta = Deta(st.secrets["deta_key"])


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

def highlight_cells(val):
    return 'background-color: yellow' if val == val else ''
    
# Carga la bd de accesos
accesos = deta.Base('minec-accesos')
res=accesos.fetch()
# try:
#     logina = st.session_state['logina']
# except:
#     st.switch_page('home2024.py')

# Carga el Pronda
Prondamin24 = deta.Base('Prondamin2024C')
Pronda24 = Prondamin24.fetch(limit=5000)
dfPronda24 = pd.DataFrame(Pronda24.items)
# dfPronda24

# Carga el DBanVerif2024 ...Datos Bancarios ya procesados
DBanV24 = deta.Base('DBanVerif2024')
DBanV24f = DBanV24.fetch().items
dfDBanV24 = pd.DataFrame(DBanV24f)

st.image(imagen1)
st.image(imagen2)

df = dfPronda24.dropna(subset=['close'])
#df
df_ordenado = df.sort_values(by='paycon', ascending=False)
#df_color = df_ordenado.style.apply(row_style, axis=1)
#df_color
cuentaref = df_ordenado['referenciaPago'].value_counts()
#cuentaref
claves = cuentaref.keys()
refrepetidas=[]
for k, v in cuentaref.items():
    if v > 1:
        k,v
        refrepetidas.append(k)
refrepetidas








