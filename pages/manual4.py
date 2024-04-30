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

Pronda = load_data02()

sel_col = ['key',  'distrito',  'nombre', 'apellido', 'teléfonos']         # List of desired column names
dfProndaSC = Pronda[sel_col]
dfProndaSC['teléfonos'] = dfProndaSC['teléfonos'].apply(lambda x: str(x[0]) if x else '')
dfProndaSC['telefFormat'] = '-'
#dfProndaSC['telefFormat'] = dfProndaSC.apply(formatelf, axis=1)
'pronda = ', dfProndaSC
st.write(dfProndaSC['teléfonos'].value_counts())

