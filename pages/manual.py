import pandas as pd
import streamlit as st
from deta import Deta

deta = Deta(st.secrets["deta_key"])
Pronda = deta.Base('Prondamin2024C')

exone = Pronda.fetch({'value?contains':'exonerado'}, limit=5000)
dfexone = pd.DataFrame(exone.items)
dfexone
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

