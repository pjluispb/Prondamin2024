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


dfpronda = load_data02()
#dfpronda
dfexo = dfpronda[dfpronda['value']=='exonerado']
dfexo
#dfpendiente = df2[df2['paycon']=='PENDIENTE']
#--------------------------------------------------
# Pronda = deta.Base('Prondamin2024C')
# Pronda.delete(" 10126173")
# reg = {.....}
#Pronda.put(reg)
#--------------------------------------------------
#mask24 = deta.Base('marks24B')
#mask24f = mask24.fetch(limit=5000)
#dfmask24 = pd.DataFrame(mask24f.items)

#regmask = dfmask24.to_dict('records')

#cont=1
#for registro in regmask:
#	mask24.delete(registro['key'])
#	cont+=1
#	'registro borrado ',str(cont)
#-------------------------------------------------	

