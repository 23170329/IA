import random
import warnings
from typing import Tuple

SPANISH_TEMPLATES = {
    "intro": [
        "Bienvenidos a esta partida de Tetris! El tablero esta limpio y la batalla esta a punto de comenzar.",
        "Arranca la partida! Un tablero vacio lleno de posibilidades. Hasta donde llegara el jugador hoy?",
        "Comienza el combate de bloques! El jugador toma posicion y la concentracion esta al maximo.",
        "El tablero aparece en pantalla y la partida da inicio. Todo puede pasar a partir de ahora.",
    ],
    "normal": [
        "El jugador mantiene el ritmo, colocando cada pieza con precision y sin perder la calma.",
        "Movimientos fluidos y control total del tablero. Por ahora, todo esta completamente bajo control.",
        "Cada pieza en su sitio. La estrategia se construye bloque a bloque, con paciencia y vision.",
        "Buen ritmo de juego. El jugador no muestra senales de panico y domina la situacion.",
        "Gestion solida del tablero. Todavia queda mucho margen de maniobra y la partida esta viva.",
        "Las piezas fluyen con naturalidad. Este jugador sabe exactamente lo que esta haciendo.",
        "Sin prisa pero sin pausa. Cada decision se toma con cabeza fria y mano firme.",
        "El juego avanza a buen ritmo. La situacion esta controlada y el jugador mantiene la compostura.",
    ],
    "peligro": [
        "Alerta maxima! El stack esta llegando al tope. Un solo error y todo se acaba!",
        "El jugador esta en peligro critico! Las piezas no dan respiro y el espacio se agota rapidamente.",
        "Esto se pone muy tenso! El tablero esta a punto de colapsar. Necesita actuar ya mismo!",
        "Las piezas se acumulan sin control! El jugador esta al borde del abismo. Concentracion maxima!",
        "Situacion desesperada! El techo esta cerca y el tiempo corre en su contra. Ahora o nunca!",
        "Peligro inminente! El stack amenaza con alcanzar el limite. Cada movimiento cuenta ahora!",
        "El tablero grita auxilio! Las columnas estan desbordadas y la presion es insoportable.",
        "Esto es una pesadilla! El jugador intenta sobrevivir mientras las piezas se apilan sin piedad.",
    ],
    "limpieza": [
        "Increible! Lineas eliminadas con maestria absoluta. El tablero respira de nuevo!",
        "Tetris! Una limpieza perfecta que le da oxigeno al jugador justo cuando mas lo necesitaba.",
        "Combo devastador! Las lineas caen una tras otra y el rival recibe el contragolpe completo.",
        "Que jugada! Multiples lineas eliminadas de un golpe. Eso si es control total del tablero!",
        "Brillante ejecucion! El jugador aprovecha el momento y limpia el tablero con elegancia absoluta.",
        "Eso estuvo perfecto! Las lineas desaparecen y la presion se alivia al instante. Magistral!",
        "Una limpieza impecable! El tablero queda despejado y el jugador recupera el control por completo.",
        "Espectacular! Esas lineas no sabian lo que se les venia encima. Pura clase y precision!",
        "El jugador activa el modo bestia! Lineas limpias, espacio ganado y la partida toma otro giro.",
    ],
    "ataque": [
        "El jugador lanza un ataque brutal! Lineas de basura enviadas al rival. Eso va a doler!",
        "Contraataque feroz! El rival recibe una lluvia de lineas completamente inesperada.",
        "Ofensiva total! El jugador no da tregua y presiona al oponente sin ninguna piedad.",
        "Jugada agresiva y calculada! Las lineas de penalizacion caen sobre el rival como un martillo.",
        "El jugador va a por todas! Ataque directo al corazon del tablero rival. Dominio absoluto!",
        "Sin misericordia! El jugador convierte su defensa en un ataque devastador para el oponente.",
    ],
    "nervioso": [
        "El jugador acelera el ritmo! Las piezas caen una tras otra. Esto se esta poniendo intenso!",
        "La velocidad aumenta! El jugador esta reaccionando por instinto. Ritmo frenetico en el tablero!",
        "Se nota la presion! Las piezas se colocan a toda velocidad. El tiempo corre en su contra.",
        "Ritmo endiablado! El jugador no para de colocar piezas. La concentracion esta al limite.",
        "Todo se acelera! Las decisiones tienen que ser instantaneas. Esto es adrenalina pura!",
        "El jugador esta en modo acelerado! Las piezas caen y el responde sin dudar ni un segundo.",
        "La frecuencia de juego se dispara. El jugador esta metido de lleno en el ritmo de la partida.",
        "Que ritmo tan trepidante! Las piezas estan entrando a una velocidad impresionante.",
    ],
    "gameover": [
        "Y asi termina la batalla! El tablero no pudo aguantar mas presion. Una derrota epica pero digna.",
        "Game over. El stack alcanzo el limite y el jugador cayo con honor en el campo de batalla.",
        "Cayo el guerrero! Pero esta derrota es solo el principio. La proxima partida sera completamente diferente.",
        "El tablero dijo basta. Game over, pero con la frente bien en alto. Hasta la proxima batalla!",
        "Se acabo la partida! Una batalla feroz que llego a su inevitable fin. Gran esfuerzo del jugador!",
        "La pantalla de derrota aparece. Pero cada game over es una leccion que hace al jugador mas fuerte.",
        "Fin de la partida! El jugador lo dio todo hasta el ultimo momento. Respeto total por ese esfuerzo.",
        "Game over, pero que partida. El jugador dejo el corazon en el tablero. Volveremos mas fuertes!",
    ],
}

