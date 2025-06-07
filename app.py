import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(page_title="Recomendador Visual", layout="wide")
st.title("🎬 Recomendador de Películas Basado en Pósters")

# === Cargar CSV enriquecido ===
@st.cache_data
def load_data():
    return pd.read_csv("Recomendaciones_Enriquecido.csv")

df = load_data()

# === Selector por título de la película elegida ===
titulos_disponibles = df['title_de_query_movie_id'].unique()
selected_title = st.selectbox("Selecciona una película:", sorted(titulos_disponibles))

# === Filtrar el DataFrame por el título seleccionado ===
pelicula_df = df[df['title_de_query_movie_id'] == selected_title]

# === Mostrar póster de la película seleccionada ===
st.subheader("🎥 Película seleccionada")

# Obtenemos el ID y género directamente de la primera fila
query_id = pelicula_df['query_movie_id'].iloc[0]
query_genre = pelicula_df['genre_de_query_movie_id'].iloc[0]

st.markdown(f"**Título:** {selected_title}")
st.markdown(f"**Género:** {query_genre}")
st.markdown(f"**Movie ID:** `{query_id}`")

poster_path = f"posters/{query_id}.jpg"
if os.path.exists(poster_path):
    st.image(Image.open(poster_path), width=250)
else:
    st.warning("📭 Póster de esta película no encontrado en posters/")

# === Mostrar las recomendaciones ===
st.subheader("🍿 Películas Recomendadas")

recomendaciones = pelicula_df.sort_values("position")
cols = st.columns(5)

for idx, (_, row) in enumerate(recomendaciones.iterrows()):
    col = cols[idx % 5]
    with col:
        rec_id = row['recommended_movie_id']
        rec_title = row['title']
        rec_genre = row['genre']
        poster_rec_path = f"posters/{rec_id}.jpg"

        if os.path.exists(poster_rec_path):
            col.image(Image.open(poster_rec_path), width=120)
        else:
            col.caption("📭 Sin póster")

        col.markdown(f"**{rec_title}**")
        col.caption(f"🎭 {rec_genre}")
