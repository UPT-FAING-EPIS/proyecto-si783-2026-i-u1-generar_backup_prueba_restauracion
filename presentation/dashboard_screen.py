"""
presentation/dashboard_screen.py
Panel de control principal unificado con barra de progreso y feedback directo.
"""
import tkinter as tk
from tkinter import filedialog
from typing import Callable, List, Optional

import customtkinter as ctk

from presentation.dialogs import show_error, show_warning, ask_yes_no
from shared.config import (
    APP_NAME,
    COLOR_ERROR,
    COLOR_INFO,
    COLOR_SUCCESS,
    UI_FONT_SIZE_NORMAL,
    UI_FONT_SIZE_SMALL,
    UI_FONT_SIZE_TITLE,
)


class DashboardScreen(ctk.CTkFrame):
    """
    Panel de control principal.
    Permite seleccionar BD, ruta de backup, restaurar desde .bak y muestra el progreso.
    """

    def __init__(
        self,
        master,
        server_name: str,
        username: str,
        databases: List[str],
        default_backup_path: str,
        on_run: Callable[[str, str], None],
        on_restore: Callable[[str, Optional[str], bool], None],
        on_logout: Callable[[], None],
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        self._server_name = server_name
        self._username = username
        self._databases = databases
        self._default_backup_path = default_backup_path
        self._on_run = on_run
        self._on_restore = on_restore
        self._on_logout = on_logout

        self._progress_value: float = 0.0
        self._build_ui()

    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Construye todos los widgets del dashboard."""
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        # Cabecera con logo
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.grid_columnconfigure(1, weight=1)

        # Logo de base de datos (cilindro)
        ctk.CTkLabel(
            header,
            text="🗄️",
            font=ctk.CTkFont(size=36),
        ).grid(row=0, column=0, padx=(0, 10))

        ctk.CTkLabel(
            header,
            text=f"{APP_NAME}",
            font=ctk.CTkFont(size=UI_FONT_SIZE_TITLE, weight="bold"),
        ).grid(row=0, column=0, padx=(50, 0), sticky="w")

        ctk.CTkLabel(
            header,
            text=f"Conectado: {self._username}@{self._server_name}",
            text_color="gray",
            font=ctk.CTkFont(size=11),
        ).grid(row=0, column=1, sticky="e")

        ctk.CTkButton(
            header,
            text="Cerrar sesión",
            width=110,
            height=30,
            fg_color="transparent",
            border_width=1,
            command=self._on_logout,
        ).grid(row=0, column=2, padx=(10, 0))

        # Separador
        ctk.CTkFrame(self, height=2, fg_color=("gray80", "gray30")).grid(
            row=1, column=0, sticky="ew", padx=20
        )

        # Sección de respaldo
        backup_card = ctk.CTkFrame(self, corner_radius=12)
        backup_card.grid(row=2, column=0, sticky="ew", padx=20, pady=(16, 10))
        backup_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            backup_card,
            text="Respaldo y validación",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(16, 12))

        # Base de datos
        ctk.CTkLabel(backup_card, text="Base de datos:").grid(
            row=1, column=0, sticky="w", padx=20, pady=4
        )
        self._db_combo = ctk.CTkComboBox(
            backup_card,
            values=self._databases if self._databases else ["(sin bases disponibles)"],
            height=36,
        )
        if self._databases:
            self._db_combo.set(self._databases[0])
        self._db_combo.grid(row=1, column=1, sticky="ew", padx=(0, 20), pady=4)

        # Directorio de backup
        ctk.CTkLabel(backup_card, text="Directorio backup:").grid(
            row=2, column=0, sticky="w", padx=20, pady=4
        )
        path_frame = ctk.CTkFrame(backup_card, fg_color="transparent")
        path_frame.grid(row=2, column=1, sticky="ew", padx=(0, 20), pady=4)
        path_frame.grid_columnconfigure(0, weight=1)

        self._path_entry = ctk.CTkEntry(
            path_frame,
            placeholder_text="Ruta en el servidor SQL...",
            height=36,
        )
        self._path_entry.insert(0, self._default_backup_path)
        self._path_entry.grid(row=0, column=0, sticky="ew")

        ctk.CTkButton(
            path_frame,
            text="📁",
            width=36,
            height=36,
            command=self._browse_path,
        ).grid(row=0, column=1, padx=(4, 0))

        # Botón ejecutar respaldo
        self._run_btn = ctk.CTkButton(
            backup_card,
            text="▶  Ejecutar respaldo y validación",
            height=44,
            font=ctk.CTkFont(size=UI_FONT_SIZE_NORMAL, weight="bold"),
            command=self._on_execute_backup,
        )
        self._run_btn.grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=(14, 20)
        )

        # Nueva sección: Restaurar desde archivo .bak
        restore_card = ctk.CTkFrame(self, corner_radius=12)
        restore_card.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))
        restore_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            restore_card,
            text="Restaurar desde archivo .bak",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(14, 8))

        # Archivo .bak
        ctk.CTkLabel(restore_card, text="Archivo .bak:").grid(
            row=1, column=0, sticky="w", padx=20, pady=4
        )
        file_frame = ctk.CTkFrame(restore_card, fg_color="transparent")
        file_frame.grid(row=1, column=1, sticky="ew", padx=(0, 20), pady=4)
        file_frame.grid_columnconfigure(0, weight=1)

        self._bak_path_entry = ctk.CTkEntry(
            file_frame,
            placeholder_text="Seleccionar archivo .bak...",
            height=36,
        )
        self._bak_path_entry.grid(row=0, column=0, sticky="ew")

        ctk.CTkButton(
            file_frame,
            text="📂",
            width=36,
            height=36,
            command=self._browse_bak,
        ).grid(row=0, column=1, padx=(4, 0))

        # Nombre de la base de destino (opcional)
        ctk.CTkLabel(restore_card, text="Base destino (opcional):").grid(
            row=2, column=0, sticky="w", padx=20, pady=4
        )
        self._target_db_entry = ctk.CTkEntry(
            restore_card,
            placeholder_text="Dejar vacío para nombre automático",
            height=36,
        )
        self._target_db_entry.grid(row=2, column=1, sticky="ew", padx=(0, 20), pady=4)

        # Botón restaurar
        self._restore_btn = ctk.CTkButton(
            restore_card,
            text="▶  Restaurar backup",
            height=44,
            font=ctk.CTkFont(size=UI_FONT_SIZE_NORMAL, weight="bold"),
            command=self._on_execute_restore,
        )
        self._restore_btn.grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=(12, 16)
        )

        # Barra de progreso
        progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(8, 4))
        progress_frame.grid_columnconfigure(0, weight=1)

        self._progress_bar = ctk.CTkProgressBar(progress_frame, height=14)
        self._progress_bar.set(0)
        self._progress_bar.grid(row=0, column=0, sticky="ew")

        self._progress_label = ctk.CTkLabel(
            progress_frame,
            text="Listo",
            font=ctk.CTkFont(size=UI_FONT_SIZE_SMALL),
            text_color="gray",
        )
        self._progress_label.grid(row=1, column=0, sticky="w", pady=(2, 0))

        # Indicador visual de completado (check ✔️) / estado
        self._status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=UI_FONT_SIZE_NORMAL, weight="bold"),
        )
        self._status_label.grid(row=5, column=0, pady=(4, 20))

    # ------------------------------------------------------------------
    # Acciones de los botones
    # ------------------------------------------------------------------

    def _browse_path(self) -> None:
        """Diálogo para seleccionar directorio de backup."""
        path = filedialog.askdirectory(title="Seleccionar directorio de backup")
        if path:
            self._path_entry.delete(0, tk.END)
            self._path_entry.insert(0, path)

    def _browse_bak(self) -> None:
        """Seleccionar archivo .bak desde el sistema de archivos."""
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo de backup",
            filetypes=[("Backup SQL Server", "*.bak"), ("Todos los archivos", "*.*")],
        )
        if filepath:
            self._bak_path_entry.delete(0, tk.END)
            self._bak_path_entry.insert(0, filepath)

    def _on_execute_backup(self) -> None:
        """Valida y lanza el respaldo."""
        db = self._db_combo.get().strip()
        path = self._path_entry.get().strip()

        if not db or db == "(sin bases disponibles)":
            show_error(self, "Error", "Selecciona una base de datos.")
            return
        if not path:
            show_error(self, "Error", "Ingresa el directorio de backup.")
            return

        self.set_running(True)
        self._on_run(db, path)

    def _on_execute_restore(self) -> None:
        """Valida y lanza la restauración desde .bak."""
        bak_file = self._bak_path_entry.get().strip()
        
        if not bak_file:
            show_error(self, "Error", "Selecciona un archivo .bak.")
            return
        
        if not bak_file.lower().endswith(".bak"):
            show_error(self, "Error", "El archivo debe tener extensión .bak")
            return

        target = self._target_db_entry.get().strip() or None
        
        # Preguntar si quiere forzar sobrescritura
        force = False
        if target:
            # Si el usuario puso un nombre específico, preguntamos
            force = ask_yes_no(
                self,
                "Confirmar restauración",
                f"¿Deseas sobrescribir la base '{target}' si ya existe?\n\n"
                "Si eliges 'No', la restauración se cancelará si la base ya existe."
            )
        
        self.set_running(True)
        self._on_restore(bak_file, target, force)

    # ------------------------------------------------------------------
    # Control de estado de la interfaz
    # ------------------------------------------------------------------

    def set_running(self, running: bool) -> None:
        """Habilita/deshabilita los botones de ejecución."""
        state = "disabled" if running else "normal"
        text_run = "⏳ Procesando..." if running else "▶  Ejecutar respaldo y validación"
        text_restore = "⏳ Restaurando..." if running else "▶  Restaurar backup"
        self._run_btn.configure(state=state, text=text_run)
        self._restore_btn.configure(state=state, text=text_restore)

    def start_operation(self) -> None:
        """Prepara la UI para una operación larga."""
        self._progress_bar.set(0)
        self._progress_label.configure(text="Preparando...")
        self._status_label.configure(text="")
        self._progress_bar.configure(mode="determinate")

    def update_progress(self, message: str) -> None:
        """
        Actualiza la barra y el mensaje de progreso.
        Se llama desde los hilos de trabajo.
        """
        progress = self._progress_value
        if "Verificando" in message:
            progress = 0.1
        elif "Generando" in message:
            progress = 0.3
        elif "Restaurando" in message and "copia" in message:
            progress = 0.55
        elif "Restaurando" in message:
            progress = 0.55
        elif "Ejecutando prueba" in message:
            progress = 0.8
        elif "Limpiando" in message:
            progress = 0.95
        elif "Prueba exitosa" in message or "completada" in message:
            progress = 1.0
        elif "ERROR" in message or "falló" in message.lower():
            progress = self._progress_value
        elif "ya existe" in message:
            progress = self._progress_value

        if progress != self._progress_value:
            self._progress_value = progress
            self._progress_bar.set(progress)
        self._progress_label.configure(text=message)

    def operation_finished(self, success: bool, message: str) -> None:
        """Muestra el resultado final con el check ✔️ o ❌."""
        self.set_running(False)
        self._progress_bar.set(1.0)
        self._progress_label.configure(text="Completado")
        self._status_label.configure(
            text=message,
            text_color=COLOR_SUCCESS if success else COLOR_ERROR,
        )

    def update_databases(self, databases: List[str]) -> None:
        """Actualiza la lista de bases de datos."""
        self._databases = databases
        self._db_combo.configure(values=databases if databases else ["(sin bases)"])
        if databases:
            self._db_combo.set(databases[0])