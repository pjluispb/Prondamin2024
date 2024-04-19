import streamlit as st
import pandas as pd
from deta import Deta


deta = Deta(st.secrets["deta_key"])

@st.cache_data
def load_data():
    # # Carga el Pronda
    Prondamin24 = deta.Base('Prondamin2024C')
    Pronda24 = Prondamin24.fetch(limit=4000).items
    return pd.DataFrame(Pronda24)

# Boolean to resize the dataframe, stored as a session state variable
st.checkbox("Use container width", value=False, key="use_container_width")

df = load_data()
df



#dfPronda24 = pd.DataFrame(Pronda24)

# Simulación de un DataFrame con 4000 filas
#data = pd.DataFrame({"key": range(4000), "nombre": range(4000), "apellido": range(4000), "categoría": range(4000), "distrito": range(4000), "paycon": range(4000)})
#data = pd.DataFrame(Pronda24)
