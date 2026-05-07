import customtkinter as ctk
import os
from datetime import datetime
from application.services.connection_service import ConnectionService
from application.services.backup_service import BackupProcess
from infrastructure.logger import SafeBridgeLogger
from presentation.terminal_widget import TerminalWidget
from presentation.settings_window import SettingsWindow
from domain.models import EngineType


# Extensión correcta de archivo de backup según el motor
_BACKUP_EXTENSIONS = {
    EngineType.SQLSERVER:   "bak",
    EngineType.MYSQL:       "sql",
    EngineType.POSTGRESQL:  "sql",
    EngineType.ORACLE:      "dmp",
    EngineType.SQLITE:      "db",
}


class DashboardWindow:
    def __init__(self, master, config, login_window=None):
        self.master = master
        self.config = config
        self.login_window = login_window

        # Inicializar atributos que se usarán después
        self.terminal = None
        self.logger = None
        self.databases = []
        self.backup_btn = None
        self.db_var = None
        self.folder_path = None

        self.master.title(f"SafeBridge Dashboard - {config.engine.value}")
        self.master.geometry("1100x700")
        self.master.minsize(900, 600)

        # Configurar el grid primero
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        # Construir la UI completa (incluye el terminal)
        self._build_ui()

        # Ahora que el terminal existe, crear el logger
        self.logger = SafeBridgeLogger(terminal_callback=self._log_to_terminal)

        # Cargar bases de datos
        try:
            self.databases = ConnectionService.get_databases_list(config)
            if hasattr(self, 'db_menu') and self.db_menu is not None:
                self.db_menu.configure(values=self.databases)
                if self.databases:
                    self.db_var.set(self.databases[0])
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error cargando bases de datos: {e}")
            else:
                print(f"Error cargando bases de datos: {e}")

        if self.logger:
            self.logger.info(
                f"Conexión establecida: {config.host}:{config.port}"
            )

        self.master.protocol("WM_DELETE_WINDOW", self._logout)

    def _build_ui(self):
        # --- SIDEBAR (Panel Izquierdo) ---
        sidebar = ctk.CTkFrame(self.master, width=260, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(
            sidebar, text="SafeBridge",
            font=ctk.CTkFont(size=22, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        ctk.CTkLabel(
            sidebar,
            text=f"{self.config.engine.value} | {self.config.user}",
            text_color="gray"
        ).grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Base de Datos
        ctk.CTkLabel(
            sidebar, text="Base de Datos",
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")

        self.db_var = ctk.StringVar(value="Cargando...")
        self.db_menu = ctk.CTkOptionMenu(
            sidebar, values=["Cargando..."], variable=self.db_var
        )
        self.db_menu.grid(row=3, column=0, padx=20, pady=(5, 15), sticky="ew")

        # Ruta de Destino
        ctk.CTkLabel(
            sidebar, text="Ruta de Destino",
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")

        self.folder_path = ctk.StringVar(value=os.path.abspath("backups"))
        self.folder_btn = ctk.CTkButton(
            sidebar, text="Cambiar Carpeta",
            fg_color="transparent", border_width=1,
            text_color=("gray10", "gray90"),
            command=self._select_folder
        )
        self.folder_btn.grid(
            row=5, column=0, padx=20, pady=(5, 10), sticky="ew"
        )

        # Botones Inferiores
        self.settings_btn = ctk.CTkButton(
            sidebar, text="Ajustes", height=35,
            command=self._open_settings
        )
        self.settings_btn.grid(
            row=7, column=0, padx=20, pady=10, sticky="ew"
        )

        self.logout_btn = ctk.CTkButton(
            sidebar, text="Cerrar Sesión", height=35,
            fg_color="#C62828", hover_color="#B71C1C",
            command=self._logout
        )
        self.logout_btn.grid(
            row=8, column=0, padx=20, pady=(10, 20), sticky="ew"
        )

        # --- MAIN CONTENT (Panel Derecho) ---
        main_frame = ctk.CTkFrame(
            self.master, corner_radius=15, fg_color="transparent"
        )
        main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Action Card
        action_card = ctk.CTkFrame(main_frame, corner_radius=10)
        action_card.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        ctk.CTkLabel(
            action_card, text="Gestor de Operaciones",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left", padx=25, pady=25)

        self.backup_btn = ctk.CTkButton(
            action_card, text="EJECUTAR BACKUP",
            font=ctk.CTkFont(weight="bold"),
            height=45, width=200,
            command=self._start_backup
        )
        self.backup_btn.pack(side="right", padx=25, pady=25)

        # Terminal / Consola de Logs
        terminal_container = ctk.CTkFrame(main_frame, corner_radius=10)
        terminal_container.grid(row=1, column=0, sticky="nsew")

        ctk.CTkLabel(
            terminal_container, text="Registro del Sistema",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.terminal = TerminalWidget(terminal_container)
        self.terminal.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _select_folder(self):
        from tkinter import filedialog
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            if self.logger:
                self.logger.info(
                    f"Carpeta de destino actualizada: {folder}"
                )

    def _start_backup(self):
        if not self.db_var:
            return

        db_name = self.db_var.get()
        if not db_name or db_name in (
            "N/A", "Sin bases de datos", "Cargando..."
        ):
            if self.logger:
                self.logger.error(
                    "Error: Seleccione una base de datos válida."
                )
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # ── Extensión correcta según el motor ──────────────────────────
        extension = _BACKUP_EXTENSIONS.get(
            self.config.engine, "bak"
        )
        # ───────────────────────────────────────────────────────────────

        output_file = os.path.join(
            self.folder_path.get(),
            f"backup_{db_name}_{timestamp}.{extension}"
        )

        self.backup_btn.configure(state="disabled", text="PROCESANDO...")

        process = BackupProcess(
            self.config, db_name, output_file, self.logger
        )
        thread = process.start()

        self._monitor_process(thread, process, self.backup_btn)

    def _monitor_process(self, thread, process, button):
        if thread and thread.is_alive():
            self.master.after(
                100, self._monitor_process, thread, process, button
            )
        else:
            button.configure(state="normal", text="EJECUTAR BACKUP")
            try:
                status, msg = process.queue.get_nowait()
                if self.logger:
                    if status == "success":
                        self.logger.info(f"ÉXITO: {msg}")
                    else:
                        self.logger.error(f"ERROR: {msg}")
            except Exception:
                pass

    def _log_to_terminal(self, message):
        """Callback seguro para el logger."""
        if self.terminal is not None:
            self.terminal.write(message)

    def _open_settings(self):
        SettingsWindow(
            self.master,
            self.config,
            self.logger
        )

    def _logout(self):
        if self.login_window:
            self.login_window.root.deiconify()
        self.master.destroy()