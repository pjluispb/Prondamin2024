import streamlit as st
import pandas as pd
from deta import Deta

deta = Deta(st.secrets["deta_key"])


ProndaCalifica = deta.Base('jota_db')
itemsProndaCalifica = ProndaCalifica.fetch().items
dfProndaCalifica = pd.DataFrame(itemsProndaCalifica)

dfcMC = dfProndaCalifica.loc[dfProndaCalifica['CURSOREALIZADO'] == 'Ministro Cristiano ']
dfcML = dfProndaCalifica.loc[dfProndaCalifica['CURSOREALIZADO'] == 'Ministro Licenciado ']

'Ministros Cristianos Bloque 01 : ', dfcMC
'---'
'Ministros Licenciados Bloque 01 : ', dfcML
