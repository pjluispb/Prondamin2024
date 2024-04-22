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
    
def update_columns(row):
    row['paycon_y'] = row['paycon_x']
    row['condicion'] = 'Bloqueo en marca 01' if row['paycon_x'] in ['SI', 'SI++'] else '-'
    row['corte-1'] = 'Corte01:'+str(row['paycon_x'])+' -->22/4:4am'
    return row
    
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
dfpronda
# st.stop()
dfmarks = load_data03()            # Carga marks
dfmarks
# st.stop()
dfpymarks = pd.merge(dfpronda, dfmarks, on='key', how='left')
'dfpymarks = ', dfpymarks
# st.stop()
dfpymarks = dfpymarks.apply(update_columns, axis=1)
'dfpymarks con paycon_y actualizado', dfpymarks
# st.stop()

# para grabar en la bd en grupos de 20 registros a la vez
num_registros_por_lista = 20
# Crea una columna que represente el número de lista para cada registro
dfpymarks['lista'] = dfpymarks.index // num_registros_por_lista + 1           #le agrego una lista mas por si acaso
# Divide el DataFrame en grupos basados en la columna 'lista'
grupos = dfpymarks.groupby('lista')                                          # Ahora puedes acceder a cada grupo individualmente
#grupos
contador = 1
for nombre_lista, grupo in grupos:
    st.write('Lista ', nombre_lista)
    #grupo
    reggrupo = grupo.to_dict('records')
    reggrupo
    try:
        bdmarks.put_many(reggrupo)
    except:
        'error grabando grupo',contador
    contador+=1
    #if contador>12: break
#--------------------------------------------------------------------------

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

