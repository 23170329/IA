import gradio as gr
import numpy as np
import tempfile
import os
import wave
from moviepy import VideoFileClip, AudioFileClip

from capture import CaptureModule
from heuristic import HeuristicModule
from vision import VisionModule
from narration import NarrationModule
from tts_module import TTSModule

_vision = None
_narration = None
_tts = None


def _load_models():
    global _vision, _narration, _tts
    if _vision is None:
        _vision = VisionModule()
    if _narration is None:
        _narration = NarrationModule()
    if _tts is None:
        _tts = TTSModule()


def _build_timeline_audio(segments, sample_rate, video_duration=None):
    if not segments:
        duration = video_duration if video_duration is not None else 1.0
        return sample_rate, np.zeros(int(sample_rate * duration), dtype=np.float32)

    result_chunks = []
    prev_end_time = 0.0

    for timestamp, audio_np in segments:
        audio_np = audio_np.astype(np.float32)
        audio_duration = len(audio_np) / sample_rate

        gap = max(0.0, timestamp - prev_end_time)
        if gap > 0:
            silence = np.zeros(int(sample_rate * gap), dtype=np.float32)
            result_chunks.append(silence)

        result_chunks.append(audio_np)
        prev_end_time = timestamp + audio_duration

    result_chunks.append(np.zeros(int(sample_rate * 0.5), dtype=np.float32))

    combined = np.concatenate(result_chunks)

    if video_duration is not None:
        target_samples = int(sample_rate * video_duration)
        if len(combined) < target_samples:
            padding = np.zeros(target_samples - len(combined), dtype=np.float32)
            combined = np.concatenate([combined, padding])
        elif len(combined) > target_samples:
            combined = combined[:target_samples]

    peak = np.abs(combined).max()
    if peak > 0:
        combined = combined / peak * 0.92

    return sample_rate, combined


