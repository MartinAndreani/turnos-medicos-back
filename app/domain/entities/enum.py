from enum import Enum

class JornadaEnum(str, Enum):
    mañana = "mañana"
    manana = "manana"   # alternativa sin virgulilla
    tarde = "tarde"
    noche = "noche"
