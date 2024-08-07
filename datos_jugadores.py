from bs4 import BeautifulSoup
import requests
import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
opciones = webdriver.ChromeOptions()
opciones.add_experimental_option('excludeSwitches', ['enable-logging'])

##### LIGA ESPAÑOLA #####
def obtenerEnlacesEquipos():    # Función que devuelve el enlace de cada equipo de La Liga
    url_principal = 'https://www.laliga.com/laliga-easports/clubes'
    peticion = requests.get(url_principal)  # Petición a la página web 
    time.sleep(2)
    sopa = BeautifulSoup(peticion.text, 'lxml') # Todo el contenido de la página
    contenido = sopa.find('div', class_='styled__GridStyled-sc-skzs8h-0 fVbFTE')   
    elementos = contenido.find_all('a', class_='link')  # Buscar en la página los elementos donde están los enlaces
    enlaces_equipos = []
    for i in range(len(elementos)):
        enlace = elementos[i].get('href')   # Obtener los enlaces del atributo href
        enlaces_equipos.append(enlace)
    return enlaces_equipos

def obtenerEnlacesJugadores():  # Función que devuelve el enlace de cada jugador de La Liga
    enlaces_jugadores = []
    enlaces_equipos = obtenerEnlacesEquipos()
    for i in range(len(enlaces_equipos)):
        url_equipo = 'https://www.laliga.com' + enlaces_equipos[i] + '/plantilla'
        peticion = requests.get(url_equipo)
        time.sleep(2)
        sopa = BeautifulSoup(peticion.text, 'lxml')
        contenido = sopa.find('div', class_='styled__SquadListContainer-sc-sx1q1t-0 hwjXzG')
        elementos = contenido.find_all('a', class_='link')
        for i in range(len(elementos)):
            enlace_jugador = elementos[i].get('href')
            enlaces_jugadores.append(enlace_jugador)
    return enlaces_jugadores

def obtenerDatosJugadores(enlaces_jugadores):    # Función que devuelve un dataframe con los datos de todos los jugadores de La Liga
    nombres = []
    apodos = []
    fechas_nacimiento = []
    pesos = []
    alturas = []
    paises = []
    posiciones = []
    equipos = []
    dorsales = []
    fotos = []
    for i in range(len(enlaces_jugadores)):
        url_jugador = 'https://www.laliga.com' + enlaces_jugadores[i]
        peticion = requests.get(url_jugador)    # Petición a la página web
        time.sleep(2)
        sopa = BeautifulSoup(peticion.text, 'lxml') # Contenido de la web
        script_jugador = sopa.find_all('script', id='__NEXT_DATA__')
        script_jugador = script_jugador[0].string   # Script con los datos del jugador
        dicc_jugador = json.loads(script_jugador)   # Pasar la cadena de caracteres a un formato más legible
        dicc_jugador = dicc_jugador['props']['pageProps']['player'] # Obtener el diccionario del jugador
        lista_claves = list(dicc_jugador.keys())    # Lista con las claves del diccionario
        posicion = dicc_jugador['squad']['position']['name']    
        if posicion == 'Entrenador': # En principio no nos interesa la informacion de los entrenadores
            pass
        else:
            if 'name' in lista_claves:
                nombre = dicc_jugador['name']
            else: 
                nombre = ''
            if 'nickname' in lista_claves:
                apodo = dicc_jugador['nickname']
            else:
                apodo = ''
            if 'date_of_birth' in lista_claves:
                fecha_nacimiento = dicc_jugador['date_of_birth']
            else: 
                fecha_nacimiento = ''
            if 'weight' in lista_claves:
                peso = dicc_jugador['weight']
            else:
                peso = 0
            if 'height' in lista_claves:
                altura = dicc_jugador['height']
            else: 
                altura = 0
            equipo = dicc_jugador['team']['name']   
            pais = dicc_jugador['country']['id']
            try:
                dorsal = dicc_jugador['squad']['shirt_number']
            except: dorsal = ''
            if 'photos' in lista_claves:
                foto = (dicc_jugador['photos']['001']['256x278'])
            else:
                foto = ''
            nombres.append(nombre)
            apodos.append(apodo)
            fechas_nacimiento.append(fecha_nacimiento)
            pesos.append(peso)
            alturas.append(altura)
            paises.append(pais)
            posiciones.append(posicion)
            equipos.append(equipo)
            dorsales.append(dorsal)
            fotos.append(foto)  # Final del bucle FOR
    columnas = ['jugador', 'apodo', 'fecha', 'peso', 'altura', 'pais', 'posicion', 'equipo', 'dorsal', 'url']
    df_jugadores = pd.DataFrame([nombres, apodos, fechas_nacimiento, pesos, alturas, paises, 
                                posiciones, equipos, dorsales, fotos], index=columnas)
    return df_jugadores.T # Se devuelve el dataframe transpuesto

