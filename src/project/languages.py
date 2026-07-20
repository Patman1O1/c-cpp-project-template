# Builtin Imports
from typing import Final
from re import Pattern, compile, IGNORECASE

LANGUAGES: Final[dict[str, Pattern[str]]] = {
    "C": compile(r"^[Cc]$"),
    "C++": compile(r"^c(?:\+\+|pp|xx)$", IGNORECASE)
}
