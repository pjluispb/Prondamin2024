import streamlit as st
import pandas as pd
from deta import Deta


deta = Deta(st.secrets["deta_key"])

@st.cache_data
def load_data():
    # # Carga el Pronda
    Prondamin24 = deta.Base('Prondamin2024C')
    Pronda24 = Prondamin24.fetch(limit=4500)
    Pronda24items = Pronda24.items
    Pronda24last = Pronda24.last
    Pronda24count = Pronda24.count
    return (pd.DataFrame(Pronda24items), Pronda24last, Pronda24count)
    
@st.cache_data
def load_data02():
    Pronda24 = deta.Base('Prondamin2024C')
    res = Pronda24.fetch()
    all_items = res.items

    while res.last:
        res = Pronda24.fetch(last=res.last)
        all_items += res.items
    return pd.DataFrame(res)
    
# Boolean to resize the dataframe, stored as a session state variable
# st.checkbox("Use container width", value=False, key="use_container_width")

#df, lastdf, countdf = load_data()
#df
#lastdf
#countdf

df2 = load_data02()
df2



#dfPronda24 = pd.DataFrame(Pronda24)

# Simulación de un DataFrame con 4000 filas
#data = pd.DataFrame({"key": range(4000), "nombre": range(4000), "apellido": range(4000), "categoría": range(4000), "distrito": range(4000), "paycon": range(4000)})
#data = pd.DataFrame(Pronda24)
