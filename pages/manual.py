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


#----------------------------------------------------------------------------------------------------------------------
# generando una nueva marca de bloqueo
Prondamin24 = deta.Base('Prondamin2024C')
dfpronda = load_data02()           # Carga pronda
st.stop()
#dfpronda
#dfpronda2 = dfpronda[(dfpronda['condicion'].isnull()) | (dfpronda['condicion']!='Bloqueo en marca 01')]
dfpronda1 = dfpronda[(dfpronda['condicion']!='Bloqueo en marca 01')]
#dfpronda1                            # aqui se muestran los registros donde condicion!='Bloqueo en marca 01'
                                     # esto es, condicion==None o condicion=='-'
dfpronda2 = dfpronda1[(dfpronda1['condicion']!='Bloqueo en marca 2')]
#dfpronda2                            # aqui se muestran los registros donde condicion!='Bloqueo en marca 02'
                                     # esto es, condicion==None o condicion=='-'
dfpronda3 = dfpronda2[(dfpronda2['condicion']!='-')]
dfpronda3                            # aqui se muestran los registros donde condicion==None
conteo = dfpronda3['paycon'].value_counts()
conteo
conteo2 = dfpronda3['condicion'].value_counts()
conteo2
genmarca = st.button('Genera marca de bloqueo')
if genmarca:
    nueva_condicion = 'Bloqueo en marca 02'
    columnaspronda = dfpronda3.columns.values.tolist()
    nueva_condicion, columnaspronda
    # genera nuevo campo/columna corte
    'generando nueva marca de bloqueo'
    cort_strings = [s for s in columnaspronda if s.startswith('corte-')]
    cort_strings
    # Encontrar el último número existente
    numeros = [int(s[len('corte-'):]) for s in cort_strings]
    ultimo_numero = max(numeros) if numeros else 0
    # Generar el siguiente número consecutivo
    siguiente_numero = ultimo_numero + 1
    # Crear la nueva cadena con el prefijo y el número
    nueva_columna = 'corte-'+str(siguiente_numero)
    nueva_condicion = 'Bloqueo en marca '+str(siguiente_numero)
    nueva_columna
    for corte in cort_strings:
        dfpronda3[corte] = dfpronda3[corte].apply(lambda x: '-' if pd.isnull(x) else x)
    dfpronda3[nueva_columna] = nueva_columna+':'+dfpronda3['paycon']+' -->22/2pm'
    dfpronda3['condicion'] = nueva_condicion
    dfpronda3['Categoría Actual'] = dfpronda3['Categoría Actual'].fillna('-')
    dfpronda3['Cédula'] = dfpronda3['Cédula'].fillna('-')
    dfpronda3['ReporteCertif'] = dfpronda3['ReporteCertif'].fillna('-')
    dfpronda3['Status'] = dfpronda3['Status'].fillna('-')
    dfpronda3['close'] = dfpronda3['close'].fillna('-')
    dfpronda3['corte-1'] = dfpronda3['corte-1'].fillna('-')
    dfpronda3['curso'] = dfpronda3['curso'].fillna('-')
    dfpronda3['value'] = dfpronda3['value'].fillna('-')
    dfpronda3.drop(columns = ['lista'], inplace=True )
    dfpronda3
    # para grabar en la bd en grupos de 20 registros a la vez
    num_registros_por_lista = 20
    ' dfpronda3.index = ', dfpronda3.index
    
    # Crea una columna que represente el número de lista para cada registro
    dfpronda3['lista'] = dfpronda3.index // num_registros_por_lista
    dfpronda3['lista']
    dfpronda3['lista'].value_counts()
    
    # Divide el DataFrame en grupos basados en la columna 'lista'
    grupos = dfpronda3.groupby('lista')                                          # Ahora puedes acceder a cada grupo individualmente
    #grupos
    
    contador = 1
    for nombre_lista, grupo in grupos:
        st.write('Lista ', nombre_lista, contador)
        grupo
        reggrupo = grupo.to_dict('records')
        
        if contador < 100:               
            reggrupo
            try:
                Prondamin24.put_many(reggrupo)
                'listo grupo ',str(contador)
            except:
                'error grabando grupo',contador
                reggrupo
                st.stop()
        else: st.stop()
        contador+=1
    #-------------------------------
    
    
