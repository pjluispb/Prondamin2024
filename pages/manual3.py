import streamlit as st
import pandas as pd
from deta import Deta
from PIL import Image
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


dfPronda = load_data02()
dfsis = dfPronda[dfPronda['paycon'] == 'SI']
dfsim = dfPronda[dfPronda['paycon'] == 'SI++']
dfSI = pd.concat([dfsis, dfsim])
dfnoSI = dfPronda.loc[~dfPronda.index.isin(dfSI.index)]
dfPronda24 = dfnoSI
dfnoSI
st.write(dfnoSI['paycon'].value_counts())
dfnoSIPend = dfnoSI[dfnoSI['paycon']=='PENDIENTE']
dfnoSIPXD = dfnoSI[dfnoSI['paycon']=='PENDIENTE X DIFERENCIA']
dfnoSIPend
st.write(dfnoSIPend['paycon'].value_counts())
dfnoSIPXD 
st.write(dfnoSIPXD['paycon'].value_counts())

