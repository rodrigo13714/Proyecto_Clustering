import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(page_title="Recomendador Visual", layout="wide")
st.title("🎬 Recomendador de Películas Basado en Pósters")

# === Cargar CSV limpio ===
@st.cache_data
def load_data():
    return pd.read_csv("Recomendaciones_Limpio.csv")

df = load_data()

# === Obtener lista única de películas de entrada ===
peliculas_unicas = df['query_movie_id'].drop_duplicates().sort_values().tolist()

# === Selector de película por ID ===
selected_id = st.selectbox("Selecciona una película por ID:", peliculas_unicas)

# === Mostrar póster de la película seleccionada (si existe) ===
st.subheader("🎥 Película seleccionada")
st.markdown(f"**Movie ID:** {selected_id}")
poster_path = f"posters/{selected_id}.jpg"
if os.path.exists(poster_path):
    st.image(Image.open(poster_path), width=250)
else:
    st.warning("📭 Póster de esta película no encontrado en posters_test/")

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