def _write_wav(filepath, sample_rate, data):
    data_int16 = (data * 32767).astype(np.int16)
    with wave.open(filepath, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(data_int16.tobytes())


def analyze_video(video_path, threshold, interval, progress=gr.Progress(track_tqdm=True)):
    if video_path is None:
        return None, "--", "--", "--", "--", None, "Sube un video primero.", None

    try:
        _load_models()
    except Exception as e:
        return None, "--", "--", "--", "--", None, f"Error cargando modelos: {e}", None

    try:
        capture = CaptureModule(video_path)
    except Exception as e:
        return None, "--", "--", "--", "--", None, f"Error abriendo video: {e}", None

    heuristic = HeuristicModule(threshold=float(threshold), min_interval=float(interval))

    events_log = []
    audio_segments = []
    last_frame = None
    last_caption = "--"
    last_state = "--"
    last_en = "--"
    last_es = "--"
    sample_rate = None
    intro_done = False

    total_frames = capture.get_total_samples(sample_rate=2.0)
    frame_count = 0

    for frame_rgb, timestamp in progress.tqdm(
        capture.extract_frames(sample_rate=2.0),
        desc="Analizando frames",
        total=total_frames,
    ):
        frame_count += 1
        force_intro = not intro_done

        heuristic.feed_frame(frame_rgb, timestamp)

        heuristic.analyze_board_state(frame_rgb, timestamp)
        is_gameover = heuristic.game_over_detected

        if is_gameover and not heuristic.has_commented("gameover"):
            should_comment = True
            force_comment = True
            heuristic.mark_commented("gameover")
        elif heuristic.game_over_detected and heuristic.has_commented("gameover"):
            should_comment = False
            force_comment = False
        elif force_intro:
            should_comment = True
            force_comment = True
        else:
            should_comment = heuristic.should_comment(timestamp)
            force_comment = False

        if not should_comment:
            continue

        caption = _vision.caption_frame(frame_rgb)

        caption_lower = caption.lower()
        if any(kw in caption_lower for kw in ["game over", "game-over", "gameover", "defeat", "failed", "you lost", "play again", "try again", "score screen", "final score"]):
            heuristic.game_over_detected = True
            if not heuristic.has_commented("gameover"):
                is_gameover = True
                heuristic.mark_commented("gameover")

        pacing = heuristic.get_pacing(timestamp)
        hint = None
        if is_gameover:
            hint = "gameover"
        elif heuristic.is_board_full:
            hint = "peligro"
        elif pacing == "nervioso":
            hint = "nervioso"

        if force_comment:
            heuristic.should_comment(timestamp, force=True)

        forced = "intro" if force_intro else None
        state, en_text, es_text = _narration.generate_commentary(caption, force_state=forced, hint=hint)
        intro_done = True

        sr, audio_np = _tts.synthesize(es_text)
        sample_rate = sr

        audio_segments.append((timestamp, audio_np))

        last_frame = frame_rgb
        last_caption = caption
        last_state = state
        last_en = en_text
        last_es = es_text

        ts_str = f"{int(timestamp // 60):02d}:{int(timestamp % 60):02d}"
        fill_pct = int(heuristic.fill_percentage * 100)
        events_log.append(
            f"[{ts_str}] {state.upper():10s} | {fill_pct:3d}% lleno | {caption[:60]}...\n"
            f"          {es_text}\n"
        )

    if frame_count == 0:
        return None, "--", "--", "--", "--", None, "No se pudieron extraer frames del video.", None

    if not events_log:
        log_text = (
            "No se detectaron cambios significativos.\n"
            "Prueba bajando el umbral de sensibilidad o usando un clip con mas accion."
        )
        return None, "--", "--", "--", "--", None, log_text, None

    combined_audio = _build_timeline_audio(audio_segments, sample_rate, video_duration=capture.duration)

    output_video_path = None
    video_clip = None
    audio_clip = None
    final = None
    try:
        temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_wav_name = temp_wav.name
        temp_wav.close()

        _write_wav(temp_wav_name, sample_rate, combined_audio[1])

        out_video = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
        out_video_name = out_video.name
        out_video.close()

        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(temp_wav_name)

        audio_duration = audio_clip.duration
        video_duration = video_clip.duration

        if audio_duration > video_duration:
            try:
                from moviepy import ImageClip, concatenate_videoclips
                remaining = audio_duration - video_duration
                last_frame = video_clip.get_frame(video_duration - 0.05)
                freeze_clip = ImageClip(last_frame).with_duration(remaining).with_fps(video_clip.fps)
                video_to_use = concatenate_videoclips([video_clip, freeze_clip])
            except Exception as concat_err:
                print(f"[WARN] Error al concatenar clips: {concat_err}. Usando video original recortando audio.")
                audio_clip = audio_clip.subclipped(0, video_duration)
                video_to_use = video_clip
        else:
            video_to_use = video_clip

        final = video_to_use.with_audio(audio_clip)
        final.write_videofile(out_video_name, codec="libx264", audio_codec="aac", logger=None)

        output_video_path = out_video_name
    except Exception as e:
        print(f"[WARN] No se pudo generar video con narracion: {e}")
    finally:
        if video_clip is not None:
            video_clip.close()
        if audio_clip is not None:
            audio_clip.close()
        if final is not None:
            final.close()
        try:
            if 'temp_wav_name' in locals() and os.path.exists(temp_wav_name):
                os.unlink(temp_wav_name)
        except Exception:
            pass

    log_text = "\n".join(events_log)
    return last_frame, last_caption, last_state, last_en, last_es, combined_audio, log_text, output_video_path


def test_with_sample(progress=gr.Progress(track_tqdm=True)):
    try:
        _load_models()
    except Exception as e:
        return None, "--", "--", "--", "--", None, f"Error cargando modelos: {e}", None

    frame = np.zeros((480, 320, 3), dtype=np.uint8)
    colors = [
        (0, 240, 240), (240, 160, 0), (160, 0, 240),
        (0, 240, 0), (240, 0, 0), (0, 0, 240), (240, 240, 0),
    ]
    block_size = 30
    for row in range(2, 16):
        for col in range(10):
            if np.random.random() > (row / 18):
                color = colors[(row + col) % len(colors)]
                x, y = col * block_size, row * block_size
                frame[y:y + block_size - 1, x:x + block_size - 1] = color

    heuristic = HeuristicModule()
    heuristic.analyze_board_state(frame, 5.0)
    hint = "peligro" if heuristic.is_board_full else None

    caption = _vision.caption_frame(frame)
    state, en_text, es_text = _narration.generate_commentary(caption, hint=hint)
    audio = _tts.synthesize(es_text)

    log = f"[TEST] {state.upper()} | {caption}\n{es_text}"
    return frame, caption, state, en_text, es_text, audio, log, None


CSS = """
.title-bar { text-align: center; padding: 0.5rem 0; }
.model-tag { display: inline-block; background: #f0f0f0; border-radius: 4px;
             padding: 2px 8px; font-size: 12px; margin: 2px; }
"""

with gr.Blocks(title="AI Game Commentator") as demo:

    gr.Markdown("""
# AI Game Commentator - Tetris Edition
**Sistema de IA que analiza clips de videojuegos (play.tetris.com / TETR.IO) y narra las jugadas automaticamente**

| Modulo | Modelo | Tipo |
|---|---|---|
| Vision | `Salesforce/blip-image-captioning-base` | HuggingFace #1 |
| Narracion | `gpt2` | HuggingFace #2 |
| Voz | `facebook/mms-tts-spa` | HuggingFace #3 |
""")

    with gr.Row():
        with gr.Column(scale=1):
            video_input = gr.Video(
                label="Sube tu clip de Tetris (.mp4)",
                height=260,
            )
            with gr.Accordion("Configuracion de sensibilidad", open=False):
                threshold_slider = gr.Slider(
                    minimum=10, maximum=1000, value=150, step=10,
                    label="Umbral de cambio (MSE) - mas bajo = mas comentarios",
                )
                interval_slider = gr.Slider(
                    minimum=1.0, maximum=15.0, value=2.5, step=0.5,
                    label="Intervalo minimo entre comentarios (segundos)",
                )
            with gr.Row():
                btn_analyze = gr.Button("Analizar video", variant="primary", scale=2)
                btn_test = gr.Button("Test sin video", scale=1)

        with gr.Column(scale=1):
            frame_out = gr.Image(label="Frame analizado", height=260)

    gr.Markdown("---")

    with gr.Row():
        with gr.Column():
            caption_out = gr.Textbox(
                label="BLIP detecta (ingles)",
                placeholder="Descripcion visual del frame...",
                interactive=False,
            )
            state_out = gr.Textbox(
                label="Estado del juego",
                placeholder="Estado detectado...",
                interactive=False,
            )
        with gr.Column():
            en_out = gr.Textbox(
                label="GPT-2 comenta (ingles)",
                placeholder="Comentario generado por GPT-2...",
                interactive=False,
            )
            es_out = gr.Textbox(
                label="Narracion en espanol (--> TTS)",
                placeholder="Texto que se narra en voz...",
                interactive=False,
            )

    audio_out = gr.Audio(
        label="Voz generada (MMS-TTS-SPA)",
        autoplay=True,
    )

    video_out = gr.Video(
        label="Video con narracion (descargable)",
    )

    events_out = gr.Textbox(
        label="Log de todos los eventos detectados",
        lines=10,
        interactive=False,
        placeholder="Los eventos apareceran aqui despues del analisis...",
    )

    outputs = [frame_out, caption_out, state_out, en_out, es_out, audio_out, events_out, video_out]

    btn_analyze.click(
        fn=analyze_video,
        inputs=[video_input, threshold_slider, interval_slider],
        outputs=outputs,
    )

    btn_test.click(
        fn=test_with_sample,
        inputs=[],
        outputs=outputs,
    )

    gr.Markdown("""
---
> **Nota:** La primera ejecucion descarga los modelos (~2 GB). Puede tardar varios minutos.
> Modelos guardados en cache en `~/.cache/huggingface/` para ejecuciones futuras.
""")

if __name__ == "__main__":
    demo.launch(share=False, css=CSS)
