# Documentación del API de Películas

Esta guía proporciona una visión general de los endpoints disponibles en la API de películas, creada con FastAPI. La API permite consultar información sobre películas, incluyendo estadísticas de filmación y recomendaciones.

```python
# 1. Obtener cantidad de películas filmadas en un mes específico 

@app.get("/cantidad_filmaciones_mes/{mes}")
async def cantidad_filmaciones_mes(mes: str):
    if not pd.api.types.is_datetime64_any_dtype(df['release_date']):
        df['release_date'] = pd.to_datetime(df['release_date'])

    meses_nombres = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    
    if mes.isdigit():
        mes_num = int(mes)
        if not 1 <= mes_num <= 12:
            raise HTTPException(status_code=400, detail="El número del mes no es válido")
    else:
        mes = mes.lower()
        mes_num = meses_nombres.get(mes)
        if mes_num is None:
            raise HTTPException(status_code=400, detail="El mes ingresado no es válido")

    cantidad = df[df['release_date'].dt.month == mes_num].shape[0]

    return {"en el mes": mes.capitalize(), "la cantidad de peliculas que se filmaron fueron": cantidad}

Devuelve la cantidad de películas filmadas en un mes específico. El mes puede ser ingresado como nombre en español.

## 2. Obtener cantidad de películas filmadas en un día específico de la semana

@app.get("/cantidad_filmaciones_dia/{dia}")
async def cantidad_filmaciones_dia(dia: str):
    try:
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

        dias_nombres = {
            'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3,
            'viernes': 4, 'sábado': 5, 'domingo': 6
        }

        dia_normalizado = dias_nombres.get(dia.lower())
        if dia_normalizado is None:
            raise ValueError("El día ingresado no es válido")

        cantidad = df[df['release_date'].dt.dayofweek == dia_normalizado].shape[0]

        return {"en el día": dia.capitalize(), "la cantidad de peliculas que se filmaron fueron": cantidad}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

Devuelve la cantidad de películas filmadas en un día específico de la semana. Los días deben ser ingresados en español.

##3. Obtener información sobre una película específica

@app.get("/score_titulo/{titulo_de_la_filmacion}")
async def obtener_score_titulo(titulo_de_la_filmacion: str):
    titulo_normalizado = titulo_de_la_filmacion.strip().lower()
    df['title_normalized'] = df['title'].str.strip().str.lower()

    pelicula = df[df['title_normalized'] == titulo_normalizado]

    if pelicula.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    titulo = pelicula.iloc[0]['title']
    año_estreno = pelicula.iloc[0]['release_date'].year
    score = pelicula.iloc[0]['popularity']

    return {
        "mensaje": f"La película '{titulo}' fue estrenada en el año {año_estreno} con un score/popularidad de {score}"
    }

Devuelve información sobre una película específica, incluyendo su título, año de estreno y score (popularidad).

##4. Obtener información sobre los votos de una película

@app.get("/votos_titulo/{titulo_de_la_filmacion}")
async def votos_titulo(titulo_de_la_filmacion: str):
    titulo_normalizado = titulo_de_la_filmacion.strip().lower()

    pelicula = df[df['title'].str.lower() == titulo_normalizado]

    if pelicula.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    titulo = pelicula['title'].iloc[0]
    votos = pelicula['vote_count'].iloc[0]
    promedio = pelicula['vote_average'].iloc[0]
    anio_estreno = pelicula['release_date'].dt.year.iloc[0]

    if votos < 2000:
        raise HTTPException(status_code=400, detail="La película no tiene suficientes valoraciones")

    return {
        "mensaje": (
            f"La película {titulo} fue estrenada en el año {anio_estreno}. "
            f"La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio}."
        )
    }

Devuelve información sobre la cantidad y promedio de votos de una película. La película debe tener al menos 2000 valoraciones.

##5. Obtener información sobre un actor específico

@app.get("/get_actor/{nombre_actor}")
async def get_actor(nombre_actor: str):
    nombre_actor = nombre_actor.lower()
    
    def actor_en_lista(actores_str):
        try:
            actores = ast.literal_eval(actores_str)
            return nombre_actor in [actor.lower() for actor in actores]
        except (ValueError, SyntaxError):
            return False
    
    peliculas_actor = df[df['actores'].apply(actor_en_lista)]
    
    if peliculas_actor.empty:
        raise HTTPException(status_code=404, detail="Actor no encontrado en el dataset")

    total_retorno = peliculas_actor['revenue'].sum()
    promedio_retorno = peliculas_actor['revenue'].mean()
    cantidad_peliculas = peliculas_actor.shape[0]

    return {
        "mensaje": (
            f"El actor {nombre_actor} ha participado en {cantidad_peliculas} películas, "
            f"con un retorno total de {total_retorno} y un promedio de retorno de {promedio_retorno:.2f} por película."
        )
    }

Devuelve información sobre un actor específico, incluyendo la cantidad de películas en las que ha participado, el retorno total y el promedio de retorno por película.

##6. Obtener información sobre un director específico

@app.get('/get_director/{nombre_director}')
async def get_director(nombre_director: str) -> Dict[str, Any]:
    nombre_director_lower = nombre_director.lower()
    
    director_df = df[df['director'].str.lower().fillna('').str.contains(nombre_director_lower)]
    
    if director_df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron películas para el director especificado.")
    
    peliculas = director_df[['title', 'release_date', 'return', 'budget', 'revenue']].to_dict(orient='records')
    
    return {
        "success": True,
        "director": nombre_director,
        "peliculas": peliculas
    }

Devuelve información sobre las películas dirigidas por un director específico. Incluye el título, fecha de estreno, retorno, presupuesto y revenue

##7. Obtener recomendaciones de películas basadas en una película específica

# Inicializar el vectorizador TF-IDF y calcular la matriz de similitud globalmente
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['overview'].fillna(''))

@app.get("/recomendacion/{titulo}")
async def obtener_recomendacion(titulo: str, top_n: int = 5):
    titulo_lower = titulo.lower()
    
    idx_list = df.index[df['title'].str.lower() == titulo_lower].tolist()
    
    if not idx_list:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    idx = idx
    
Devuelve una lista de las 5 películas más similares a la película proporcionada. La similitud se basa en el contenido textual de las películas.