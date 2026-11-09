"""Minimal Gmusic sample surface with a deliberate greeting bug."""


def greeting(name: str = "alumno") -> str:
    return f"Hola {name}, Bienvenido a Gmusic Academy"


def health() -> dict[str, str]:
    return {"status": "ok", "product": "Gmusic Academy"}
