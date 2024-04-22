import pandas as pd
import streamlit as st
from deta import Deta

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
Pronda
#--------------------------------------------------
# para eliminar(1ro) y luego crear(put) registros en Pronda
#Pronda = deta.Base('Prondamin2024C')
#Pronda.delete("92ttxhdnjfnt")
# reg = {.....}
#Pronda.put(reg)
#--------------------------------------------------
