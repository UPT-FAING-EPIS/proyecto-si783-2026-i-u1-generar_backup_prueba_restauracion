"""
presentation/app_controller.py
Controlador principal de la aplicación.
"""
import threading
from pathlib import Path
from typing import Optional

import customtkinter as ctk

from application.orchestrator import BackupOrchestrator
from application.restore_backup_use_case import RestoreBackupUseCase
from domain.entities import ConnectionConfig, OperationStatus
from infrastructure.sql_server_repository import SqlServerRepository
from presentation.dashboard_screen import DashboardScreen
from presentation.dialogs import show_error, show_success, show_warning
from presentation.login_screen import LoginScreen
from shared.config import (
    APP_NAME,
    APP_VERSION,
    BASE_DIR,
    COLOR_ERROR,
    COLOR_INFO,
    COLOR_SUCCESS,
    UI_COLOR_SCHEME,
    UI_THEME,
)
from shared.logger import UILogger, build_session_id


class AppController(ctk.CTk):
    """
    Ventana raíz de la aplicación.
    Maneja la navegación entre LoginScreen y DashboardScreen.
    """

    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode(UI_THEME)
        ctk.set_default_color_theme(UI_COLOR_SCHEME)

        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("900x700")
        self.minsize(800, 600)

        self._config: Optional[ConnectionConfig] = None
        self._repository = SqlServerRepository()
        self._logger: Optional[UILogger] = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._show_login()

    # ------------------------------------------------------------------
    # Navegación
    # ------------------------------------------------------------------

    def _clear_frames(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()

    def _show_login(self) -> None:
        """Muestra la pantalla de login centrada."""
        self._clear_frames()
        frame = LoginScreen(
            master=self,
            on_login_success=self._handle_login,
        )
        frame.grid(row=0, column=0, sticky="nsew")

    def _show_main(
        self,
        server: str,
        username: str,
        databases: list,
        default_backup_path: str,
    ) -> None:
        """Muestra el dashboard a pantalla completa."""
        self._clear_frames()
        self._dashboard = DashboardScreen(
            master=self,
            server_name=server,
            username=username,
            databases=databases,
            default_backup_path=default_backup_path,
            on_run=self._handle_run,
            on_restore=self._handle_restore,
            on_logout=self._handle_logout,
        )
        self._dashboard.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # ------------------------------------------------------------------
    # Handlers
    # ------------------------------------------------------------------

    def _handle_login(self, server: str, username: str, password: str) -> None:
        """Valida credenciales y navega al dashboard."""
        config = ConnectionConfig(
            server=server,
            username=username,
            password=password,
        )

        def _do_connect() -> None:
            ok = self._repository.test_connection(config)
            if not ok:
                self.after(
                    0,
                    lambda: self._on_login_failed(
                        "No se pudo conectar al servidor.\n\nVerifica:\n• El nombre del servidor\n• Las credenciales"
                    ),
                )
                return

            has_perm = self._repository.validate_permissions(config)
            if not has_perm:
                self.after(
                    0,
                    lambda: self._on_login_failed(
                        "Permisos insuficientes.\n\nEl usuario necesita rol sysadmin."
                    ),
                )
                return

            databases = self._repository.list_databases(config)
            default_path = self._repository.get_default_backup_path(config)
            self._config = config
            self.after(
                0,
                lambda: self._show_main(server, username, databases, default_path),
            )

        threading.Thread(target=_do_connect, daemon=True).start()

    def _on_login_failed(self, message: str) -> None:
        """Muestra error en ventana emergente y restablece el login."""
        show_error(self, "Error de conexión", message)
        for widget in self.winfo_children():
            if isinstance(widget, LoginScreen):
                widget.reset()
                break

    def _handle_logout(self) -> None:
        """Cierra sesión y vuelve al login."""
        self._config = None
        self._show_login()

    def _handle_run(self, database_name: str, backup_path: str) -> None:
        """Inicia la orquestación completa (backup + validación)."""
        if not self._config:
            return

        session_id = build_session_id(database_name)
        self._logger = UILogger(
            session_id=session_id,
            ui_callback=self._ui_log_callback,
        )

        self._dashboard.start_operation()

        orchestrator = BackupOrchestrator(
            repository=self._repository,
            logger=self._logger,
        )

        def _run() -> None:
            result = orchestrator.run(
                config=self._config,
                database_name=database_name,
                backup_directory=backup_path,
                progress_callback=self._dashboard.update_progress,
            )
            self._logger.save_json()
            self.after(0, lambda: self._on_operation_done(result))

        threading.Thread(target=_run, daemon=True).start()

    def _handle_restore(self, backup_file: str, target_database: Optional[str], force: bool) -> None:
        """Inicia la restauración de un archivo .bak cargado por el usuario."""
        if not self._config:
            return

        session_id = build_session_id("restore_backup")
        self._logger = UILogger(
            session_id=session_id,
            ui_callback=self._ui_log_callback,
        )

        self._dashboard.start_operation()

        use_case = RestoreBackupUseCase(
            repository=self._repository,
            logger=self._logger,
        )

        default_dir = self._repository.get_default_backup_path(self._config)

        def _run() -> None:
            result = use_case.execute(
                config=self._config,
                backup_file=backup_file,
                data_directory=default_dir,
                log_directory=default_dir,
                target_database=target_database,
                force=force,
                progress_callback=self._dashboard.update_progress,
            )
            self._logger.save_json()
            self.after(0, lambda: self._on_restore_done(result))

        threading.Thread(target=_run, daemon=True).start()

    def _on_operation_done(self, result) -> None:
        """Finaliza la operación de respaldo + validación."""
        if result.status == OperationStatus.SUCCESS:
            self._dashboard.operation_finished(
                success=True, message="✔️ Prueba exitosa"
            )
            show_success(
                self,
                "Proceso completado",
                "El respaldo y la validación se completaron correctamente."
            )
        else:
            self._dashboard.operation_finished(
                success=False, message=f"❌ {result.error_message or 'Error'}"
            )
            show_error(
                self,
                "Error",
                f"El proceso falló:\n\n{result.error_message or 'Error desconocido'}"
            )

    def _on_restore_done(self, result) -> None:
        """Finaliza la restauración desde archivo."""
        if result.status == OperationStatus.SUCCESS:
            self._dashboard.operation_finished(
                success=True, message=f"✔️ Restauración completada: {result.sandbox_database}"
            )
            show_success(
                self,
                "Restauración completada",
                f"Base de datos restaurada como:\n{result.sandbox_database}"
            )
        elif result.status == OperationStatus.CANCELLED:
            self._dashboard.operation_finished(
                success=False, message="⚠️ Restauración cancelada"
            )
            show_warning(
                self,
                "Restauración cancelada",
                result.error_message or "La base de datos ya existe."
            )
        else:
            self._dashboard.operation_finished(
                success=False, message=f"❌ Error al restaurar"
            )
            show_error(
                self,
                "Error",
                f"La restauración falló:\n\n{result.error_message or 'Error desconocido'}"
            )

    # ------------------------------------------------------------------
    # Callbacks de UI desde hilos
    # ------------------------------------------------------------------

    def _ui_log_callback(self, level: str, message: str) -> None:
        """Recibe logs desde el logger."""
        pass