st.stop()
#dfpronda = load_data02()           # Carga pronda
##dfprondabloq1 = dfpronda[(dfpronda['condicion']=='Bloqueo en marca 01') & (dfpronda['value']=='exonerado') ]
#dfprondabloq1 = dfpronda[(dfpronda['condicion']!='Bloqueo en marca 01')]
#dfprondabloq1
#conteo = dfprondabloq1['paycon'].value_counts()
#conteo
#==================================================================================================================================
# Carga Pronda y marks y los mezcla, actualiza loc campos condicion y corte-1 y graba los registros en Prondamin2024C

#Prondamin24 = deta.Base('Prondamin2024C')
#dfpronda = load_data02()           # Carga pronda
#dfpronda
#dfpronda2 = dfpronda[(dfpronda['condicion'].isnull())]
#dfpronda2
#st.stop()
#dfmarks = load_data03()            # Carga marks
#dfmarks

#dfpymarks = pd.merge(dfpronda2, dfmarks, on='key', how='left')
#'dfpymarks = ', dfpymarks
#st.stop()
#dfpymarks = dfpymarks.apply(update_columns, axis=1)
#dfpymarks['value'] = dfpymarks['value'].fillna('-')                             # Coloca value = '-' cuando valga None
#dfpymarks['close'] = dfpymarks['close'].fillna('-')                             # Coloca close = '-' cuando valga None
#dfpymarks['Categoría Actual'] = dfpymarks['Categoría Actual'].fillna('-')       # Coloca Categoría Actual = '-' cuando valga None
#dfpymarks['Cédula'] = dfpymarks['Cédula'].fillna('-')                          # Coloca Cédula = '-' cuando valga None
#dfpymarks['ReporteCertif'] = dfpymarks['ReporteCertif'].fillna('-')            # Coloca ReporteCertif = '-' cuando valga None
#dfpymarks['Status'] = dfpymarks['Status'].fillna('-')                           # Coloca Status = '-' cuando valga None
#dfpymarks['curso'] = dfpymarks['curso'].fillna('-')                           # Coloca curso = '-' cuando valga None
#'dfpymarks con paycon_y actualizado', dfpymarks
#st.stop()
#dfpymarks.drop(columns = ['paycon_y', 'lista'], inplace=True )
#dfpymarks.rename(columns={'paycon_x':'paycon'}, inplace=True)
#'dfpymarks_final =', dfpymarks
#st.stop()
# para grabar en la bd en grupos de 20 registros a la vez
#num_registros_por_lista = 20
# Crea una columna que represente el número de lista para cada registro
#dfpymarks['lista'] = dfpymarks.index // num_registros_por_lista
# Divide el DataFrame en grupos basados en la columna 'lista'
#grupos = dfpymarks.groupby('lista')                                          # Ahora puedes acceder a cada grupo individualmente
#grupos
#contador = 1
#for nombre_lista, grupo in grupos:
#    st.write('Lista ', nombre_lista)
    #grupo
#    reggrupo = grupo.to_dict('records')
    
#    if 160 < contador < 170:                #graba los primeros 100 grupos de 162
#        reggrupo
#        try:
#            Prondamin24.put_many(reggrupo)
#            'listo grupo ',str(contador)
#        except:
#            'error grabando grupo',contador
#            reggrupo
#            st.stop()
#    else: st.stop()
#    contador+=1
#--------------------------------------------------------------------------

#if st.button("Clear All"):
    # Clear values from *all* all in-memory and on-disk data caches:
    # i.e. clear values from both square and cube
#    st.cache_data.clear()

#==============================================================================================================================
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