STATE_KEYWORDS = {
    "gameover": [
        "game over", "game-over", "gameover", "over screen", "end screen",
        "dark screen", "black screen", "defeat", "failed", "you lost",
        "death screen", "lost the game", "screen with text",
        "play again", "try again", "score screen", "final score", "replay button",
    ],
    "peligro": [
        "top", "near the top", "almost full", "filled", "overflow",
        "high blocks", "stacked high", "reaching the top", "almost",
        "too high", "blocks reach", "blocks are high",
    ],
    "limpieza": [
        "cleared", "clear", "disappear", "empty row", "lines cleared",
        "row clear", "tetris", "flash", "vanish", "empty board",
        "clean board", "rows removed",
    ],
    "ataque": [
        "garbage", "attack", "sending", "opponent", "rival",
        "multiplayer", "versus", "two boards", "both",
    ],
    "normal": [
        "falling", "piece", "block", "playing", "tetromino",
        "game board", "colorful", "screenshot", "video game",
    ],
}

_last_used: dict[str, str] = {}


def _pick_template(state: str) -> str:
    templates = SPANISH_TEMPLATES.get(state, SPANISH_TEMPLATES["normal"])
    last = _last_used.get(state)
    candidates = [t for t in templates if t != last]
    if not candidates:
        candidates = templates
    chosen = random.choice(candidates)
    _last_used[state] = chosen
    return chosen


class NarrationModule:
    MODEL_NAME = "gpt2"

    def __init__(self):
        print(f"[Narracion] Cargando {self.MODEL_NAME}...")
        from transformers import pipeline
        warnings.filterwarnings("ignore", message=".*generation_config.*", category=UserWarning)
        warnings.filterwarnings("ignore", message=".*max_new_tokens.*max_length.*", category=UserWarning)
        self.pipe = pipeline(
            "text-generation",
            model=self.MODEL_NAME,
        )
        print("[Narracion] GPT-2 listo")

    def _detect_state(self, caption: str) -> str:
        caption_lower = caption.lower()
        for state in ["gameover", "ataque", "peligro", "limpieza", "normal"]:
            if any(kw in caption_lower for kw in STATE_KEYWORDS[state]):
                return state
        return "normal"

    def _gpt2_commentary(self, caption: str) -> str:
        prompt = (
            f"As an epic esports commentator for Tetris: '{caption}'. "
            f"Exciting live commentary:"
        )
        try:
            result = self.pipe(
                prompt,
                max_new_tokens=50,
                do_sample=True,
                temperature=0.85,
                repetition_penalty=1.3,
                pad_token_id=50256,
            )
            raw = result[0]["generated_text"][len(prompt):].strip()
            raw = raw.replace("\n", " ")
            for sep in [".", "!", "?"]:
                if sep in raw:
                    raw = raw.split(sep)[0] + sep
                    break
            return raw[:140].strip() or "Incredible play!"
        except Exception:
            return "What a moment in this Tetris battle!"

    def generate_commentary(self, caption: str, force_state: str | None = None, hint: str | None = None) -> Tuple[str, str, str]:
        state = force_state if force_state else self._detect_state(caption)
        if hint == "gameover":
            state = "gameover"
        elif hint == "peligro" and state in ["normal", "nervioso"]:
            state = "peligro"
        elif hint == "nervioso" and state == "normal":
            state = "nervioso"
        english_text = self._gpt2_commentary(caption)
        spanish_text = _pick_template(state)
        return state, english_text, spanish_text
