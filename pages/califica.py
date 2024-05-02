import streamlit as st
import pandas as pd
from deta import Deta

deta = Deta(st.secrets["deta_key"])


ProndaCalifica = deta.Base('jota_db')
itemsProndaCalifica = ProndaCalifica.fetch().items
dfProndaCalifica = pd.DataFrame(itemsProndaCalifica)

dfcMC = dfProndaCalifica.loc[dfProndaCalifica['CURSOREALIZADO'] == 'Ministro Cristiano ']
dfcML = dfProndaCalifica.loc[dfProndaCalifica['CURSOREALIZADO'] == 'Ministro Licenciado ']
dfcMO = dfProndaCalifica.loc[dfProndaCalifica['CURSOREALIZADO'] == 'Ministro Ordenado ']
dfcMCi = dfcMC.reindex(columns=['CATEGORIA','DISTRITO','NOMBRES','APELLIDOS','CURSOREALIZADO','Total del curso (Real)','STATUS','MODALIDAD','CEDULA','EMAIL','TELEFONO','REPORTECERTIF','key'])
dfcMLi = dfcML.reindex(columns=['CATEGORIA','DISTRITO','NOMBRES','APELLIDOS','CURSOREALIZADO','Total del curso (Real)','STATUS','MODALIDAD','CEDULA','EMAIL','TELEFONO','REPORTECERTIF','key'])
dfcMOi = dfcMO.reindex(columns=['CATEGORIA','DISTRITO','NOMBRES','APELLIDOS','CURSOREALIZADO','Total del curso (Real)','STATUS','MODALIDAD','CEDULA','EMAIL','TELEFONO','REPORTECERTIF','key'])

'Ministros Cristianos Bloque 01 : ', dfcMCi
col1, col2 = st.columns(2)
col1.write(dfcMCi['DISTRITO'].value_counts())
col2.write(dfcMCi['Total del curso (Real)'].value_counts())
'---'
'Ministros Licenciados Bloque 01 : ', dfcMLi
col3, col4 = st.columns(2)
col3.write(dfcMLi['DISTRITO'].value_counts())
col4.write(dfcMLi['Total del curso (Real)'].value_counts())
'---'
'Ministros Ordenados Bloque 01 : ', dfcMOi
col3, col4 = st.columns(2)
col3.write(dfcMOi['DISTRITO'].value_counts())
col4.write(dfcMOi['Total del curso (Real)'].value_counts())
'---'

