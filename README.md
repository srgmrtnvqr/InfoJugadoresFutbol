<h1 align="center">Descargar jugadores inscritos en las ligas de fútbol</h1>
<p align="center"><img src="https://github.com/srgmrtnvqr/InfoJugadoresFutbol/blob/main/resultado_obtenido.JPG"/></p> 

- Lenguaje utilizado: ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 

## Índice:
---

- [Descripción](#descripción)
- [Guía de usuario](#guía-de-usuario)
- [Dependencias](#dependencias)
- [Autor/es](#autores)


## Descripción
---
Este repositorio contiene el código para descargar los datos de los jugadores inscritos en ligas de fútbol profesionales.

Las ligas disponibles para descargar sus jugadores son: 
- La Liga (https://www.laliga.com/es-GB/laliga-easports/clubes) :white_check_mark:
- Premier League (https://www.premierleague.com/clubs) :white_check_mark:
- Bundesliga (https://www.bundesliga.com/de/bundesliga/clubs) :white_check_mark:
- Serie A (https://www.legaseriea.it/it/serie-a/calciatori) :white_check_mark:
- Ligue 1 (https://ligue1.com/competitions/ligue1mcdonalds?tab=standings) :white_check_mark:

Los datos descargados son almacenados en un Excel para su posterior análisis.

## Guía de usuario
---
Pasos a seguir para descargar la información de los jugadores de las ligas disponibles:
- 1. Ejecuta la primera celda para poder usar las funciones implementadas en el archivo .py

      ```import datos_jugadores```

- 2. Ejecuta las celdas correspondientes a la liga de la que quieres obtener los datos:
     [La Liga](#la-liga) ,
     [Premier League](#premier-league) ,
     [Bundesliga](#bundesliga) ,
     [Serie A](#serie-a) y
     [Ligue 1](#ligue-1)

     ### La Liga
     `` # Descargar jugadores de La Liga (2024-2025) ``

     La primera celda de código, dentro de `` Obtención de los enlaces de las páginas de todos los jugadores de La Liga ``, te devuelve una lista de todos los jugadores que hay inscritos en La Liga.
     ```
     lista_jugadores = datos_jugadores.obtenerEnlacesJugadores()
     lista_jugadores
     ```

     La celda siguiente, dentro de `` Obtención de los datos de todos los jugadores de La Liga ``, te devuelve los datos de todos los jugadores de La Liga.
     ```
     df_jugadores = datos_jugadores.obtenerDatosJugadores(lista_jugadores)
     ```
     
     La celda de abajo sirve para tratar la fecha de cada jugador.
     ```
     # Tratamiento de los datos
     df_jugadores['fecha'] = df_jugadores.fecha.str.slice(start=0, stop=10)
     df_jugadores
     ```

     Por último, ejecuta la celda para almacenar los datos en un Excel.
     ```
     # Almacenamiento de los datos en un Excel
     df_jugadores.to_excel('info_jugadores_la_liga.xlsx', index=False)
     ```



     ### Premier League
     `` # Descargar jugadores de la Premier League (2024-2025) ``

     Para la Premier League, puedes obtener los datos de los jugadores directamente. Para ello, ejecuta la celda de código que está dentro de `` Obtención de los datos de todos los jugadores de la Premier League ``.
     ```
     df_jugadores_pl = datos_jugadores.obtenerDatosJugadoresPremier()
     df_jugadores_pl
     ```

     A continuación, ejecuta la última celda para almacenar los datos en un Excel.
     ```
     # Almacenamiento de los datos en un Excel
     df_jugadores_pl.to_excel('info_jugadores_premier_league.xlsx', index=False)  
     ```



     ### Bundesliga
     `` # Descargar jugadores de la Bundesliga (2024-2025) ``

     Para la Bundesliga, puedes obtener los datos de los jugadores directamente. Para ello, ejecuta la celda de código que está dentro de `` Obtención de los datos de todos los jugadores de la Bundesliga  ``.
     ```
     df_jugadores_bdl = datos_jugadores.obtenerDatosJugadoresBundesliga()  
     df_jugadores_bdl
     ```
     
     A continuación, ejecuta la siguiente celda para que los datos de algunas columnas se puedan tratar mejor.
     ```
     # Tratamiento de los datos
     df_jugadores_bdl['fecha'] = (df_jugadores_bdl.fecha.str.slice(start=0, stop=10)).str.replace('.','/')
     df_jugadores_bdl['pais'] = [pais[0] for pais in df_jugadores_bdl.pais.str.split(',')]
     df_jugadores_bdl['peso'] = [peso[0] for peso in df_jugadores_bdl.peso.str.split(' ')]
     df_jugadores_bdl['altura'] = [altura[0] for altura in df_jugadores_bdl.altura.str.split(' ')]
     df_jugadores_bdl
     ```

     Por último, ejecuta la última celda para almacenar los datos en un Excel.
     ```
     # Almacenamiento de los datos en un Excel
     df_jugadores_bdl.to_excel('info_jugadores_bundesliga.xlsx', index=False)
     ```



     ### Serie A
     `` # Descargar jugadores de la Serie A (2024-2025) ``
     
     Para la Serie A, puedes obtener los datos de los jugadores directamente. Para ello, ejecuta la celda de código que está dentro de `` Obtención de los datos de todos los jugadores de la Serie A  ``.
     ```
     df_jugadores_SerieA = datos_jugadores.obtenerDatosJugadoresSerieA()
     df_jugadores_SerieA
     ```
     
     Por último, ejecuta la última celda para almacenar los datos en un Excel.
     ```
     df_jugadores_SerieA.to_excel('info_jugadores_seriea.xlsx', index=False)
     ```



     ### Ligue 1
     `` # Descargar jugadores de la Ligue 1 (2024-2025) ``
     

## Dependencias
---
Las librerías necesarias para la ejecución del código son: 
- BeautifulSoup
- json 
- pandas 
- requests
- selenium webdriver
- time

## Autor/es
---
Sergio Martín Vaquero
