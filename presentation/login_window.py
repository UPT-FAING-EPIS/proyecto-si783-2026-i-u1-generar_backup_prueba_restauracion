import customtkinter as ctk
from tkinter import messagebox
from domain.models import ConnectionConfig, EngineType
from application.services.connection_service import ConnectionService
from infrastructure.security import save_connections, load_connections
from presentation.dashboard_window import DashboardWindow

DEFAULT_PORTS = {
    EngineType.MYSQL: "3306",
    EngineType.POSTGRESQL: "5432",
    EngineType.SQLSERVER: "1433",
    EngineType.ORACLE: "1521",
    EngineType.SQLITE: ""
}

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("SafeBridge | Autenticación")
        self.root.geometry("450x680")
        self.root.resizable(False, False)

        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(pady=30, padx=30, fill="both", expand=True)

        ctk.CTkLabel(self.main_frame, text="SafeBridge", font=ctk.CTkFont(family="Roboto", size=28, weight="bold")).pack(pady=(25, 5))
        ctk.CTkLabel(self.main_frame, text="Gestión empresarial de respaldos", text_color="gray").pack(pady=(0, 20))

        self.form_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.form_frame.pack(fill="both", expand=True, padx=20)

        ctk.CTkLabel(self.form_frame, text="Motor de Base de Datos", anchor="w").pack(fill="x")
        self.engine_var = ctk.StringVar(value=EngineType.MYSQL.value)
        self.engine_menu = ctk.CTkOptionMenu(self.form_frame, values=[e.value for e in EngineType], variable=self.engine_var, command=self._on_engine_change)
        self.engine_menu.pack(fill="x", pady=(0, 15))

        self.fields = {}
        self._create_input("Host / IP", "host", "localhost")
        self._create_input("Puerto", "port", DEFAULT_PORTS[EngineType.MYSQL])
        self._create_input("Usuario", "user", "root")
        self._create_input("Contraseña", "password", "", show="*")

        self.dynamic_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.dynamic_frame.pack(fill="x")

        self.service_entry = ctk.CTkEntry(self.dynamic_frame, placeholder_text="Service Name")
        self.use_tcp_var = ctk.BooleanVar(value=False)
        self.use_tcp_check = ctk.CTkCheckBox(self.dynamic_frame, text="Conexión TCP/IP", variable=self.use_tcp_var)

        self.save_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(self.form_frame, text="Recordar credenciales", variable=self.save_var).pack(anchor="w", pady=15)

        self.connect_btn = ctk.CTkButton(self.main_frame, text="Conectar", height=40, font=ctk.CTkFont(weight="bold"), command=self._connect)
        self.connect_btn.pack(fill="x", padx=20, pady=(10, 5))

        self.test_btn = ctk.CTkButton(self.main_frame, text="Probar Conexión", height=40, fg_color="transparent", border_width=1, text_color=("gray10", "gray90"), command=self._test_connection)
        self.test_btn.pack(fill="x", padx=20, pady=(0, 25))

        self._update_dynamic_fields()
        self._load_saved_connections()

    def _create_input(self, label, key, default, show=""):
        ctk.CTkLabel(self.form_frame, text=label, anchor="w").pack(fill="x")
        entry = ctk.CTkEntry(self.form_frame, show=show)
        entry.pack(fill="x", pady=(0, 10))
        entry.insert(0, default)
        self.fields[key] = entry

    def _on_engine_change(self, engine_str):
        engine = EngineType(engine_str)
        self.fields["port"].delete(0, "end")
        self.fields["port"].insert(0, DEFAULT_PORTS.get(engine, ""))
        self._update_dynamic_fields()

    def _update_dynamic_fields(self):
        engine = EngineType(self.engine_var.get())
        self.use_tcp_check.pack_forget()
        self.service_entry.pack_forget()
        if engine == EngineType.SQLSERVER:
            self.use_tcp_check.pack(anchor="w", pady=(5, 5))
        elif engine == EngineType.ORACLE:
            self.service_entry.pack(fill="x", pady=(5, 5))

    def _get_config(self) -> ConnectionConfig:
        engine = EngineType(self.engine_var.get())
        config = ConnectionConfig(
            engine=engine,
            host=self.fields["host"].get(),
            port=int(self.fields["port"].get()) if self.fields["port"].get().isdigit() else 0,
            user=self.fields["user"].get(),
            password=self.fields["password"].get()
        )
        if engine == EngineType.ORACLE:
            config.service_name = self.service_entry.get()
        elif engine == EngineType.SQLSERVER:
            config.use_tcp = self.use_tcp_var.get()
        return config

    def _test_connection(self):
        config = self._get_config()
        if ConnectionService.test_connection(config):
            messagebox.showinfo("Éxito", "Conexión exitosa.")
        else:
            messagebox.showerror("Error", "No se pudo conectar.")

    def _connect(self):
        config = self._get_config()

        if self.save_var.get():
            existing = load_connections()

            existing.append({
                "engine": config.engine.value,
                "host": config.host,
                "port": config.port,
                "user": config.user,
                "password": config.password,
                "service_name": getattr(config, "service_name", "")
            })

            save_connections(existing)

        try:
            self.root.withdraw()

            dash = ctk.CTkToplevel(self.root)

            DashboardWindow(
                dash,
                config,
                login_window=self
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _load_saved_connections(self):
        saved = load_connections()

        if not saved:
            return

        last = saved[-1]

        self.fields["host"].delete(0, "end")
        self.fields["host"].insert(0, last["host"])

        self.fields["port"].delete(0, "end")
        self.fields["port"].insert(0, str(last["port"]))

        self.fields["user"].delete(0, "end")
        self.fields["user"].insert(0, last["user"])

        self.fields["password"].delete(0, "end")
        self.fields["password"].insert(0, last["password"])

        self.engine_var.set(last["engine"])
        self._on_engine_change(last["engine"])