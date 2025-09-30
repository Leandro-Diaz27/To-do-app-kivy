"""
Nivel 2/6: Prototipo en Kivy con persistencia SQLite

Qué hace esta pantalla:
- Permite ingresar un título y agregarlo a la base SQLite
- Muestra todas las tareas cargadas desde la base
- Permite cambiar estado y eliminar, actualizando la base y la UI

Notas de implementación:
- Se usa `ListaTareas` (ScrollView + GridLayout) para simplificar
  la creación de filas con controles por ítem sin usar .kv.
- `gestor.py` encapsula la lógica de validación y acceso a `db.py`.
"""

from typing import List, Dict

import gestor

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout


class ListaTareas(ScrollView):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)
        self.app_ref = app_ref
        self.size_hint = (1, 1)
        self.do_scroll_x = False
        self.do_scroll_y = True

        # Grid de 4 columnas: Título | Estado | Cambiar | Eliminar | Editar
        # En móviles/ventanas chicas, las celdas se ajustan al ancho
        self.contenedor = GridLayout(cols=5, spacing=6, size_hint_y=None, padding=[8, 8, 8, 8])
        self.contenedor.bind(minimum_height=self.contenedor.setter("height"))
        self.add_widget(self.contenedor)

    def actualizar(self, tareas: List[Dict[str, str]]):
        self.contenedor.clear_widgets()
        if not tareas:
            orig_cols = self.contenedor.cols
            self.contenedor.cols = 1
            self.contenedor.add_widget(Label(text="(sin tareas)", color=(0, 0, 0, 1), size_hint_y=None, height=dp(40)))
            self.contenedor.cols = orig_cols
            return
        # Encabezados
        for header in ("Título", "Estado", "Cambiar", "Eliminar", "Editar"):
            self.contenedor.add_widget(Label(text=header, bold=True, color=(0,0,0,1), size_hint_y=None, height=dp(30)))

        for t in tareas:
            self.contenedor.add_widget(Label(text=t["titulo"], color=(0, 0, 0, 1), size_hint_y=None, height=dp(40), halign="left", valign="middle"))
            self.contenedor.add_widget(Label(text=t["estado"], color=(0, 0, 0, 1), size_hint_y=None, height=dp(40)))
            boton = Button(text="Cambiar", size_hint_y=None, height=dp(36))
            boton.bind(on_release=lambda *_btn, idt=t["id"], estado=t["estado"]: self._toggle(idt, estado))
            self.contenedor.add_widget(boton)
            btn_del = Button(text="Eliminar", size_hint_y=None, height=dp(36))
            btn_del.bind(on_release=lambda *_btn, idt=t["id"]: self._eliminar(idt))
            self.contenedor.add_widget(btn_del)
            btn_edit = Button(text="Editar", size_hint_y=None, height=dp(36))
            btn_edit.bind(on_release=lambda *_btn, idt=t["id"], titulo=t["titulo"]: self._editar(idt, titulo))
            self.contenedor.add_widget(btn_edit)

    def _toggle(self, id_tarea: int, estado_actual: str):
        nuevo = "completada" if estado_actual == "pendiente" else "pendiente"
        try:
            gestor.actualizar_estado_db(id_tarea, nuevo)
        except Exception as exc:
            self.app_ref.mensaje.text = f"Error al actualizar: {exc}"
            return
        self.app_ref.recargar_lista()

    def _eliminar(self, id_tarea: int):
        try:
            gestor.eliminar_tarea_db(id_tarea)
        except Exception as exc:
            self.app_ref.mensaje.text = f"Error al eliminar: {exc}"
            return
        self.app_ref.recargar_lista()

    def _editar(self, id_tarea: int, titulo_actual: str):
        caja = BoxLayout(orientation="vertical", spacing=6, padding=6)
        entrada = TextInput(text=titulo_actual, multiline=False)
        caja.add_widget(entrada)
        acciones = BoxLayout(size_hint_y=None, height=dp(40), spacing=6)
        btn_ok = Button(text="Guardar")
        btn_cancel = Button(text="Cancelar")
        acciones.add_widget(btn_ok)
        acciones.add_widget(btn_cancel)
        caja.add_widget(acciones)

        popup = Popup(title="Editar tarea", content=caja, size_hint=(0.8, 0.4))

        def guardar(*_):
            nuevo = entrada.text.strip()
            try:
                gestor.actualizar_titulo_db(id_tarea, nuevo)
            except Exception as exc:
                self.app_ref.mensaje.text = f"Error al editar: {exc}"
                return
            popup.dismiss()
            self.app_ref.recargar_lista()

        btn_ok.bind(on_release=guardar)
        btn_cancel.bind(on_release=lambda *_: popup.dismiss())
        popup.open()


class TareasRecycleView(RecycleView):
    pass


class TodoLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Fondo blanco para mejor contraste
        Window.clearcolor = (1, 1, 1, 1)
        self.orientation = "vertical"
        self.padding = [10, 10, 10, 10]
        self.spacing = 8

        self.tareas: List[Dict[str, str]] = []

        # Inicializar DB y cargar tareas persistidas (se hará tras crear la lista)

        cabecera = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(48), spacing=8)
        self.titulo_input = TextInput(hint_text="Escribe una tarea...", multiline=False)
        cabecera.add_widget(self.titulo_input)
        self.boton_agregar = Button(text="Agregar tarea", size_hint_x=None, width=dp(160))
        self.boton_agregar.bind(on_release=self.on_agregar)
        cabecera.add_widget(self.boton_agregar)
        self.add_widget(cabecera)

        self.lista = ListaTareas(app_ref=self, size_hint=(1, 1))
        self.add_widget(self.lista)

        # Mensajes de estado
        self.mensaje = Label(text="", color=(0.9, 0.2, 0.2, 1), size_hint=(1, None), height=dp(24))
        self.add_widget(self.mensaje)

        # Ahora sí: inicializar DB, cargar tareas y refrescar lista
        gestor.init_db()
        self._cargar_desde_db()
        self.lista.actualizar(self.tareas)
        self.mensaje.text = f"Tareas: {len(self.tareas)}"

    def on_agregar(self, *_):
        titulo = self.titulo_input.text.strip()
        if not titulo:
            self.mensaje.text = "El título no puede estar vacío."
            return
        self.mensaje.text = ""
        # Guardar en DB y recargar listado
        try:
            gestor.agregar_tarea_db(titulo)
        except Exception as exc:
            self.mensaje.text = f"Error al guardar: {exc}"
            return
        self._cargar_desde_db()
        self.titulo_input.text = ""
        self.lista.actualizar(self.tareas)
        self.mensaje.text = f"Tareas: {len(self.tareas)}"

    def _cargar_desde_db(self):
        registros = gestor.listar_tareas_db()
        # registros: List[Tuple[id, titulo, estado]]
        self.tareas = [{"id": t[0], "titulo": t[1], "estado": t[2]} for t in registros]

    def recargar_lista(self):
        self._cargar_desde_db()
        self.lista.actualizar(self.tareas)
        self.mensaje.text = f"Tareas: {len(self.tareas)}"


class TodoApp(App):
    def build(self):
        self.title = "To-Do App"
        return TodoLayout()


if __name__ == "__main__":
    TodoApp().run()


