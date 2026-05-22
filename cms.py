import streamlit as st
import random
import time

st.title("CMS vs Transformer estático")

freq_rapida = st.slider("Frecuencia memoria rápida (ítems)", 2, 20, 5)
freq_media  = st.slider("Frecuencia memoria media (ítems)", 5, 50, 20)
freq_lenta  = st.slider("Frecuencia memoria lenta (ítems)", 10, 100, 50)

# Lista de palabras
palabras = [f"item_{i}" for i in range(100)]
# Simulación de memorias
mem_rapida, mem_media, mem_lenta = [], [], []
transformer_window = []

st.write("---")
for i, p in enumerate(palabras):
    # Transformer solo recuerda últimos 20 ítems
    transformer_window.append(p)
    if len(transformer_window) > 20:
        transformer_window.pop(0)

    # CMS: actualizamos memorias según frecuencia
    if i % freq_rapida == 0:
        mem_rapida.append(p)
    if i % freq_media == 0:
        mem_media.append(p)
    if i % freq_lenta == 0:
        mem_lenta.append(p)

    # Mostrar retención acumulada
    retencion_trans = len(transformer_window)
    retencion_cms = len(set(mem_rapida + mem_media + mem_lenta))

    st.write(f"Paso {i+1}: Transformer recuerda {retencion_trans} palabras, CMS recuerda {retencion_cms} palabras")
    time.sleep(0.05)  # animación

st.success("Fin de la secuencia. Haz clic en 'Reiniciar' para cambiar frecuencias.")
