import pandas as pd
from deta import Deta
import streamlit as st

deta = Deta(st.secrets.deta_key)

st.set_page_config(
    page_title="Minec Reg App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

pronda2024 = deta.Base('Prondamin2024B')
p24 = pronda2024.fetch(limit=5000)
dfp24 = pd.DataFrame(p24.items)

dfp24