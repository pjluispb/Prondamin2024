
import streamlit as st
import pandas as pd
from deta import Deta
import pygsheets
from google.oauth2 import service_account
import unicodedata
from unidecode import unidecode

deta = Deta(st.secrets["deta_key"])
SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
service_account_info = st.secrets.gcp_service_account
my_credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes = SCOPES)
gc =pygsheets.authorize(custom_credentials=my_credentials)


@st.cache_data
def load_data02():
    Pronda24 = deta.Base('Prondamin2024D')
    res = Pronda24.fetch(limit=500)
    all_items = res.items
    while res.last:
        res = Pronda24.fetch(last=res.last)
        all_items += res.items
    dfall_items = pd.DataFrame(all_items)
    return dfall_items

def update_columns(row):
    try:
        kced = str(row['CEDULA'])
        rcur = row['CURSO']
        if rcur.startswith('ML'):
            curso = 'Ministro Licenciado'
        elif rcur.startswith('MO'):
            curso = 'Ministro Ordenado'
        else:
            curso = 'Ministro Cristiano'
    except:
        st.error('error procesando fila: ', row)
    row['CEDULA']=kced
    row['CURSO']=curso
    return row    

def row_style(row):
    if row['CATEGORIA'].startswith('Ministro Distrital'): cat = '1'
    if row['CATEGORIA'].startswith('Ministro Cristiano'): cat = '2'
    if row['CATEGORIA'].startswith('Ministro Licenciado'): cat = '3'
    if row['CATEGORIA'].startswith('Ministro Ordenado'): cat = '4'
    if row['CURSOREALIZADO']=='Ministro Cristiano': cur = '1'
    if row['CURSOREALIZADO']=='Ministro Licenciado': cur = '2'
    if row['CURSOREALIZADO']=='Ministro Ordenado': cur = '3'
    catcur = cat+cur
    if catcur not in ['11', '22', '33']:
        return pd.Series('background-color: #fdd834; color:#000000', row.index)
    else:
        return pd.Series('', row.index)
    
acceso = st.text_input('clave de acceso : ', type='password')
if acceso == 'j0tA':

    sh1 = gc.open('falconPresencial')
    sh2 = gc.open('yaracuyPresencial')
    #--------------------------------------------------------------------------
    dfPronda = load_data02()
    dfPronda.drop(columns=['lista'], inplace=True)
    dfPronda['EMAIL'] = dfPronda['EMAIL'].apply(lambda x: str(x[0]) if x else '')
    #'pronda = ', dfPronda

    if st.button("Clear All"):
        # Clear values from *all* all in-memory and on-disk data caches:
        # i.e. clear values from both square and cube
        st.cache_data.clear()

    #----------carga las calificaciones del Presencial FALCON----------
    #dfpfalcon= pd.read_csv('C:/Users/user/OneDrive/Desktop/python/minec2024/calificaciones/falconPresencial.csv', delimiter=';')
    wks1 = sh1[0]
    dfpfalcon = wks1.get_as_df()
    dfpfalcon = dfpfalcon.apply(update_columns, axis=1)
    #dfpfalcon
    #----------mezcla el csv con el Pronda y muestra los resultados
    result = pd.merge( dfpfalcon, dfPronda, on='CEDULA', how='left')

    result['STATUS'] = result['RESULTADO']
    result['CURSOREALIZADO'] = result['CURSO']
    result['MODALIDAD'] = 'Presencial'
    result.drop(columns=['CURSO', 'RESULTADO'], inplace=True)
    #'result = ', result

    resultcol = result.style.apply(row_style, axis=1)  #Coloriza las filas
    '---'
    'Resultados Presencial Falcón'
    resultcol

    #-----------------------------------------------------------------------------
        #----------carga las calificaciones del Presencial YARACUY----------
    #dfpyaracuy= pd.read_csv('C:/Users/user/OneDrive/Desktop/python/minec2024/calificaciones/yaracuyPresencial.csv', delimiter=';')
    wks2 = sh2[0]
    dfpyaracuy = wks2.get_as_df()
    dfpyaracuy = dfpyaracuy.apply(update_columns, axis=1)
    #dfpyaracuy
    #----------mezcla el csv con el Pronda y muestra los resultados
    resulty = pd.merge( dfpyaracuy, dfPronda, on='CEDULA', how='left')
    
    resulty['STATUS'] = resulty['RESULTADO']
    resulty['CURSOREALIZADO'] = resulty['CURSO']
    resulty['MODALIDAD'] = 'Presencial'
    resulty.drop(columns=['CURSO', 'RESULTADO'], inplace=True)
    #resulty

    resultycol = resulty.style.apply(row_style, axis=1)  #Coloriza las filas
    '---'
    'Resultados Presencial Yaracuy'
    resultycol


    st.page_link("home2024.py", label="Inicio", icon="🏠")

else:
    # st.error('acceso inválido')
    
    st.caption('clave de acceso inválida')
    st.caption('intente nuevamente o vuelva al inicio')
    st.page_link("home2024.py", label="Inicio", icon="🏠")
