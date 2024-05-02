import streamlit as st
import pandas as pd
from deta import Deta

deta = Deta(st.secrets["deta_key"])


ProndaCalifica = deta.Base('jota_db')
itemsProndaCalifica = ProndaCalifica.fetch().items
dfProndaCalifica = pd.DataFrame(itemsProndaCalifica)

dfcMC = dfProndaCalifica.loc[dfProndaCalifica['CURSOREALIZADO'] == 'Ministro Cristiano ']
dfcML = dfProndaCalifica.loc[dfProndaCalifica['CURSOREALIZADO'] == 'Ministro Licenciado ']
dfcMCi = dfcMC.reindex(columns=['CATEGORIA','DISTRITO','NOMBRES','APELLIDOS','CURSOREALIZADO','Total del curso (Real)','STATUS','MODALIDAD','CEDULA','EMAIL','TELEFONO','REPORTECERTIF','key'])
dfcMLi = dfcMC.reindex(columns=['CATEGORIA','DISTRITO','NOMBRES','APELLIDOS','CURSOREALIZADO','Total del curso (Real)','STATUS','MODALIDAD','CEDULA','EMAIL','TELEFONO','REPORTECERTIF','key'])

'Ministros Cristianos Bloque 01 : ', dfcMCi
'---'
'Ministros Licenciados Bloque 01 : ', dfcMLi
