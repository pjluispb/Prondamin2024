import streamlit as st
import pandas as pd
from deta import Deta
from PIL import Image

st.set_page_config(
    page_title="Minec Reg App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

deta = Deta(st.secrets["deta_key"])
