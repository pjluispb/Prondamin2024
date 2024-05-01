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
    digitos = re.sub(r'\D', '', str(row['notifitelf']))
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
    



listdb = []
try:  #obtiene pronda2023 y su drive
    pronda2023 = deta.Base('PRONDAMIN2023-Final')
    df23 = pd.DataFrame(pronda2023.fetch().items)
    drive2023 = deta.Drive("minec")
    dicPminec2023 =  drive2023.list()
    p2023 = 'PRONDAMIN2023'
    df23
    dicPminec2023
except:
    st.write('********Error conectando con Prondamin2023-Final y el drive minec')
try:  #obtiene pronda2022 y su drive
    pronda2022 = deta.Base('PRONDANMIN-2022')
    df22 = pd.DataFrame(pronda2022.fetch().items)
    drive2022 = deta.Drive("minec2022")
    dicPminec2022 =  drive2022.list()
    p2022 = 'PRONDAMIN2022'
    df22
    dicPminec2022
except:
    st.write('*/*/*/*/*/*/*/')
try:  #obtiene pronda2021 y su drive
    pronda2021 = deta.Base('PRONDANMIN-2021')
    df21 = pd.DataFrame(pronda2021.fetch().items)
    drive2021 = deta.Drive("minec2021")
    dicPminec2021 =  drive2021.list()
    p2021 = 'PRONDAMIN2021'
    df21
    dicPminec2021
    #st.write(pronda2021.fetch().items)
except:
    st.write('pronda2021 NO existe')
try:  #obtiene pronda2020 y su drive
    pronda2020 = deta.Base('PRONDANMIN-2020')
    df20 = pd.DataFrame(pronda2020.fetch().items)
    drive2020 = deta.Drive("minec2020")
    dicPminec2020 =  drive2020.list()
    p2020 = 'PRONDAMIN2020'
    df20
    dicPminec2020
except:
    # pronda2021 No Existe
    st.write('pronda2020 NO existe')
    #pronda2021 = []


st.write(pronda2023)
st.write(drive2023)
st.write(p2023)
listdb = [(pronda2023,drive2023,p2023), (pronda2022,drive2022,p2022), (pronda2021,drive2021,p2021), (pronda2020,drive2020,p2020)]

st.write(listadb)
#drive2023 = deta.Drive("minec")
#dicPminec2023 =  drive2023.list()
st.write(dicPminec2023)

Pronda = load_data02()
#sel_col = ['key',  'distrito',  'nombre', 'apellido', 'teléfonos', 'emails']         # List of desired column names
#dfProndaSC = Pronda[sel_col]
dfProndaSC = Pronda
dfProndaSC['notifitelf'] = dfProndaSC['teléfonos'].apply(lambda x: str(x[0]) if x else '')
dfProndaSC['notifitelf'] = dfProndaSC.apply(formatelf, axis=1)
#dfProndaSC['xval'] = '***'
'pronda = ', dfProndaSC
st.stop()
st.write(dfProndaSC['notifitelf'].value_counts())
dfProndaSC['Categoría Actual'] = dfProndaSC['Categoría Actual'].fillna('-')
dfProndaSC['Cédula'] = dfProndaSC['Cédula'].fillna('-')
dfProndaSC['ReporteCertif'] = dfProndaSC['ReporteCertif'].fillna('-')
dfProndaSC['Status'] = dfProndaSC['Status'].fillna('-')
dfProndaSC['close'] = dfProndaSC['close'].fillna('-')
dfProndaSC['condicion'] = dfProndaSC['condicion'].fillna('-')
dfProndaSC['corte-1'] = dfProndaSC['corte-1'].fillna('-')
dfProndaSC['corte-2'] = dfProndaSC['corte-2'].fillna('-')
dfProndaSC['corte-3'] = dfProndaSC['corte-3'].fillna('-')
dfProndaSC['curso'] = dfProndaSC['curso'].fillna('-')
dfProndaSC['lista'] = dfProndaSC['lista'].fillna('-')
dfProndaSC['value'] = dfProndaSC['value'].fillna('-')
'---'
'dfProndaSC = ', dfProndaSC
'---'
#regPronda = dfProndaSC.to_dict('records')
#regPronda

dfProndaSC.drop(columns = ['lista'], inplace=True )
dfProndaSC

# Abre la BD donde se guardaran los nuevos datos normalizados (teléfonos y nombres)
# por ahora solo los teléfonos
# también aquí se incluiran los datos de los certificados y cursos realizados
Pronda24D = deta.Base('Prondamin2024D')
# elimino las columnas innecesarias: 
#    Cédula, Categoría Actual, Status, ReporteCertif, close, condicion, corte-1
#    corte-2, corte-3, lista, curso
dfProndaSC.drop(columns = ['Cédula', 'Categoría Actual', 'Status', 'ReporteCertif',
                           'close', 'condicion', 'corte-1', 'corte-2',
                           'corte-3', 'curso'], inplace=True )

# para grabar en la bd en grupos de 10 registros a la vez
num_registros_por_lista = 10
' dfProndaSC.index = ', dfProndaSC.index

# Crea una columna que represente el número de lista para cada registro
dfProndaSC['lista'] = dfProndaSC.index // num_registros_por_lista
dfProndaSC['lista']
dfProndaSC['lista'].value_counts()

# Divide el DataFrame en grupos basados en la columna 'lista'
grupos = dfProndaSC.groupby('lista')                                          # Ahora puedes acceder a cada grupo individualmente
#grupos

contador = 1
for nombre_lista, grupo in grupos:
    st.write('Lista ', nombre_lista, contador)
    grupo
    reggrupo = grupo.to_dict('records')
    
    if contador < 2:               
        reggrupo
        try:
            Pronda24D.put_many(reggrupo)
            'listo grupo ',str(contador)
        except:
            'error grabando grupo',contador
            reggrupo
            st.stop()
    else: st.stop()
    contador+=1
#-------------------------------