##### PREMIER LEAGUE #####
def obtenerEnlacesEquiposPremier(): # Función que devuelve una lista con los enlaces de los equipos de la Premier League
    url_principal = 'https://www.premierleague.com/clubs'
    peticion = requests.get(url_principal)  # Petición a la página web 
    time.sleep(2)
    sopa = BeautifulSoup(peticion.text, 'lxml') # Todo el contenido de la página
    contenedor = sopa.find('ul', class_='club-list dataContainer')
    enlaces = contenedor.find_all('a')
    lista_enlaces = []
    for i in range(len(enlaces)):
        enlace = enlaces[i].get('href')
        enlace = enlace.replace('overview', 'squad')
        lista_enlaces.append(enlace)
    return lista_enlaces

def obtenerEnlacesJugadoresPremier():   # Función que devuelve el enlace de cada jugador de la Premier League
    lista_jugadores = []
    enlaces_equipos = obtenerEnlacesEquiposPremier()
    for i in range(len(enlaces_equipos)):
        url_equipo = 'https://www.premierleague.com' + enlaces_equipos[i]
        time.sleep(2)
        peticion = requests.get(url_equipo)
        sopa = BeautifulSoup(peticion.text, 'lxml')
        contenedor = sopa.find('div', class_='wrapper col-12')
        enlaces = contenedor.find_all('a')
        for i in range(len(enlaces)):
            enlace_jugador = enlaces[i].get('href')
            lista_jugadores.append(enlace_jugador)
    return lista_jugadores

def obtenerDatosJugadoresPremier(): # Función que devuelve un dataframe con los datos de los jugadores de la Premier League
    nombres = []
    equipos = []
    dorsales = []
    posiciones = []
    paises = []
    fotos = []
    urls_equipos = obtenerEnlacesEquiposPremier()   # Llamada a la función para obtener los enlaces de los equipos
    for i in range(len(urls_equipos)):  # Primer bucle For para cada equipo
        url_equipo = 'https://www.premierleague.com' + urls_equipos[i]
        ruta = Service(executable_path=r'/Users/sergi/Desktop/Proyectos/ChromeDriver/chromedriver.exe')
        driver = webdriver.Chrome(service=ruta, options=opciones)
        driver.get(url_equipo)  # Para poder acceder a la url de las imágenes
        imagenes = driver.find_elements(By.XPATH, '//*[@id="mainContent"]/div[3]/div/ul/div/ul/li/a/div/div/div[3]/img')
        peticion = requests.get(url_equipo) # Para acceder a los demás datos de los jugadores
        sopa = BeautifulSoup(peticion.text, 'lxml')
        equipo = sopa.find('h2', class_='club-header__team-name').get_text()
        contenedor = sopa.findAll('div', class_='stats-card__container')    # Aquí se encuentran los datos de los jugadores
        time.sleep(2)
        for i in range(len(contenedor)):    # Segundo bucle For para cada contenedor de cada jugador
            if(contenedor[i].find('div', class_='stats-card__player-first') != None):
                nombre = contenedor[i].find('div', class_='stats-card__player-first').get_text()
            else:
                nombre = ''
            if(contenedor[i].find('div', class_='stats-card__player-last') != None):
                apellido = contenedor[i].find('div', class_='stats-card__player-last').get_text()
            else:
                apellido = ''
            nombre_apellido = nombre + apellido
            if(contenedor[i].find('div', class_='stats-card__squad-number u-hide-mob-l') != None):
                dorsal = contenedor[i].find('div', class_='stats-card__squad-number u-hide-mob-l').get_text()
            else:
                dorsal = ''
            if(contenedor[i].find('div', class_='stats-card__player-position') != None):
                posicion = contenedor[i].find('div', class_='stats-card__player-position').get_text()
            else:
                posicion = ''
            if(contenedor[i].find('span', class_='stats-card__player-country') != None):
                pais = contenedor[i].find('span', class_='stats-card__player-country').get_text()
            else:
                pais = ''
            url_foto = imagenes[i].get_attribute('src')
            nombres.append(nombre_apellido)
            equipos.append(equipo)
            dorsales.append(dorsal)
            posiciones.append(posicion)
            paises.append(pais)
            fotos.append(url_foto)  # Final del segundo bucle For
    # Final del primer bucle For
    # Crear un dataframe con los datos obtenidos
    columnas = ['jugador', 'equipo', 'dorsal', 'posicion', 'pais', 'url']
    df_jugadores = pd.DataFrame([nombres, equipos, dorsales, posiciones, paises, fotos], index=columnas)
    return df_jugadores.T
        
