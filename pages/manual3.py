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


#----------Lista de Lara--------------------------------------------------
dfPronda = load_data02()
dfLara1 = dfPronda[dfPronda['distrito']=='Lara']
dfLara = dfLara1[dfLara1['paycon']!='NO']
sel_col = ['key', 'paycon', 'distrito', 'categoría', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'referenciaPago']         # List of desired column names
dfLaraSC = dfLara[sel_col]
dfLaraSC['emails'] = dfLaraSC['emails'].apply(lambda x: str(x[0]) if x else '')
dfLaraSC
st.write(dfLaraSC['paycon'].value_counts())
#----------Listado de calificaciones de Lara----------------------------
uploaded_file = st.file_uploader("Subir archivo CSV", type=["csv"])  
if uploaded_file is not None:
    # Lee el archivo CSV en un DataFrame
    df = pd.read_csv(uploaded_file) 
    df
    #st.write(df['test01'].value_counts())
'---'    
#dfpyd = pd.merge(dfPronda24_ref, DatBanVerif, on='referenciaPago', how='left')   # Mezcla Pronda y DatBanVerif   
#dfpymarks = pd.merge(dfpronda2, dfmarks, on='key', how='left')
result = pd.merge(dfLaraSC, df, on='emails', how='left')
#result = pd.merge(dfLaraSC, df, on=
#result = pd.merge(dfLaraSC, df, left_on=['nombre', 'apellido'], right_on=['nombre', 'apellido'])
'result = ', result
st.write(result['test01'].value_counts())

#=======Genera la lista de los matriculados con Pendiente y Pendiente por diferncia============================
#dfPronda = load_data02()
#dfsis = dfPronda[dfPronda['paycon'] == 'SI']
#dfsim = dfPronda[dfPronda['paycon'] == 'SI++']
#dfSI = pd.concat([dfsis, dfsim])
#dfnoSI = dfPronda.loc[~dfPronda.index.isin(dfSI.index)]
#dfPronda24 = dfnoSI
#dfnoSI
#st.write(dfnoSI['paycon'].value_counts())
#dfnoSIPend = dfnoSI[dfnoSI['paycon']=='PENDIENTE']
#dfnoSIPXD = dfnoSI[dfnoSI['paycon']=='PENDIENTE X DIFERENCIA']
#dfnoSIPend
#selected_columns = ['key', 'paycon', 'distrito', 'categoría', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'referenciaPago']         # List of desired column names
#dfnoSIPend_selected = dfnoSIPend[selected_columns]
#dfnoSIPend_selected
#st.write(dfnoSIPend['paycon'].value_counts())
#dfnoSIPXD 
#dfnoSIPXD_selected = dfnoSIPXD[selected_columns]
#dfnoSIPXD_selected
#st.write(dfnoSIPXD['paycon'].value_counts())
#==============================================================================================================

