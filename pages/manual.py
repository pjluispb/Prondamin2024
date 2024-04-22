import pandas as pd
import streamlit as st
from deta import Deta

deta = Deta(st.secrets["deta_key"])

def update_paycon(row):
    fmontoPago = float(row['montoPago']) if row['montoPago'] not in ('-', None, '') else 0
    fmontoApagar = float(row['montoApagar']) if row['montoApagar'] not in ('-', None, '') else 0
    diferencia = fmontoPago - fmontoApagar
    if -10 <= diferencia <= 10:
        return 'SI'
    elif diferencia < -10:
        return 'PENDIENTE X DIFERENCIA'
    elif diferencia > 10:
        return 'SI++'
    else:
        return row['paycon']  # Keep the original value if none of the conditions apply

def update_condicion(row):
    row['condicion'] = 'Bloqueo en marca 01' if row['paycon_y'] in ['SI', 'SI++'] else '-'
    #row['condicion'] = vcondicion
    return row['condicion']
    
def update_paycon_y(row):
    pay_y = row['paycon_x'] 
    return pay_y
    
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
    
@st.cache_data
def load_data03():
    marks24 = deta.Base('marks24B')
    res = marks24.fetch(limit=500)
    all_items = res.items
    while res.last:
        res = marks24.fetch(last=res.last)
        all_items += res.items
    dfall_items = pd.DataFrame(all_items)
    return dfall_items


dfpronda = load_data02()           # Carga pronda
dfmarks = load_data03()            # Carga marks
dfpronda
dfmarks
dfpymarks = pd.merge(dfpronda, dfmarks, on='key', how='left')
'dfpymarks = ', dfpymarks

dfpymarks['paycon_y'] = dfpymarks.apply(update_paycon_y, axis=1)                  # Actualiza paycon_y en dfpyd
dfpymarks['paycon_y'] = dfpymarks.apply(update_condicion, axis=1)                 # Actualiza condicion en dfpyd
'dfpymarks con paycon_y actualizado', dfpymarks

if st.button("Clear All"):
    # Clear values from *all* all in-memory and on-disk data caches:
    # i.e. clear values from both square and cube
    st.cache_data.clear()
    
#dfpyd = pd.merge(dfPronda24_ref, DatBanVerif, on='referenciaPago', how='left')   # Mezcla Pronda y DatBanVerif
#---------------------------------------------------
# muestra los exonerados en dfpronda
#dfpronda = load_data02()          # Carga completa(todos los registros) de la bd pronda
#dfpronda
#dfexo = dfpronda[dfpronda['value']=='exonerado']
#dfexo
#-------------------------------------------------
# muestra si existe la columna value en dfpronda
#if 'value' in dfpronda.columns:
#    'columna value existe en dfpronda'
#dfpendiente = df2[df2['paycon']=='PENDIENTE']
#--------------------------------------------------
# para eliminar(1ro) y luego crear(put) registros en Pronda
# Pronda = deta.Base('Prondamin2024C')
# Pronda.delete(" 10126173")
# reg = {.....}
#Pronda.put(reg)
#--------------------------------------------------
# para borrar(delete) todos los registros en mask24
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

