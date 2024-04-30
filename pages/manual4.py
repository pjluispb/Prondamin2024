import pandas as pd
import streamlit as st
from deta import Deta
import time

deta = Deta(st.secrets["deta_key"])

@st.cache_data
def load_data02():
    Pronda24 = deta.Base('Prondamin2024C')
    res = Pronda24.fetch(limit=500)
    all_items = res.items
    while res.last:
        res = Pronda24.fetch(last=res.last)
        all_items += res.items
    dfall_items = pd.DataFrame(all_items)
    return dfall_items



Pronda = load_data02()

sel_col = ['key',  'distrito', 'categoría', 'nombre', 'apellido', 'emails', 'teléfonos', 'paycon', 'modalidad', 'referenciaPago']         # List of desired column names
dfProndaSC = Pronda[sel_col]
dfProndaSC['teléfonos'] = dfProndaSC['teléfonos'].apply(lambda x: str(x[0]) if x else '')
'pronda = ', dfProndaSC
st.write(dfProndaSC['teléfonos'].value_counts())
