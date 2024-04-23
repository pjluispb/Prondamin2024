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

def update_condicion(row):
    #'row : ', row
    #fmontoPago = float(row['montoPago']) if row['montoPago'] not in ('-', None, '') else 0
    if row['paycon'] in ['NO', 'PENDIENTE', 'PENDIENTE X DIFERENCIA']:
        return '-'
    else:
        if row['corte-1'] != '-':
            return 'Bloqueo en marca 01'
        else:
            if row['corte-2'].find('SI')>0:
                return 'Bloqueo en marca 2'
            else:
                return 'Bloqueo en marca 3'




#autoriza = st.text_input('ingresa clave')
#with st.spinner('...'):
#    time.sleep(5)
#if autoriza not in (5125570, 77777):
#    st.switch_page('home2024.py')

#---------------------------------------------------------------------------------------------------------
# Aqui se genera el df con los registros bloqueados inicialmente(corte-1 y corte-2 son no nulos)
Pronda = load_data02()
df_filtrado = Pronda.dropna(subset=["corte-1", "corte-2"], thresh=2)
selected_columns = ['key', 'paycon', 'distrito', 'categoría', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'referenciaPago']         # List of desired column names
df_selected = df_filtrado[selected_columns]
#df_selected
df_filtrado
st.write(df_filtrado['paycon'].value_counts())

df_complementario = Pronda.loc[~Pronda.index.isin(df_filtrado.index)]
df_complement_selected = df_complementario[selected_columns]
#df_complement_selected
df_complementario
st.write(df_complementario['paycon'].value_counts())

#---------------------------------------------------------------------------------------------
#Pronda = load_data02()
#Pronda
#------modo 1 de mostrar solo cuando haya valor en corte-1 y corte-2---
#df1 = Pronda[Pronda['corte-1'].notnull()]
#df1
#st.write(df1['paycon'].value_counts())
#df2 = Pronda[Pronda['corte-2'].notnull()]
#df2
#st.write(df2['paycon'].value_counts())
#-----modo 1 de mostrar solo cuando haya valor en corte-1 y corte-2-----
#df_filtrado = Pronda.dropna(subset=["corte-1", "corte-2"], thresh=2)
#df_filtrado
#st.write(df_filtrado['paycon'].value_counts())
#------------------------------------------------------------------------------------

#-----------------------------------------------------
# Pronda = load_data02()
# Pronda
# Display specific columns
# selected_columns = ['key', 'paycon', 'condicion', 'corte-1', 'corte-2', 'corte-3', 'distrito']  # List of desired column names
# df_selected = Pronda[selected_columns]
# df_selected
# df_selected['condicion'] = df_selected.apply(update_condicion, axis=1)
# df_selected
# st.stop()
#--------------------------------------------------
# para eliminar(1ro) y luego crear(put) registros en Pronda
#Pronda = deta.Base('Prondamin2024C')
#Pronda.delete("92ttxhdnjfnt")
# reg = {.....}
#Pronda.put(reg)
#--------------------------------------------------
