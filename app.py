import streamlit as st
import pandas as pd
import os
from PIL import Image

# Configuración de página con fondo blanco personalizado
st.set_page_config(page_title="Recomendador Visual", layout="wide")
st.markdown("""
    <style>
    body {
        background-color: white;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 Recomendador de Películas Basado en Pósters")

# === Cargar CSV limpio ===
@st.cache_data
def load_data():
    return pd.read_csv("Recomendaciones_Limpio.csv")

df = load_data()

# === Obtener lista única de títulos de películas ===
titulos_unicos = df[['query_movie_id', 'title']].drop_duplicates().sort_values('title')

# === Selector de película por título ===
selected_title = st.selectbox("Selecciona una película por título:", titulos_unicos['title'])

# === Obtener el ID correspondiente al título seleccionado ===
selected_id = titulos_unicos[titulos_unicos['title'] == selected_title]['query_movie_id'].values[0]

# === Mostrar póster de la película seleccionada ===
st.subheader("🎥 Película seleccionada")
st.markdown(f"**Título:** `{selected_title}`")
st.markdown(f"**Movie ID:** `{selected_id}`")

poster_path = f"posters/{selected_id}.jpg"
if os.path.exists(poster_path):
    st.image(Image.open(poster_path), width=250)
else:
    st.warning("📭 Póster de esta película no encontrado en posters/")

# === Obtener recomendaciones ===
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
