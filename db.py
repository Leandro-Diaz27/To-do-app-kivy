"""
Persistencia con SQLite (Nivel 6)

Este módulo encapsula todo acceso a la base `tareas.db`.
Provee funciones CRUD usadas por `gestor.py` y la UI.
"""

from __future__ import annotations

import sqlite3
from typing import Iterable, List, Optional, Tuple


DB_PATH = "tareas.db"


def get_connection() -> sqlite3.Connection:
    """Abre una conexión a la base de datos local.

    Usa un archivo `tareas.db` en la carpeta del proyecto. Si no existe,
    SQLite lo crea automáticamente.
    """
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    """Crea la tabla `tareas` si no existe."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                estado TEXT NOT NULL
            )
            """
        )
        conn.commit()


def insertar_tarea(titulo: str, estado: str = "pendiente") -> int:
    """Inserta una fila y devuelve el ID autoincremental."""
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO tareas (titulo, estado) VALUES (?, ?)", (titulo, estado)
        )
        conn.commit()
        return cur.lastrowid


def listar_tareas() -> List[Tuple[int, str, str]]:
    """Devuelve [(id, titulo, estado)] ordenadas por id."""
    with get_connection() as conn:
        cur = conn.execute("SELECT id, titulo, estado FROM tareas ORDER BY id ASC")
        return list(cur.fetchall())


def actualizar_tarea(id_: int, titulo: Optional[str] = None, estado: Optional[str] = None) -> int:
    """Actualiza campos no nulos. Devuelve cantidad de filas afectadas."""
    if titulo is None and estado is None:
        return 0

    campos: list[str] = []
    valores: list[str] = []
    if titulo is not None:
        campos.append("titulo = ?")
        valores.append(titulo)
    if estado is not None:
        campos.append("estado = ?")
        valores.append(estado)
    valores.append(id_)

    sql = f"UPDATE tareas SET {', '.join(campos)} WHERE id = ?"
    with get_connection() as conn:
        cur = conn.execute(sql, valores)
        conn.commit()
        return cur.rowcount


def eliminar_tarea(id_: int) -> int:
    """Elimina una fila por ID. Devuelve filas afectadas (0 o 1)."""
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM tareas WHERE id = ?", (id_,))
        conn.commit()
        return cur.rowcount


