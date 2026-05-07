import mysql.connector
import subprocess
import os
from .base_connector import DatabaseConnector


# Rutas comunes donde XAMPP / instaladores de MySQL ponen los binarios en Windows
_MYSQL_BIN_CANDIDATES = [
    r"C:\xampp\mysql\bin",
    r"C:\xampp8\mysql\bin",
    r"C:\Program Files\MySQL\MySQL Server 8.0\bin",
    r"C:\Program Files\MySQL\MySQL Server 8.4\bin",
    r"C:\Program Files\MySQL\MySQL Server 5.7\bin",
    r"C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin",
]


def _find_mysql_binary(name: str) -> str:
    """
    Devuelve la ruta completa al binario `name` (mysqldump / mysql).
    Primero busca en el PATH del sistema; si no está, prueba las
    carpetas conocidas de XAMPP e instalaciones típicas de MySQL.
    Lanza FileNotFoundError si no lo encuentra en ningún lado.
    """
    import shutil

    # 1) PATH del sistema
    found = shutil.which(name)
    if found:
        return found

    # 2) Candidatos fijos (Windows)
    for folder in _MYSQL_BIN_CANDIDATES:
        candidate = os.path.join(folder, name + ".exe")
        if os.path.isfile(candidate):
            return candidate

    raise FileNotFoundError(
        f"No se encontró '{name}'. "
        f"Asegúrate de que MySQL/XAMPP esté instalado y su carpeta 'bin' "
        f"esté en el PATH del sistema, o agrega la ruta manualmente en "
        f"mysql_connector._MYSQL_BIN_CANDIDATES."
    )


class MySQLConnector(DatabaseConnector):

    def test_connection(self) -> bool:
        try:
            conn = mysql.connector.connect(
                host=self.config.host,
                port=self.config.port,
                user=self.config.user,
                password=self.config.password
            )
            conn.close()
            return True
        except Exception:
            return False

    def get_databases(self):
        conn = mysql.connector.connect(
            host=self.config.host,
            port=self.config.port,
            user=self.config.user,
            password=self.config.password
        )
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        dbs = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return dbs

    def get_structure_count(self, database: str) -> int:
        conn = mysql.connector.connect(
            host=self.config.host,
            port=self.config.port,
            user=self.config.user,
            password=self.config.password,
            database=database
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        count = len(cursor.fetchall())
        cursor.close()
        conn.close()
        return count

    def backup(self, database, output_path):
        mysqldump = _find_mysql_binary("mysqldump")

        env = os.environ.copy()
        env["MYSQL_PWD"] = self.config.password

        cmd = [
            mysqldump,
            f"--host={self.config.host}",
            f"--port={self.config.port}",
            f"--user={self.config.user}",
            "--single-transaction", "--routines", "--triggers",
            database
        ]

        with open(output_path, "w", encoding="utf-8") as out:
            result = subprocess.run(
                cmd, env=env, stdout=out,
                stderr=subprocess.PIPE, text=True
            )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        return True

    def restore(self, backup_file, temp_db):
        mysql_bin = _find_mysql_binary("mysql")

        env = os.environ.copy()
        env["MYSQL_PWD"] = self.config.password

        cmd = [
            mysql_bin,
            f"--host={self.config.host}",
            f"--port={self.config.port}",
            f"--user={self.config.user}",
            temp_db
        ]

        with open(backup_file, "r", encoding="utf-8") as infile:
            result = subprocess.run(
                cmd, env=env, stdin=infile,
                stderr=subprocess.PIPE, text=True
            )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        return True

    def create_temp_database(self, temp_db: str) -> bool:
        conn = mysql.connector.connect(
            host=self.config.host,
            port=self.config.port,
            user=self.config.user,
            password=self.config.password
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE `{temp_db}`")
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def drop_database(self, temp_db: str) -> bool:
        conn = mysql.connector.connect(
            host=self.config.host,
            port=self.config.port,
            user=self.config.user,
            password=self.config.password
        )
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS `{temp_db}`")
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def verify_backup_integrity(self, temp_db: str, original_count: int) -> bool:
        restored_count = self.get_structure_count(temp_db)
        return restored_count == original_count and restored_count > 0