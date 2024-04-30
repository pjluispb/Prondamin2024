import pandas as pd
import streamlit as st
from deta import Deta
import time
import re

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

def formatelf(row):
    digitos = re.sub(r'\D', '', str(row['teléfonos']))
    newt = digitos
    if digitos=='': newt = '-'
    if digitos == '0416': newt = '-'
    if digitos.startswith('04'):
        if digitos[2:4] in ['12', '14', '16', '24', '26']:
            newt = '04'+digitos[2:4]+' - '+digitos[4:]
    if digitos.startswith('4'):
        if digitos[0:3] in ['412', '414', '416', '424', '426']:
            newt = '0'+digitos[0:3]+' - '+digitos[3:10]
    if digitos.startswith('02'):
        newt = digitos[:4]+' - '+digitos[4:]
    if digitos.startswith('58'):
        newt = '+'+digitos[:2]+' - '+digitos[2:5]+' - '+digitos[5:]
    if digitos.startswith('59'):
        newt = '+'+digitos[:2]+' - '+digitos[2:5]+' - '+digitos[5:]
    if digitos.startswith('57'):
        newt = '+'+digitos[:2]+' - '+digitos[2:5]+' - '+digitos[5:]
    if digitos.startswith('56'):
        newt = '+'+digitos[:2]+' - '+digitos[2:5]+' - '+digitos[5:]
    if digitos.startswith('54'):
        newt = '+'+digitos[:2]+' - '+digitos[2:5]+' - '+digitos[5:]
    if digitos.startswith('51'):
        newt = '+'+digitos[:2]+' - '+digitos[2:5]+' - '+digitos[5:]
    if digitos.startswith('34'):
        newt = '+'+digitos[:2]+' - '+digitos[2:5]+' - '+digitos[5:]
    if digitos.startswith('351'):
        newt = '+'+digitos[:3]+' - '+digitos[3:6]+' - '+digitos[6:]
    if digitos.startswith('212'):
        newt = '+'+digitos[:3]+' - '+digitos[3:6]+' - '+digitos[6:]
    if digitos.startswith('1'):
        if len(digitos)==11:
            newt = '+1'+' - '+digitos[1:4]+' - '+digitos[4:7]+' - '+digitos[7:]
    return newt
    

Pronda = load_data02()

sel_col = ['key',  'distrito',  'nombre', 'apellido', 'teléfonos', 'emails']         # List of desired column names
dfProndaSC = Pronda[sel_col]
dfProndaSC['telefFormat'] = dfProndaSC['teléfonos']
dfProndaSC['telefFormat'] = dfProndaSC['telefFormat'].apply(lambda x: str(x[0]) if x else '')
#dfProndaSC['telefFormat'] = '-'
dfProndaSC['telefFormat'] = dfProndaSC.apply(formatelf, axis=1)
dfProndaSC['xval'] = '***'
'pronda = ', dfProndaSC
st.write(dfProndaSC['telefFormat'].value_counts())

