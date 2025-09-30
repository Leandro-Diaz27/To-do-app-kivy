# To-Do App (Python, Kivy, SQLite)

## Requisitos
- Python 3.10+
- Windows PowerShell

## Instalación
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install kivy
```

## extension usada
SQLite de alexcvzz

## Ejecución
- Consola (Nivel 1):
```powershell
python .\main.py
```

- App Kivy (Nivel 2):
```powershell
python .\app.py
```

## Persistencia (Nivel 6)
La base de datos `tareas.db` se crea automáticamente al usar `db.py`/`gestor.py`.

## Estructura
- `main.py`: app de consola (memoria)
- `app.py`: app Kivy con SQLite (agregar, listar, editar, cambiar estado, eliminar)
- `models.py`: clases `Tarea`, `Usuario`
- `db.py`: SQLite CRUD
- `gestor.py`: funciones en memoria y DB


