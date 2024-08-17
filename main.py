#Importar las Librerías. 
#Se importaron las siguientes librerías.
from fastapi import FastAPI, HTTPException
import pandas as pd 
import ast
from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
app = FastAPI()

#Cargar el conjunto de datos
df = pd.read_csv("data_transf.csv")

#Este endpoint permite obtener la cantidad de películas filmadas en un mes específico
@app.get("/cantidad_filmaciones_mes/{mes}")
async def cantidad_filmaciones_mes(mes: str):
    # Convertimos la columna 'release_date' a formato datetime si no lo está.
    if not pd.api.types.is_datetime64_any_dtype(df['release_date']):
        df['release_date'] = pd.to_datetime(df['release_date'])

    # Mapeo de nombres de meses en español a sus respectivos números.
    meses_nombres = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    
    #Verificar si el mes es un número.
    if mes.isdigit():
        mes_num = int(mes)
        #Validar que el mes esté en el rango correcto.
        if not 1 <= mes_num <= 12:
            raise HTTPException(status_code=400, detail="El número del mes no es válido")
    else:
        #Convertir el mes a minúscula y verificamos si es un nombre de mes válido.
        mes = mes.lower()
        mes_num = meses_nombres.get(mes)
        if mes_num is None:
            raise HTTPException(status_code=400, detail="El mes ingresado no es válido")

    #Filtrar las películas por el mes especificado.
    cantidad = df[df['release_date'].dt.month == mes_num].shape[0]

    #Devolver la cantidad de películas.
    return {"en el mes": mes.capitalize(), "la cantidad de peliculas que se filmaron fueron": cantidad}

#Este endpoint muestra la cantidad de películas filmadas en un día específico de la semana
@app.get("/cantidad_filmaciones_dia/{dia}")
async def cantidad_filmaciones_dia(dia: str):
    try:
        # Asegurar que la columna 'release_date' esté en formato datetime
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

        # Mapear de días en español a números correspondientes de día de la semana
        dias_nombres = {
            'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3,
            'viernes': 4, 'sábado': 5, 'domingo': 6
        }

        #Normalizar el día ingresado
        dia_normalizado = dias_nombres.get(dia.lower())
        if dia_normalizado is None:
            raise ValueError("El día ingresado no es válido")

        #Filtrar películas estrenadas en el día especificado
        cantidad = df[df['release_date'].dt.dayofweek == dia_normalizado].shape[0]

        return {"en el día": dia.capitalize(), "la cantidad de peliculas que se filmaron fueron": cantidad}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
#Este endpoint muestra informacion sobre una pelicula especifica
@app.get("/score_titulo/{titulo_de_la_filmacion}")
async def obtener_score_titulo(titulo_de_la_filmacion: str):
    #Normalizar el título de la filmación ingresado y los títulos en el dfFrame
    titulo_normalizado = titulo_de_la_filmacion.strip().lower()
    df['title_normalized'] = df['title'].str.strip().str.lower()

    #Filtrar el dfFrame por el título normalizado
    pelicula = df[df['title_normalized'] == titulo_normalizado]

    #Verificar si la película existe
    if pelicula.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    #Extraer el título, año de estreno y score (o popularidad)
    titulo = pelicula.iloc[0]['title']
    año_estreno = pelicula.iloc[0]['release_date'].year
    score = pelicula.iloc[0]['popularity']

    #Retornar la respuesta
    return {
        "mensaje": f"La película '{titulo}' fue estrenada en el año {año_estreno} con un score/popularidad de {score}"
    }

