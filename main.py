"""
Aplicación To-Do (Nivel 1: Consola)

Menú básico por terminal para practicar listas, dicts e input().

Permite:
- Agregar tarea
- Mostrar tareas
- Salir

Las tareas se almacenan en memoria como diccionarios:
{"titulo": str, "estado": "pendiente" | "completada"}
"""

from typing import List, Dict


def mostrar_menu() -> None:
    """Pinta el menú de opciones en la terminal."""
    print("\n=== To-Do App (Consola) ===")
    print("1) Agregar tarea")
    print("2) Mostrar tareas")
    print("3) Salir")


def agregar_tarea(tareas: List[Dict[str, str]]) -> None:
    """Solicita un título y agrega una tarea pendiente a la lista."""
    titulo = input("Título de la tarea: ").strip()
    if not titulo:
        print("⚠️  El título no puede estar vacío.")
        return
    tareas.append({"titulo": titulo, "estado": "pendiente"})
    print("✅ Tarea agregada.")


def mostrar_tareas(tareas: List[Dict[str, str]]) -> None:
    """Imprime las tareas existentes con su índice."""
    if not tareas:
        print("(sin tareas)")
        return
    print("\nListado de tareas:")
    for indice, tarea in enumerate(tareas, start=1):
        print(f"{indice}. {tarea['titulo']} - {tarea['estado']}")


def main() -> None:
    """Bucle principal de la app de consola."""
    tareas: List[Dict[str, str]] = []
    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-3): ").strip()

        if opcion == "1":
            agregar_tarea(tareas)
        elif opcion == "2":
            mostrar_tareas(tareas)
        elif opcion == "3":
            print("👋 Saliendo... ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")


if __name__ == "__main__":
    main()


