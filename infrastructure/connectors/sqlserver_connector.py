"""
Conector SQL Server.
"""

import pyodbc
import subprocess
import os

from .base_connector import DatabaseConnector


class SQLServerConnector(DatabaseConnector):

    def _connection_string(self, db="master"):
        """
        Construye cadena de conexión SQL Server.
        """

        if getattr(self.config, "use_tcp", False):
            server = (
                f"{self.config.host},"
                f"{self.config.port}"
            )
        else:
            server = self.config.host

        return (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={db};"
            f"UID={self.config.user};"
            f"PWD={self.config.password};"
            f"TrustServerCertificate=yes;"
            f"Encrypt=yes;"
        )

    def _get_server_param(self):
        """
        Devuelve parámetro servidor para sqlcmd.
        """

        if getattr(self.config, "use_tcp", False):
            return (
                f"{self.config.host},"
                f"{self.config.port}"
            )

        return self.config.host

    def test_connection(self):
        """
        Verifica conexión SQL Server.
        """

        conn = pyodbc.connect(
            self._connection_string(),
            timeout=5
        )

        conn.close()

        return True

    def get_databases(self):
        """
        Obtiene bases de datos usuario.
        """

        conn = pyodbc.connect(self._connection_string())

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT name
            FROM sys.databases
            WHERE database_id > 4
            """
        )

        result = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return result

    def get_structure_count(self, database: str) -> int:
        """
        Cuenta tablas reales usuario.
        """

        conn = pyodbc.connect(
            self._connection_string(database)
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM sys.tables
            WHERE is_ms_shipped = 0
            """
        )

        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return count

    def backup(self, database, output_path):
        """
        Realiza backup nativo SQL Server (.bak).
        """

        server = self._get_server_param()

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        cmd = [
            "sqlcmd",
            "-S", server,
            "-U", self.config.user,
            "-P", self.config.password,
            "-C",
            "-Q",
            (
                f"BACKUP DATABASE [{database}] "
                f"TO DISK = N'{output_path}' "
                f"WITH INIT, CHECKSUM"
            )
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip() or result.stdout.strip()
            )

        if (
            not os.path.exists(output_path)
            or os.path.getsize(output_path) <= 0
        ):
            raise RuntimeError(
                "El backup no fue generado."
            )

        return True

    def restore(self, backup_file, temp_db):
        """
        No se utiliza restauración temporal.
        """

        return True

    def create_temp_database(self, temp_db):
        """
        No se utiliza base temporal.
        """

        return True

    def drop_database(self, temp_db):
        """
        No se utiliza base temporal.
        """

        return True

    def verify_backup_integrity(
        self,
        temp_db: str,
        original_count: int
    ) -> bool:
        """
        Verifica integridad del archivo .bak usando:
        RESTORE VERIFYONLY

        NO restaura la BD.
        """

        conn = pyodbc.connect(
            self._connection_string(),
            autocommit=True
        )

        cursor = conn.cursor()

        try:

            cursor.execute(
                f"""
                RESTORE VERIFYONLY
                FROM DISK = N'{temp_db}'
                WITH CHECKSUM
                """
            )

            cursor.close()
            conn.close()

            return True

        except Exception as e:

            cursor.close()
            conn.close()

            print(f"[DEBUG] VERIFYONLY ERROR: {e}")

            return False