#Este endpoint proporciona información sobre los votos de una película
@app.get("/votos_titulo/{titulo_de_la_filmacion}")
async def votos_titulo(titulo_de_la_filmacion: str):
    #Convertir el título ingresado a minúsculas y eliminar espacios adicionales
    titulo_normalizado = titulo_de_la_filmacion.strip().lower()

    #Buscar la película en el dfFrame
    pelicula = df[df['title'].str.lower() == titulo_normalizado]

    #Verificar si se encontró la película
    if pelicula.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    #Extraer datos relevantes
    titulo = pelicula['title'].iloc[0]
    votos = pelicula['vote_count'].iloc[0]
    promedio = pelicula['vote_average'].iloc[0]
    anio_estreno = pelicula['release_date'].dt.year.iloc[0]

    #Verificar la cantidad de votos
    if votos < 2000:
        raise HTTPException(status_code=400, detail="La película no tiene suficientes valoraciones")

    #Retornar la respuesta en el formato solicitado
    return {
        "mensaje": (
            f"La película {titulo} fue estrenada en el año {anio_estreno}. "
            f"La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio}."
        )
    }
#este enpoind nos da informacion sobre un actor en especifico
@app.get("/get_actor/{nombre_actor}")
async def get_actor(nombre_actor: str):
    nombre_actor = nombre_actor.lower()
    
    # Función para verificar si el nombre del actor está en la lista de actores
    def actor_en_lista(actores_str):
        try:
            actores = ast.literal_eval(actores_str)
            return nombre_actor in [actor.lower() for actor in actores]
        except (ValueError, SyntaxError):
            return False
    
    # Filtrar el DataFrame para obtener las películas en las que ha participado el actor
    peliculas_actor = df[df['actores'].apply(actor_en_lista)]
    
    # Verificar si el actor ha participado en alguna película
    if peliculas_actor.empty:
        raise HTTPException(status_code=404, detail="Actor no encontrado en el dataset")

    # Calcular el total de retorno y el promedio
    total_retorno = peliculas_actor['revenue'].sum()
    promedio_retorno = peliculas_actor['revenue'].mean()
    cantidad_peliculas = peliculas_actor.shape[0]

    # Retornar la respuesta 
    return {
        "mensaje": (
            f"El actor {nombre_actor} ha participado en {cantidad_peliculas} películas, "
            f"con un retorno total de {total_retorno} y un promedio de retorno de {promedio_retorno:.2f} por película."
        )
    }
#este enpoind nos da informacion sobre un director en especifico   
@app.get('/get_director/{nombre_director}')
async def get_director(nombre_director: str) -> Dict[str, Any]:
    #Convertir a minúsculas para hacer la búsqueda case-insensitive
    nombre_director_lower = nombre_director.lower()
    
    #Filtrar el DataFrame por el nombre del director, eliminando nulos
    director_df = df[df['director'].str.lower().fillna('').str.contains(nombre_director_lower)]
    
    if director_df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron películas para el director especificado.")
    
    #Crear la respuesta directamente en una lista de diccionarios
    peliculas = director_df[['title', 'release_date', 'return', 'budget', 'revenue']].to_dict(orient='records')
    
    return {
        "success": True,
        "director": nombre_director,
        "peliculas": peliculas
    }
#este ultimo enpoind nos devuelve como redomendacion las 5 peliculas. 

#Inicializar el vectorizador TF-IDF y calcular la matriz de similitud globalmente
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['overview'].fillna(''))
 
@app.get("/recomendacion/{titulo}")
async def obtener_recomendacion(titulo: str, top_n: int = 5):
    #Convertir el título ingresado a minúsculas
    titulo_lower = titulo.lower()
    
    #Buscar el índice de la película en minúsculas
    idx_list = df.index[df['title'].str.lower() == titulo_lower].tolist()
    
    if not idx_list:
        #Devolver un mensaje de error si no se encuentra la película
        raise HTTPException(status_code=404, detail="Película no encontrada")

    idx = idx_list[0]

    #Calcular la similitud del coseno entre la película seleccionada y todas las demás
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix)

    #Obtener las puntuaciones de similitud y ordenar por la más alta
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    #Excluir la primera película (es la misma) y obtener las top_n más similares
    sim_scores = sim_scores[1:top_n + 1]

    #Obtener los índices de las películas recomendadas
    movie_indices = [i[0] for i in sim_scores]

    #Devolver los títulos de las películas recomendadas
    recomendaciones = df['title'].iloc[movie_indices].tolist()

    #Devolver la lista de películas recomendadas
    return {"lista_recomendada": recomendaciones}