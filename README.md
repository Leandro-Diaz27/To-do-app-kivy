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

Capturas de pantalla 

Agregar tarea "Maqueta de biologia"
<img width="794" height="619" alt="Agregar Tarea" src="https://github.com/user-attachments/assets/93e6485f-5f9e-493c-adcc-a7f65f3d7d67" />

Tarea ya agregada
<img width="793" height="624" alt="Tarea agregada" src="https://github.com/user-attachments/assets/d32a72cc-7bf5-4557-af05-512f9ec16488" />

Cambio de estado a "completada"
<img width="799" height="619" alt="Cambio de estado" src="https://github.com/user-attachments/assets/08f104a4-8dbe-4da9-bcb6-bdae531569b5" />

Editar tarea con un " :D "
<img width="793" height="620" alt="Editar tarea" src="https://github.com/user-attachments/assets/a1035d80-a83f-45c0-a1f0-0439fdb60815" />

Eliminar tarea "informe de matematicas"
<img width="788" height="274" alt="Eliminar tarea" src="https://github.com/user-attachments/assets/11b1aa75-d59a-446b-8ddc-e0b9e1a78208" />

Base de datos
<img width="605" height="257" alt="Base de datos" src="https://github.com/user-attachments/assets/03da0232-8ff3-4dfc-b061-a9199836e8fa" />
