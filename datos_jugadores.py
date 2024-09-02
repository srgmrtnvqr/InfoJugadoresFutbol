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

# Webdriver
def obtenerWebDriver():
    ruta = Service(executable_path=r'/Users/sergi/Desktop/Proyectos/ChromeDriver/chromedriver.exe')
    driver = webdriver.Chrome(service=ruta, options=opciones)
    return driver

##### LIGA ESPAÑOLA #####
def obtenerEnlacesEquiposLaLiga():    # Función que devuelve el enlace de cada equipo de La Liga
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

def obtenerEnlacesJugadoresLaLiga():  # Función que devuelve el enlace de cada jugador de La Liga
    enlaces_jugadores = []
    enlaces_equipos = obtenerEnlacesEquiposLaLiga()
    for i in range(len(enlaces_equipos)):
        url_equipo = 'https://www.laliga.com' + enlaces_equipos[i]
        driver = obtenerWebDriver()
        driver.get(url_equipo)  
        time.sleep(3)
        sopa = BeautifulSoup(driver.page_source, 'lxml')
        contenido = sopa.find('div', class_='styled__SquadListContainer-sc-sx1q1t-0 hwjXzG')
        elementos = contenido.find_all('a', class_='link')
        for i in range(len(elementos)):
            enlace_jugador = elementos[i].get('href')
            enlaces_jugadores.append(enlace_jugador)
    return enlaces_jugadores

def obtenerDatosJugadoresLaLiga():    # Función que devuelve un dataframe con los datos de todos los jugadores de La Liga
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
    enlaces_jugadores = obtenerEnlacesJugadoresLaLiga()
    for i in range(len(enlaces_jugadores)):
        url_jugador = 'https://www.laliga.com' + enlaces_jugadores[i]
        peticion = requests.get(url_jugador)    # Petición a la página web
        time.sleep(2)
        sopa = BeautifulSoup(peticion.text, 'lxml') # Contenido de la web
        script_jugador = sopa.find_all('script', id='__NEXT_DATA__')
        try:
            script_jugador = script_jugador[0].string   # Script con los datos del jugador
            dicc_jugador = json.loads(script_jugador)   # Pasar la cadena de caracteres a un formato más legible
            dicc_jugador = dicc_jugador['props']['pageProps']['player'] # Obtener el diccionario del jugador
            lista_claves = list(dicc_jugador.keys())    # Lista con las claves del diccionario
            try:
                posicion = dicc_jugador['squad']['position']['name']  
            except:
                posicion = ''
            try:
                pais = sopa.find('p', class_='styled__TextStyled-sc-1mby3k1-0 iBRpyN').get_text()   # Aquí está el nombre completo del país
            except:
                pais = ''  
            if((posicion == 'Entrenador')|(posicion == 'Segundo entrenador')): # En principio no nos interesa la informacion de los entrenadores
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
                #pais = dicc_jugador['country']['id']   # Ahora este dato se obtiene antes
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
        except:
            pass
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
        driver = obtenerWebDriver()
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
            try:
                url_foto = imagenes[i].get_attribute('src')
            except:
                url_foto = ''
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
        try:
            etiquetas = contenido.find_all('span', class_='label')
            valores = contenido.find_all('span', class_='value')
        except: pass
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
    driver = obtenerWebDriver()
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

def obtenerDatosJugadoresSerieA():
    url_jugadores = 'https://www.legaseriea.it/it/serie-a/calciatori'
    driver = obtenerWebDriver()
    driver.get(url_jugadores)  
    time.sleep(3)
    # Navegar hacia abajo en la web
    tamaño = driver.execute_script("return window.screen.height;")  # Tamaño de la parte visible de la página
    i = 1
    while True:
        driver.execute_script(f"window.scrollTo(0, {tamaño * i});")
        i += 1
        time.sleep(2)   # Pausa entre cada bajada
        tamaño_total = driver.execute_script("return document.body.scrollHeight;")  # Tamaño de la parte donde se encuentran todos los jugadores
        if tamaño * i > tamaño_total:  # Para comprobar si se ha llegado al final de la página
            break
    sopa = BeautifulSoup(driver.page_source, "lxml")
    contenido = sopa.find('tbody', class_='hm-tbody')   
    elementos = contenido.find_all('tr')  # Buscar en la página los elementos donde están los enlaces
    imagenes = []
    nombres = []
    equipos = []
    posiciones = []
    fechas = []
    paises = []
    for i in range(len(elementos)):
        imagen = elementos[i].find('img', class_='player-img align-self-end').get('src')
        imagenes.append(imagen)
        nombre = elementos[i].find('h3').get_text()
        nombres.append(nombre)
        equipo = elementos[i].find('h3', class_='medium black text-capitalize').get_text()
        equipos.append(equipo)
        posicion = elementos[i].find('h3', class_='regular black text-capitalize d-lg-block d-none').get_text()
        posiciones.append(posicion)
        fecha = elementos[i].find('h3', class_='regular black').get_text()
        fechas.append(fecha)
        pais = elementos[i].find('h3', class_='regular black text-capitalize').get_text()
        paises.append(pais)
    driver.close()
    columnas = ['jugador', 'equipo', 'posicion', 'pais', 'fecha', 'foto']
    df_jugadores = pd.DataFrame([nombres, equipos, posiciones, paises, fechas, imagenes], index=columnas)
    return df_jugadores.T

