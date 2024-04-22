import pandas as pd
import streamlit as st
from deta import Deta

deta = Deta(st.secrets["deta_key"])

#--------------------------------------------------
# para eliminar(1ro) y luego crear(put) registros en Pronda
Pronda = deta.Base('Prondamin2024C')
Pronda.delete("92ttxhdnjfnt")
# reg = {.....}
#Pronda.put(reg)
#--------------------------------------------------
