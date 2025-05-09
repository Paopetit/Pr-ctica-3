# -*- coding: utf-8 -*-
"""Practica3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MUZsRfhbAUgj53mEmeomcJffox_FN2zV
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Dashboard NBA", layout="wide")

# Título y descripción
st.title("Dashboard de Análisis de Juegos NBA")
st.markdown("Explora los resultados de los juegos de la NBA filtrando por año, equipo y tipo de juego (Temporada Regular, Playoffs o Ambos).")

# Cargar datos desde el archivo CSV
nba_data = pd.read_csv("/content/nba_all_elo - nba_all_elo.csv")

# Listas de valores únicos para los filtros
year_list = sorted(nba_data['year_id'].unique())
team_list = sorted(nba_data['team_id'].unique())

# Barra lateral con filtros
with st.sidebar:
    st.header("Filtros")
    selected_year = st.selectbox("Selecciona el año:", year_list)
    selected_team = st.selectbox("Selecciona el equipo:", team_list)
    game_type = st.radio("Selecciona el tipo de juego:", ("Temporada Regular", "Playoffs", "Ambos"))

# Filtrar datos por año y equipo
filtered_data = nba_data[(nba_data['year_id'] == selected_year) & (nba_data['team_id'] == selected_team)]
if game_type != "Ambos":
    # is_playoffs: 0 para temporada regular, 1 para playoffs
    if game_type == "Temporada Regular":
        filtered_data = filtered_data[filtered_data['is_playoffs'] == 0]
    else:  # Playoffs
        filtered_data = filtered_data[filtered_data['is_playoffs'] == 1]

# Verificar si existen datos tras el filtrado
if filtered_data.empty:
    st.warning("No se encontraron datos para los filtros seleccionados.")
else:
    # Ordenar los datos según el orden de juego: se usa 'seasongame' si existe, sino 'date_game'
    if "seasongame" in filtered_data.columns:
        filtered_data = filtered_data.sort_values(by="seasongame")
    elif "date_game" in filtered_data.columns:
        filtered_data = filtered_data.sort_values(by="date_game")
    else:
        filtered_data = filtered_data.sort_index()

    # Crear columnas para identificar juegos ganados y perdidos
    filtered_data['win'] = (filtered_data['game_result'] == 'W').astype(int)
    filtered_data['loss'] = (filtered_data['game_result'] == 'L').astype(int)

    # Calcular acumulados de victorias y derrotas
    filtered_data['cumulative_wins'] = filtered_data['win'].cumsum()
    filtered_data['cumulative_losses'] = filtered_data['loss'].cumsum()

    # Mostrar datos y gráfica de líneas en columnas
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Datos Filtrados")
        st.dataframe(filtered_data)

    with col2:
        st.subheader("Acumulado de Juegos Ganados y Perdidos")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(filtered_data.index, filtered_data['cumulative_wins'], label="Ganados", marker='o')
        ax.plot(filtered_data.index, filtered_data['cumulative_losses'], label="Perdidos", marker='o')
        ax.set_title(f"{selected_team} - {selected_year} ({game_type})")
        ax.set_xlabel("Orden de Juego")
        ax.set_ylabel("Cantidad Acumulada")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    # Calcular totales para la gráfica de pastel
    total_wins = filtered_data['win'].sum()
    total_losses = filtered_data['loss'].sum()

    st.subheader("Porcentaje de Juegos Ganados vs. Perdidos")
    if (total_wins + total_losses) > 0:
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.pie([total_wins, total_losses], labels=["Ganados", "Perdidos"], autopct="%1.1f%%", startangle=90)
        ax2.axis("equal")
        ax2.set_title("Distribución de Resultados")
        st.pyplot(fig2)
    else:
        st.info("No hay datos suficientes para mostrar la gráfica de pastel.")