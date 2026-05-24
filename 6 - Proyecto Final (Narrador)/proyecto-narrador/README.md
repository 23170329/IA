# AI Game Commentator - TETR.IO Edition

Sistema de IA que analiza clips de videojuegos y genera comentarios automaticos en espanol orquestando Vision, Lenguaje y Audio.

---

## Arquitectura

```
video.mp4
    |
    v
+-----------------------------------------------------------+
|  Modulo 1 - CAPTURA (capture.py)                          |
|  OpenCV - extrae 1 frame cada 2 segundos                  |
+-----------------------------+-----------------------------+
                              | frames RGB
                              v
+-----------------------------------------------------------+
|  Modulo 5 - HEURISTICA (heuristic.py)                     |
|  MSE entre frames - decide si el cambio es significativo  |
+-----------------------------+-----------------------------+
                              | frame aprobado
                              v
+-----------------------------------------------------------+
|  Modulo 2 - VISION - HuggingFace #1 (vision.py)           |
|  Salesforce/blip-image-captioning-base                    |
|  "a game board with many red blocks near the top"         |
+-----------------------------+-----------------------------+
                              | caption en ingles
                              v
+-----------------------------------------------------------+
|  Modulo 3 - NARRACION - HuggingFace #2 (narration.py)     |
|  gpt2 - genera comentario epico en ingles                 |
|  + deteccion de estado -> plantilla epica en espanol      |
+--------------+---------------------------+----------------+
               | espanol                   | ingles (UI)
               v
+-----------------------------------------------------------+
|  Modulo 4 - VOZ - HuggingFace #3 (tts_module.py)          |
|  facebook/mms-tts-spa                                     |
|  texto -> audio WAV en espanol                            |
+-----------------------------+-----------------------------+
                              | audio + resultados
                              v
+-----------------------------------------------------------+
|  INTERFAZ - Gradio (app.py)                               |
|  Muestra frame + captions + comentarios + audio           |
+-----------------------------------------------------------+
```

---

## Modelos de HuggingFace utilizados

| # | Modulo | Modelo | Tarea |
|---|---|---|---|
| 1 | Vision | `Salesforce/blip-image-captioning-base` | Caption de imagen -> texto ingles |
| 2 | Narracion | `gpt2` | Generacion de comentario creativo en ingles |
| 3 | Voz | `facebook/mms-tts-spa` | Text-to-Speech en espanol |

---

## Juego elegido: TETR.IO

Tetris competitivo online (gratis en [tetr.io](https://tetr.io)), con estados visuales muy distintos que BLIP clasifica sin entrenamiento adicional:

| Estado | Keywords que BLIP genera | Comentario |
|---|---|---|
| Peligro | `top`, `full`, `high`, `filled` | El stack esta llegando al limite! |
| Limpieza | `clear`, `line`, `row`, `empty` | Tetris! Lineas eliminadas con maestria |
| Game Over | `game over`, `dark`, `end` | Y asi termina la batalla! |
| Inicio | `start`, `fresh`, `blank` | Comienza la batalla! |
| Normal | (resto) | El jugador mantiene el control |

---

## Estructura del proyecto

```
tetris_commentator/
|-- app.py            <- Interfaz Gradio (punto de entrada)
|-- capture.py        <- Modulo 1: extraccion de frames (OpenCV)
|-- heuristic.py      <- Modulo 5: logica de cuando comentar (MSE)
|-- vision.py         <- Modulo 2: BLIP image captioning
|-- narration.py      <- Modulo 3: GPT-2 + plantillas espanol
|-- tts_module.py     <- Modulo 4: MMS-TTS voz en espanol
|-- requirements.txt
|-- README.md
```

---

## Instalacion y ejecucion

### Requisitos
- Python 3.9 o superior
- ~4 GB de espacio libre (para modelos en cache)
- Conexion a internet (primera ejecucion descarga modelos)

### Pasos

```bash
# 1. Clonar / descomprimir el proyecto
cd tetris_commentator

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicacion
python app.py
```

Gradio abrira automaticamente `http://127.0.0.1:7860` en el navegador.

### Uso
1. Sube un clip `.mp4` de TETR.IO (o usa el boton "Test sin video")
2. Ajusta la sensibilidad si quieres mas/menos comentarios
3. Presiona "Analizar video"
4. Espera el procesamiento - la primera vez descarga los modelos (~2 GB)
5. Ve el frame analizado, el caption de BLIP, el comentario de GPT-2 y escucha la narracion

---

## Como conseguir clips de TETR.IO
1. Entra a [tetr.io](https://tetr.io) y crea una cuenta gratuita
2. Juega una partida en modo Solitario o versus
3. Graba la pantalla con [OBS Studio](https://obsproject.com) (gratuito) o usa la grabacion nativa del SO
4. Exporta como `.mp4` y subelo a la app

---

## Heuristica de control

El sistema NO comenta en cada frame. La logica en `heuristic.py`:

1. Convierte el frame actual a escala de grises y lo reduce a 160x90 px
2. Calcula el **MSE** (error cuadratico medio) contra el frame anterior
3. Si `MSE >= umbral` Y han pasado `>= intervalo_minimo` segundos -> genera comentario
4. Esto simula la deteccion de "cambio significativo en la escena"

```python
mse = mean((frame_actual - frame_anterior)2)
if mse >= 800 and tiempo_desde_ultimo >= 4.0:
    -> comentar
```