##### Ligue 1 #####
def obtenerEnlacesEquiposLigue1():  # Función que devuelve una lista con los enlaces de los equipos de la Ligue 1
    url_liga = 'https://ligue1.com/competitions/ligue1mcdonalds?tab=standings'
    driver = obtenerWebDriver()
    driver.get(url_liga)  
    time.sleep(5)
    elementos = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[2]/div/div/div[3]/div/div[3]/div/div[2]/div/div[1]/div/div/div/div/div[1]/div/a')
    enlaces_equipos = []
    for i in elementos:
        enlace = i.get_attribute('href')
        enlaces_equipos.append(enlace)
    driver.close()
    return enlaces_equipos

def obtenerEnlacesJugadoresLigue1(): # Función que devuelve el enlace de cada jugador de la Ligue 1
    equipos = obtenerEnlacesEquiposLigue1()
    lista_jugadores = []
    for i in range(len(equipos)):
        url_equipo = equipos[i] + '?tab=squad'
        driver = obtenerWebDriver()
        driver.get(url_equipo) 
        time.sleep(8)
        contenido = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[2]/div/div/div/div[3]/div/div[3]/div/div')
        elementos = contenido.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[2]/div/div/div/div[3]/div/div[3]/div/div/div/div/a')
        for i in elementos:
            enlace = i.get_attribute('href')
            lista_jugadores.append(enlace)
        #driver.close()
    return lista_jugadores

def obtenerDatosJugadoresLigue1(enlaces_jugadores_l1):  # Devuelve un dataframe con los datos de los jugadores de la Ligue 1
    nombres = []
    dorsales = []
    equipos = []
    posiciones = []
    paises = []
    fechas = []
    for i in range(len(enlaces_jugadores_l1)):  # Primer bucle For para cada equipo
        url_jugador = enlaces_jugadores_l1[i]
        driver = obtenerWebDriver()
        driver.get(url_jugador) 
        time.sleep(5)
        tamaño = driver.execute_script("return window.screen.height;")  # Tamaño de la parte visible de la página
        i = 1
        while True:
            driver.execute_script(f"window.scrollTo(0, {tamaño * i});")
            i += 1
            time.sleep(1)   # Pausa entre cada bajada
            tamaño_total = driver.execute_script("return document.body.scrollHeight;")  # Tamaño de la parte donde se encuentran todos los jugadores
            if tamaño * i > tamaño_total:  # Para comprobar si se ha llegado al final de la página
                break
        sopa = BeautifulSoup(driver.page_source, "lxml")
        try:
            nombre = sopa.find('h6', class_='css-146c3p1 r-14z05s1 r-ubezar r-14yzgew').get_text()
        except:
            nombre = ''
        try:
            apellido = sopa.find('h2', class_='css-146c3p1 r-m5oelx r-xb2eav r-2agvir').get_text()
        except:
            apellido = ''
        nombre_completo = nombre + ' ' + apellido
        nombres.append(nombre_completo)
        try:
            dorsal = sopa.find('h1', class_='css-146c3p1 r-m5oelx r-s67bdx r-162c8fk').get_text()
        except:
            dorsal = ''
        dorsales.append(dorsal)
        try:
            equipo = sopa.find('title').get_text()
            equipo = equipo.split('- ')[1]
        except:
            equipo = ''
        equipos.append(equipo)
        try:
            posicion = sopa.find('h6', class_='css-146c3p1 r-dnmrzs r-1udh08x r-1udbk01 r-3s2u2q r-1iln25a r-14z05s1 r-ubezar r-14yzgew').get_text()
        except:
            posicion = ''
        posiciones.append(posicion)
        contenedor = sopa.find_all('div', class_='css-175oi2r r-1awozwy r-18u37iz r-1cmwbt1 r-1777fci')
        fecha = ''
        pais = ''
        if len(contenedor) == 1:
            pais = contenedor[0].find('div', class_='css-146c3p1 r-c59phl r-ubezar r-135wba7').get_text()
        elif len(contenedor) == 2:
            pais = contenedor[0].find('div', class_='css-146c3p1 r-c59phl r-ubezar r-135wba7').get_text()
            fecha = contenedor[1].find('div', class_='css-146c3p1 r-c59phl r-ubezar r-135wba7').get_text()
        else:
            pass
        paises.append(pais)
        fechas.append(fecha)
    columnas = ['jugador', 'equipo', 'dorsal', 'posicion', 'pais', 'fecha']
    df_jugadores = pd.DataFrame([nombres, equipos, dorsales, posiciones, paises, fechas], index=columnas)
    return df_jugadores.T