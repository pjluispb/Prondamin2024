import pandas as pd
import streamlit as st
from deta import Deta

deta = Deta(st.secrets["deta_key"])
Pronda = deta.Base('Prondamin2024C')

# Pronda.delete(" 10126173")

reg = {
	"key": "10126173",
	"ReporteCertif": "S/A",
	"Status": "S/A",
	"apellido": "Betancourt de Luna",
	"categoría": "Ministro Cristiano",
	"distrito": "Lara",
	"emails": [
		"-"
	],
	"fechaPago": "-",
	"fuenteOrigen": "-",
	"modalidad": "-",
	"montoApagar": "-",
	"montoPago": "-",
	"nombre": "Ana Maritza",
	"paycon": "NO",
	"referenciaPago": "-",
	"teléfonos": [
		"-"
	]
}

Pronda.put(reg)

