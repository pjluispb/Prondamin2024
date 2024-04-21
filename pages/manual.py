import pandas as pd
import streamlit as st
from deta import Deta

deta = Deta(st.secrets["deta_key"])
Pronda = deta.Base('Prondamin2024C')

# Pronda.delete(" 10126173")

reg = {
	"key": "15733073",
	"ReporteCertif": "-",
	"Status": "-",
	"apellido": "Rengifo",
	"categoría": "Ministro Licenciado",
	"distrito": "Nor Oriente",
	"emails": [
		"erengifom@yahoo.com"
	],
	"fechaPago": "-",
	"fuenteOrigen": "-",
	"modalidad": "-",
	"montoApagar": "-",
	"montoPago": "-",
	"nombre": "Eduardo",
	"paycon": "NO",
	"referenciaPago": "-",
	"teléfonos": [
		"04128643490"
	]
}
Pronda.put(reg)

