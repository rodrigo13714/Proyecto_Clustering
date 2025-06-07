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

# === Obtener lista única de títulos de películas de entrada ===
titulos_unicos = df[['query_movie_id', 'title_de_query_movie_id']].drop_duplicates().sort_values('title_de_query_movie_id')

# Selector de película por título
selected_title = st.selectbox("Selecciona una película:", titulos_unicos['title_de_query_movie_id'])

# Obtener el query_movie_id correspondiente
selected_id = titulos_unicos[titulos_unicos['title_de_query_movie_id'] == selected_title]['query_movie_id'].values[0]

# === Mostrar póster y detalles de la película seleccionada ===
st.subheader("🎥 Película seleccionada")
st.markdown(f"**Título:** {selected_title}")
st.markdown(f"**Movie ID:** `{selected_id}`")

poster_path = f"posters/{selected_id}.jpg"
if os.path.exists(poster_path):
    st.image(Image.open(poster_path), width=250)
else:
    st.warning("📭 Póster de esta película no encontrado en posters/")

# === Obtener recomendaciones para la película seleccionada ===
st.subheader("🍿 Películas Recomendadas")
recomendaciones = df[df['query_movie_id'] == selected_id].sort_values('position')

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
