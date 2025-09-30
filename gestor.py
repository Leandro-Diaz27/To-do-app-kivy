"""
Nivel 3: Modularización y manejo de errores.

Este módulo expone funciones para:
- operar en memoria (listas de diccionarios) para los primeros niveles
- y funciones adaptadoras hacia SQLite (usando `db.py`) para persistencia

La idea es que la UI llame aquí y esta capa decida detalles de validación,
errores y llamadas a la base de datos.
"""

from typing import Dict, List, Tuple

from models import Tarea
import db


# --- Operaciones en memoria ---

def agregar_tarea_mem(lista: List[Dict[str, str]], titulo: str) -> None:
    """Agrega una tarea pendiente a una lista en memoria.

    Se usa en el Nivel 1/3 cuando aún no hay base de datos.
    """
    if not titulo:
        raise ValueError("El título no puede estar vacío")
    lista.append({"titulo": titulo, "estado": "pendiente"})


def listar_tareas_mem(lista: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Devuelve una copia de la lista de tareas en memoria."""
    return list(lista)


def completar_tarea_mem(lista: List[Dict[str, str]], indice: int) -> None:
    """Marca como completada la tarea por índice en memoria."""
    if indice < 0 or indice >= len(lista):
        raise IndexError("Índice fuera de rango")
    lista[indice]["estado"] = "completada"


# --- Operaciones con SQLite ---

def init_db() -> None:
    """Inicializa la base de datos (idempotente)."""
    db.init_db()


def agregar_tarea_db(titulo: str) -> int:
    """Valida y persiste una tarea nueva en SQLite."""
    if not titulo:
        raise ValueError("El título no puede estar vacío")
    return db.insertar_tarea(titulo)


def listar_tareas_db() -> List[Tuple[int, str, str]]:
    """Lista todas las tareas desde SQLite."""
    return db.listar_tareas()


def completar_tarea_db(id_tarea: int) -> int:
    """Marca como completada una tarea por ID en SQLite."""
    return db.actualizar_tarea(id_tarea, estado="completada")


def eliminar_tarea_db(id_tarea: int) -> int:
    """Elimina una tarea por ID en SQLite."""
    return db.eliminar_tarea(id_tarea)


def actualizar_estado_db(id_tarea: int, nuevo_estado: str) -> int:
    """Cambia el estado de una tarea en SQLite."""
    return db.actualizar_tarea(id_tarea, estado=nuevo_estado)


def actualizar_titulo_db(id_tarea: int, nuevo_titulo: str) -> int:
    """Actualiza el título de una tarea en SQLite."""
    if not nuevo_titulo:
        raise ValueError("El título no puede estar vacío")
    return db.actualizar_tarea(id_tarea, titulo=nuevo_titulo)


