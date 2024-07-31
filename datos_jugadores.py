from bs4 import BeautifulSoup
import requests
import time
import json
import pandas as pd

##### LIGA ESPAÑOLA #####
def obtenerEnlacesEquipos():    # Función que devuelve el enlace de cada equipo de La Liga
    url_principal = 'https://www.laliga.com/laliga-easports/clubes'
    peticion = requests.get(url_principal)  # Petición a la página web 
    time.sleep(2)
    sopa = BeautifulSoup(peticion.text, 'lxml') # Todo el contenido de la página
    contenido = sopa.find("div", class_="styled__GridStyled-sc-skzs8h-0 fVbFTE")   
    elementos = contenido.find_all("a", class_="link")  # Buscar en la página los elementos donde están los enlaces
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
        contenido = sopa.find("div", class_="styled__SquadListContainer-sc-sx1q1t-0 hwjXzG")
        elementos = contenido.find_all("a", class_="link")
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
    columnas = ['jugador','apodo','fecha','peso','altura','pais','posicion','equipo','dorsal','url']
    df_jugadores = pd.DataFrame([nombres, apodos, fechas_nacimiento, pesos, alturas, paises, 
                                posiciones, equipos, dorsales, fotos], index=columnas)
    return df_jugadores.T # Se devuelve el dataframe transpuesto

##### PREMIER LEAGUE #####
def obtenerEnlacesEquiposPremier(): # Función que devuelve una lista con los enlaces de los equipos de la Premier League
    url_principal = 'https://www.premierleague.com/clubs'
    peticion = requests.get(url_principal)  # Petición a la página web 
    time.sleep(2)
    sopa = BeautifulSoup(peticion.text, 'lxml') # Todo el contenido de la página
    contenedor = sopa.find("ul", class_="club-list dataContainer")
    enlaces = contenedor.find_all("a")
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
        contenedor = sopa.find('div', class_="wrapper col-12")
        enlaces = contenedor.find_all("a")
        for i in range(len(enlaces)):
            enlace_jugador = enlaces[i].get('href')
            lista_jugadores.append(enlace_jugador)
    return lista_jugadores