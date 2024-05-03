
import streamlit as st
from deta import Deta
from PIL import Image

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

st.set_page_config(
    page_title="Minec Reg App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def muestraCert(nombre,cedula, drive):
    nnyced = ''
    for arch in drive.list()['names']:
        if cedula in arch:
            nnyced = arch
            #print('cedula ',cedula, ' encontrada en minec2024 en: ', arch)
            break
    imag = drive.get(nnyced)
    try:
        st.image(imag.read())
        st.success('Para :red[**guardar**] la 👆imagen👆 de tu certificado👆 en tu :orange[**computadora**]💻, _puedes hacer clic con el **botón derecho** sobre la 👆imagen👆, y elegir en el **menú contextual** la opción de :blue[**imprimir**]🖨️ o :blue[**guardar imagen como**]_.📂 $\\newline$ En caso de que lo hagas desde una :orange[**tablet o un celular**]📱, manten la imagen _presionada_ y te aparecerá un **_menú contextual_** con las opciones de :blue[**agregar a fotos**]🖼️ (_que descargará el certificado en la carpeta :red[**Fotos**] de tu dispositivo_), :blue[**compartir**]✉️ (_que te permitirá enviarlo a un correo electrónico, Whatsapp, Telegram, Drive, etc_) y la de :blue[**copiar**] (_lo copia en memoria para pegarlo en otra aplicación tal como Powerpoint, Notas, etc_)')
    except:
        for nomima in drive.list()["names"]:
            if cedula in nomima:
                nnyced = nomima
                st.write('=====>>'+nnyced)
                imag = drive.get(nnyced)
            else:
                #st.write(drive.list()["names"])
                for certifi in drive.list()["names"]:
                    if certifi.find('Error')!=-1:
                        st.write('---')
                        st.write(certifi)
                        st.stop()
                # if cedula == '10867892':
                #     #nnyced = 'MariaConsueloAnguloDeLozada10867892.png'
                #     nnyced = 'MariaAngulo10868892Error.png'
                #     st.write(nnyced)
                #     st.stop()
        #st.image(imag.read())
        st.success('Para :red[**guardar**] la 👆imagen👆 de tu certificado👆 en tu :orange[**computadora**]💻, _puedes hacer clic con el **botón derecho** sobre la 👆imagen👆, y elegir en el **menú contextual** la opción de :blue[**imprimir**]🖨️ o :blue[**guardar imagen como**]_.📂 $\\newline$ En caso de que lo hagas desde una :orange[**tablet o un celular**]📱, manten la imagen _presionada_ y te aparecerá un **_menú contextual_** con las opciones de :blue[**agregar a fotos**]🖼️ (_que descargará en la carpeta :red[**Fotos**] de tu dispositivo_), :blue[**compartir**]✉️ (_que te permitirá enviarlo a un correo electrónico, Whatsapp, Telegram, Drive, etc_) y la de :blue[**copiar**] (_lo copia en memoria para pegarlo en otra aplicación tal como Powerpoint, Notas, etc_)')
        # st.error('''
        # Lo sentimos, ha ocurrido un error de carga en relación a su certificado.
        # Por favor reportelo al coordinador distrital de Minec, e inténtelo después
        # ''')

def procesar_lista(lista):
    nombreU = None
    aprobados = []
    reprobados = []
    for tupla in lista:
        #st.write('---')
        #tupla
        if tupla is not None:
            if nombreU is None:
                nombreU = tupla['NOMBRES']+' '+tupla['APELLIDOS']
                cedulaU = tupla['CEDULA']
                # st.write(nombreU)
            if tupla['STATUS'] == 'APROBADO':
                # Raprobados.append((tupla['CURSOREALIZADO'],tupla[4]))
                aprobados.append((tupla['CURSOREALIZADO'], tupla['PERIODO'], tupla['DRIVE']))
            else:
                reprobados.append((tupla['CURSOREALIZADO'], tupla['PERIODO'], tupla['DRIVE']))
                #st.error(f"Reprobaste el curso de {tupla['CURSOREALIZADO']} correspondiente al {tupla['PERIODO']}")
    # st.write(2*'\n','\t Aprobados : ', aprobados, '\n')
    if nombreU is not None:
        msg0a = ' Estimado ministro '
        msg0b = nombreU
        msg1 = '**$\\LARGE✨Felicitaciones✨\\newline$** $\\newline$ por haber realizado y aprobado los cursos de : .$\\newline$ '
        if len(aprobados)>0:
            # msg2 =' Haz aprobado los siguientes cursos: '
            msg3 = '\t'
            for cura in aprobados:
                msg3+=' $\space$ 🔹 :orange['+cura[0]+'] 🔹 del periodo/cohorte de :violet[**'+cura[1]+'**]   $\\newline$'
        else:
            msg3 = 'No tiene cursos APROBADOS'
        if len(reprobados)>0:
            msg6 = '\t'
            for cura in reprobados:
                msg6+='Lamentablemente NO aprobaste el curso de '+cura[0]+'correspondiente al '+cura[1]+'  '
        else:
            msg6 = ''
        st.subheader(msg0a)
        st.header(msg0b)
        if len(aprobados)>0: st.markdown(msg1)
        #st.markdown(msg2)
        if msg3!='':st.markdown(msg3)
        if msg6!='': st.error(msg6)
        bcont = 10
        for cap in aprobados:
            bcont+=10
            bot = st.button(label='Ver certificado del curso '+cap[0]+' de la cohorte '+cap[1],key=nombreU+str(bcont))
            if bot: muestraCert(nombreU, cedulaU,cap[2])
    #     cursosA=[a[0] for a in aprobados]
    #     drivesA=[a[1] for a in aprobados]
    #     st.write(f"Felicidades, has aprobado los cursos de {cursosA}. Aquí tienes acceso a tu certificado: certificado/{drivesA}.pdf")
    #     st.write(f"Felicidades, has aprobado los cursos de {', '.join(cursosA)}. Aquí tienes acceso a tu certificado: certificado/{drivesA}.pdf")
        #for t in drivesA:

    else:
        st.error("No se encontró este número de cédula en nuestros registros de certificados")


deta = Deta(st.secrets["deta_key"])
listdb = []

try:  #obtiene pronda2023 y su drive
    pronda2024 = deta.Base('jota_db')
    drive2024 = deta.Drive("minec2024")
    dicPminec2024 =  drive2024.list()
    
    p2024 = 'PRONDAMIN2024'
except:
    st.write('********Error conectando con Prondamin2023-Final y el drive minec')

try:  #obtiene pronda2023 y su drive
    pronda2023 = deta.Base('PRONDAMIN2023-Final')
    drive2023 = deta.Drive("minec")
    dicPminec2023 =  drive2023.list()
    p2023 = 'PRONDAMIN2023'
except:
    st.write('********Error conectando con Prondamin2023-Final y el drive minec')
try:  #obtiene pronda2022 y su drive
    pronda2022 = deta.Base('PRONDANMIN-2022')
    drive2022 = deta.Drive("minec2022")
    dicPminec2022 =  drive2022.list()
    p2022 = 'PRONDAMIN2022'
except:
    st.write('*/*/*/*/*/*/*/')
try:  #obtiene pronda2021 y su drive
    pronda2021 = deta.Base('PRONDANMIN-2021')
    drive2021 = deta.Drive("minec2021")
    dicPminec2021 =  drive2022.list()
    p2021 = 'PRONDAMIN2021'
    #st.write(pronda2021.fetch().items)
except:
    st.write('pronda2021 NO existe')
try:  #obtiene pronda2020 y su drive
    pronda2020 = deta.Base('PRONDANMIN-2020')
    drive2020 = deta.Drive("minec2020")
    dicPminec2020 =  drive2020.list()
    p2020 = 'PRONDAMIN2020'
except:
    # pronda2021 No Existe
    st.write('pronda2020 NO existe')
    #pronda2021 = []


listdb = [(pronda2024,drive2024,p2024), (pronda2023,drive2023,p2023), (pronda2022,drive2022,p2022), (pronda2021,drive2021,p2021), (pronda2020,drive2020,p2020)]

st.image(imagen1)
st.image(imagen2)
st.subheader(' Módulo de Consulta de Certificados MINEC')
#cedula = st.text_input('Introduce tu cedula')

cedula = st.session_state['cedulaministro']
#cedula = '10070077'
if cedula!='':
    regCedXyear = []
    for (db,dr,pcur) in listdb:
        breg = db.get(key=cedula)
        if breg!=None: 
            breg['DRIVE']=dr
            breg['PERIODO']=pcur
        # st.write(breg)
        # st.write(type(breg))
        regCedXyear.append(breg)
    # regCedXyear
    # st.write(type(regCedXyear))
    procesar_lista(regCedXyear)


st.page_link("home2024.py", label="Inicio", icon="🏠")
