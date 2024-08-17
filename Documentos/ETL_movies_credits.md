## Documentación del Código

Este documento proporciona una guía detallada sobre las transformaciones y limpiezas realizadas en el conjunto de datos de películas.

**Código:**
```python

## 1. mportación de Librerías

Se importan las siguientes librerías necesarias para la manipulación y limpieza de datos:

import pandas as pd
import re 
import json
import ast

## 2. Carga del Conjunto de Datos

Se carga el conjunto de datos desde un archivo CSV:

df = pd.read_csv("movies_dataset.csv")

## 3. Desanidación de Campos

Se desanidan los campos id y name de las columnas belongs_to_collection y production_companies, creando nuevas columnas para cada uno:

busq_1 = r"'id': ([^,]*)"
df['id_coleccion'] = df['belongs_to_collection'].str.extract(busq_1, flags=re.IGNORECASE)
busq_2 = r"'name': '([^']*)"
df['nombre_coleccion'] = df['belongs_to_collection'].str.extract(busq_2, flags=re.IGNORECASE)

busq_3 = r"'id': ([^}]*)"
df['id_produccion'] = df['production_companies'].str.extract(busq_3, flags=re.IGNORECASE)
busq_4= r"'name': '([^']*)"
df['nombre_produccion'] = df['production_companies'].str.extract(busq_4, flags=re.IGNORECASE)

## 4. Manejo de Valores Nulos

Se verifica la presencia de valores nulos en las columnas revenue y budget, reemplazando los valores nulos en revenue por 0. También se eliminan filas con valores nulos en release_date.

nulos_revenue = df["revenue"].isnull().sum()
nulos_budget = df["budget"].isnull().sum()

df["revenue"] = df["revenue"].fillna(0)
df = df.dropna(subset=["release_date"])

## 5. Conversión de Tipos de Datos

Se convierte release_date a formato de fecha y se extrae el año de estreno en una nueva columna release_year. Las columnas revenue y budget se convierten a tipo numérico.

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce').dt.strftime('%Y-%m-%d')
df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year.astype('Int64')

df['revenue'] = pd.to_numeric(df['revenue'], errors= "coerce")
df['budget'] = pd.to_numeric(df['budget'], errors= "coerce")

## 6. Cálculo del Retorno de Inversión

Se calcula el retorno de inversión en la columna return.

df['return'] = df.apply(lambda row: row['revenue'] / row['budget'] if row['budget'] != 0 else 0, axis=1)

## 7. Eliminación de Columnas No Necesarias

Se eliminan las columnas innecesarias del DataFrame:

eliminar_columnas = ["video", "imdb_id", "adult", "original_title", "poster_path", "homepage", "belongs_to_collection", "production_companies"]
df2 = df.drop(columns=eliminar_columnas)

## 8. Extracción de Nombres de Géneros

Se convierte la columna genres en una lista de nombres de géneros y se crea una nueva columna genres_name.

def extraer_nombres_genero(generos_str):
    try:
        generos_lista = json.loads(generos_str.replace("'", '"'))
        nombres_genero = [genero['name'] for genero in generos_lista]
        return ', '.join(nombres_genero)
    except (json.JSONDecodeError, KeyError):
        return None

df2['genres_name'] = df2['genres'].apply(extraer_nombres_genero)

## 9. Eliminación de Columnas y Duplicados

Se eliminan las columnas genres y se eliminan los registros duplicados basados en el campo id:

eliminar_genres = ["genres"]
movies = df2.drop(columns=eliminar_genres)
movies = movies.drop_duplicates(subset='id', keep='first')

## 10. Procesamiento del Conjunto de Datos de Créditos
Se carga el dataset de créditos y se eliminan duplicados. Se convierte la columna cast en una lista de diccionarios y se extraen los nombres de los actores. También se extrae el nombre del director.

credits = pd.read_csv("credits.csv")
credits = credits.drop_duplicates(subset='id', keep='first')
credits['cast'] = credits['cast'].apply(ast.literal_eval)
credits['actores'] = credits['cast'].apply(extract_actor_names)

credits['crew'] = credits['crew'].apply(safe_literal_eval)
credits['director'] = credits['crew'].apply(extract_director)

## 11. Unión de DataFrames y Filtrado de Títulos

Se combinan los DataFrames de películas y créditos, y se filtran los títulos de películas que contienen solo caracteres alfabéticos. Se eliminan columnas no necesarias.

data_fusionado = movies.merge(data_credits, how='inner', on='id')

def filtrar_titulo(titulo):
    return re.match("^[a-zA-Z0-9\\s\\$\\-\\#\\?\\&\\!\\ñ\\¿\\¡]*$", titulo) is not None

df_fusionado = data_fusionado[data_fusionado['title'].apply(filtrar_titulo)]
df_combinado = df_fusionado.drop(columns=["production_countries", "spoken_languages", "status", "tagline"])

## 12. Guardar el Dataset Transformado

Finalmente, se guarda el DataFrame transformado en un archivo CSV.

df_combinado.to_csv('data_transf.csv', index=False)

Este documento ofrece una visión general clara de las transformaciones realizadas en los datos, facilitando su comprensión y replicación si es necesario.