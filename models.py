from typing import List

"""Modelos de dominio (Nivel 5 - POO)

Este módulo define las clases que representan los conceptos
principales de la aplicación: una `Tarea` y un `Usuario`.
Permite trabajar con objetos (POO) en lugar de diccionarios sueltos.
"""


class Tarea:
    """Representa una tarea del to-do.

    Atributos:
    - titulo: texto descriptivo de la tarea
    - estado: "pendiente" o "completada"
    """

    def __init__(self, titulo: str, estado: str = "pendiente"):
        self.titulo = titulo
        self.estado = estado

    def __repr__(self) -> str:
        return f"Tarea(titulo={self.titulo!r}, estado={self.estado!r})"


class Usuario:
    """Representa un usuario con su propia lista de tareas."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.tareas: List[Tarea] = []

    def agregar_tarea(self, titulo: str) -> None:
        """Crea una `Tarea` pendiente y la agrega a la colección."""
        self.tareas.append(Tarea(titulo))

    def listar_tareas(self) -> List[Tarea]:
        """Devuelve una copia de la lista de tareas."""
        return list(self.tareas)

    def completar_tarea(self, indice: int) -> bool:
        """Marca como completada la tarea dada por su índice.

        Devuelve True si se pudo completar, False si el índice es inválido.
        """
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].estado = "completada"
            return True
        return False


