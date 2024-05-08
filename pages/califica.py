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

'Ministros Cristianos Bloque 01 y 02 : ', dfcMCi
col1, col2, col3 = st.columns(3)
col1.write(dfcMCi['DISTRITO'].value_counts())
col2.write(dfcMCi['STATUS'].value_counts())
col3.write(dfcMCi['Total del curso (Real)'].value_counts())
'---'
'Ministros Licenciados Bloque 01 y 02 : ', dfcMLi
col4, col5, col6 = st.columns(3)
col4.write(dfcMLi['DISTRITO'].value_counts())
col5.write(dfcMLi['STATUS'].value_counts())
col6.write(dfcMLi['Total del curso (Real)'].value_counts())
'---'
'Ministros Ordenados Bloque 01 y 02 : ', dfcMOi
col7, col8, col9 = st.columns(3)
col7.write(dfcMOi['DISTRITO'].value_counts())
col8.write(dfcMOi['STATUS'].value_counts())
col9.write(dfcMOi['Total del curso (Real)'].value_counts())
'---'

