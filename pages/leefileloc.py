import streamlit as st
import pandas as pd

def main():
    st.title('Cargar y mostrar un archivo CSV')

    # Sección para cargar el archivo CSV
    st.sidebar.title('Cargar archivo CSV')
    uploaded_file = st.sidebar.file_uploader("Selecciona un archivo CSV", type=['csv'])

    # Sección para mostrar el DataFrame
    st.header('Contenido del archivo CSV')

    if uploaded_file is not None:
        # Leer el archivo CSV y mostrar como DataFrame
        df = pd.read_csv(uploaded_file)
        st.write(df)
    else:
        st.write('Carga un archivo CSV utilizando el panel lateral.')

if __name__ == '__main__':
    main()
