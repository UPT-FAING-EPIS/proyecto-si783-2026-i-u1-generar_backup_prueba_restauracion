"""
presentation/login_screen.py
Pantalla de login: server, usuario y contraseña, con logo de base de datos.
"""
import tkinter as tk
from typing import Callable

import customtkinter as ctk

from shared.config import (
    APP_NAME,
    APP_VERSION,
    COLOR_ERROR,
    COLOR_INFO,
    UI_FONT_SIZE_NORMAL,
    UI_FONT_SIZE_TITLE,
)


class LoginScreen(ctk.CTkFrame):
    """
    Frame de inicio de sesión.
    Llama a on_login_success(server, username, password) al autenticar.
    """

    def __init__(
        self,
        master,
        on_login_success: Callable[[str, str, str], None],
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        self._on_success = on_login_success
        self._build_ui()

    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Construye los widgets de la pantalla de login."""
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        # Logo de base de datos
        ctk.CTkLabel(
            self,
            text="🗄️",
            font=ctk.CTkFont(size=64),
        ).grid(row=0, column=0, pady=(30, 4))

        # Título
        ctk.CTkLabel(
            self,
            text=f"{APP_NAME}",
            font=ctk.CTkFont(size=UI_FONT_SIZE_TITLE, weight="bold"),
        ).grid(row=1, column=0, pady=(0, 4))

        ctk.CTkLabel(
            self,
            text=f"v{APP_VERSION} — Gestión de Respaldos SQL Server",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        ).grid(row=2, column=0, pady=(0, 30))

        # Card central
        card = ctk.CTkFrame(self, corner_radius=16)
        card.grid(row=3, column=0, padx=60, pady=10, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        # Servidor
        ctk.CTkLabel(card, text="Servidor SQL Server", anchor="w").grid(
            row=0, column=0, sticky="w", padx=20, pady=(20, 2)
        )
        self._server_entry = ctk.CTkEntry(
            card,
            placeholder_text="localhost\\SQLEXPRESS",
            height=38,
        )
        self._server_entry.grid(row=1, column=0, sticky="ew", padx=20)

        # Usuario
        ctk.CTkLabel(card, text="Usuario", anchor="w").grid(
            row=2, column=0, sticky="w", padx=20, pady=(14, 2)
        )
        self._user_entry = ctk.CTkEntry(
            card,
            placeholder_text="sa",
            height=38,
        )
        self._user_entry.grid(row=3, column=0, sticky="ew", padx=20)

        # Contraseña
        ctk.CTkLabel(card, text="Contraseña", anchor="w").grid(
            row=4, column=0, sticky="w", padx=20, pady=(14, 2)
        )
        self._pwd_entry = ctk.CTkEntry(
            card,
            placeholder_text="••••••••",
            show="•",
            height=38,
        )
        self._pwd_entry.grid(row=5, column=0, sticky="ew", padx=20)

        # Mensaje de error
        self._error_label = ctk.CTkLabel(
            card, text="", text_color=COLOR_ERROR, font=ctk.CTkFont(size=11)
        )
        self._error_label.grid(row=6, column=0, pady=(8, 0))

        # Botón conectar
        self._connect_btn = ctk.CTkButton(
            card,
            text="Conectar",
            height=40,
            font=ctk.CTkFont(size=UI_FONT_SIZE_NORMAL, weight="bold"),
            command=self._on_connect,
        )
        self._connect_btn.grid(row=7, column=0, sticky="ew", padx=20, pady=(16, 20))

        # Bind Enter
        for entry in (self._server_entry, self._user_entry, self._pwd_entry):
            entry.bind("<Return>", lambda _e: self._on_connect())

    # ------------------------------------------------------------------

    def _on_connect(self) -> None:
        """Valida campos y llama al callback de éxito."""
        server = self._server_entry.get().strip()
        username = self._user_entry.get().strip()
        password = self._pwd_entry.get()

        if not server:
            self._show_error("El campo Servidor es obligatorio.")
            return
        if not username:
            self._show_error("El campo Usuario es obligatorio.")
            return
        if not password:
            self._show_error("El campo Contraseña es obligatorio.")
            return

        self._error_label.configure(text="")
        self._connect_btn.configure(state="disabled", text="Conectando…")
        self.after(50, lambda: self._on_success(server, username, password))

    def _show_error(self, message: str) -> None:
        """Muestra un mensaje de error en el formulario."""
        self._error_label.configure(text=message)
        self._connect_btn.configure(state="normal", text="Conectar")

    def reset(self) -> None:
        """Restablece el estado del botón (útil si la conexión falla)."""
        self._connect_btn.configure(state="normal", text="Conectar")
        self._pwd_entry.delete(0, tk.END)