##### BUNDESLIGA #####
def obtenerEnlacesEquiposBundesliga():    # Función que devuelve el enlace de cada equipo de la Bundesliga
    url_principal = 'https://www.bundesliga.com/de/bundesliga/clubs'
    peticion = requests.get(url_principal)  # Petición a la página web 
    time.sleep(2)
    sopa = BeautifulSoup(peticion.text, 'lxml') # Todo el contenido de la página
    contenido = sopa.find('div', class_='clubs grid')   
    elementos = contenido.find_all('a')  # Buscar en la página los elementos donde están los enlaces
    enlaces_equipos = []
    for i in range(len(elementos)):
        enlace = elementos[i].get('href')   # Obtener los enlaces del atributo href
        enlaces_equipos.append(enlace)
    return enlaces_equipos

def obtenerEnlacesJugadoresBundesliga():  # Función que devuelve el enlace de cada jugador de la Bundesliga
    enlaces_jugadores = []
    enlaces_equipos = obtenerEnlacesEquiposBundesliga()
    for i in range(len(enlaces_equipos)):
        url_equipo = 'https://www.bundesliga.com' + enlaces_equipos[i]
        if url_equipo == 'https://www.bundesliga.com/de/bundesliga/clubs/sc-freiburg':
            pass    # Este enlace no está disponible actualmente
        else:
            peticion = requests.get(url_equipo)
            time.sleep(4)
            sopa = BeautifulSoup(peticion.text, 'lxml')
            contenido = sopa.find('div', class_='container ng-star-inserted') # Aquí se encuentran todos los jugadores
            elementos = contenido.find_all('a')
            for i in range(len(elementos)):
                enlace_jugador = elementos[i].get('href')
                enlaces_jugadores.append(enlace_jugador)
    return enlaces_jugadores

def obtenerDatosJugadoresBundesliga():  # Función que devuelve un dataframe con los datos de los jugadores de la Bundesliga
    jugadores_bdl = obtenerEnlacesJugadoresBundesliga()
    columnas = {'nombre': [], 'dorsal': [], 'Club': [], 'Position': [], 'Geburtstag': [], 'Nationalität': [], 'Größe': [], 'Gewicht': [], 'foto': []}
    df_jugadores = pd.DataFrame.from_dict(columnas) # Dataframe para almacenar a todos los jugadores
    for i in range(len(jugadores_bdl)):
        lista_columnas = ['nombre', 'dorsal','foto']
        lista_valores = []
        url_jugador = 'https://www.bundesliga.com' + jugadores_bdl[i]
        peticion = requests.get(url_jugador)
        time.sleep(3)
        sopa = BeautifulSoup(peticion.text, 'lxml')
        contenido = sopa.find('header', class_='header container-fluid')    # Aquí se encuentran todos los datos del jugador
        try:
            nombre = contenido.find('div', class_='firstName').get_text()
        except:
            nombre = ''
        try:
            apellido = contenido.find('div', class_='lastName').get_text()
        except:
            apellido = ''
        nombre = nombre + ' ' + apellido
        lista_valores.append(nombre)
        try:
            dorsal = contenido.find('div', class_='shirtNumber ng-star-inserted').get_text()
        except:
            dorsal = 0
        lista_valores.append(dorsal)
        try:
            imagen = contenido.find('div', class_='playerImage')    # Aquí se encuentra la imagen del jugador
            url_imagen = imagen.find('img').get('src')
        except:
            url_imagen = ''
        lista_valores.append(url_imagen)
        etiquetas = contenido.find_all('span', class_='label')
        valores = contenido.find_all('span', class_='value')
        for i in range(len(etiquetas)): # Para guardar las columnas disponibles de cada jugador
            lista_columnas.append(etiquetas[i].get_text())
        for i in range(len(valores)):   # Para guardar los valores disponibles en la web de cada jugador
            lista_valores.append(valores[i].get_text())
        nueva_fila = dict(zip(lista_columnas, lista_valores))
        df_jugadores = pd.concat([df_jugadores, pd.DataFrame([nueva_fila])], ignore_index=True) # Añadir la nueva fila al dataframe
    df_jugadores = df_jugadores.rename(columns={'Club': 'equipo', 'Position': 'posicion', 'Geburtstag': 'fecha', 'Nationalität': 'pais', 
                                            'Größe': 'altura', 'Gewicht': 'peso'})
    return df_jugadores

##### SERIE A #####
def obtenerEnlacesEquiposSerieA():  # Función que devuelve una lista con los enlaces de los equipos de la Serie A
    url_principal = 'https://www.legaseriea.it/it'
    ruta = Service(executable_path=r'/Users/sergi/Desktop/Proyectos/ChromeDriver/chromedriver.exe')
    driver = webdriver.Chrome(service=ruta, options=opciones)
    driver.get(url_principal)  
    time.sleep(3)
    sopa = BeautifulSoup(driver.page_source, 'lxml')
    tabla_equipos = sopa.find('div', class_='tab-content')
    filas_equipos = tabla_equipos.find_all('a')
    enlaces_equipos = []
    for i in range(len(filas_equipos)):   
        enlace = filas_equipos[i].get('href')
        enlaces_equipos.append(enlace)
    driver.close()
    return enlaces_equipos
