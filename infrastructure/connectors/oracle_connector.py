import oracledb
import subprocess
from .base_connector import DatabaseConnector

class OracleConnector(DatabaseConnector):
    def _get_connection_params(self):
        return {
            "host": self.config.host,
            "port": self.config.port,
            "user": self.config.user,
            "password": self.config.password,
            "service_name": self.config.service_name
        }

    def test_connection(self) -> bool:
        try:
            conn = oracledb.connect(**self._get_connection_params())
            conn.close()
            return True
        except Exception:
            return False

    def get_databases(self):
        conn = oracledb.connect(**self._get_connection_params())
        cursor = conn.cursor()
        cursor.execute("SELECT USERNAME FROM ALL_USERS")
        dbs = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return dbs

    def get_structure_count(self, database: str) -> int:
        conn = oracledb.connect(**self._get_connection_params())
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM all_tables WHERE owner = UPPER('{database}')")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count

    def backup(self, database, output_path):
        db_string = f"{self.config.host}:{self.config.port}/{self.config.service_name}"
        cmd = [
            "exp",
            f"{self.config.user}/{self.config.password}@{db_string}",
            f"FILE={output_path}",
            f"OWNER={database}",
            "GRANTS=Y", "ROWS=Y", "COMPRESS=Y"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 and "Export terminated successfully" not in result.stdout:
            raise RuntimeError(f"Error en backup Oracle: {result.stderr or result.stdout}")
        return True

    def restore(self, backup_file, temp_db):
        db_string = f"{self.config.host}:{self.config.port}/{self.config.service_name}"
        cmd = [
            "imp",
            f"{self.config.user}/{self.config.password}@{db_string}",
            f"FILE={backup_file}",
            f"FROMUSER={self.config.user}",
            f"TOUSER={temp_db}",
            "IGNORE=Y", "GRANTS=N"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 and "Import terminated successfully" not in result.stdout:
            raise RuntimeError(f"Error en restauración Oracle: {result.stderr or result.stdout}")
        return True

    def create_temp_database(self, temp_db: str) -> bool:
        conn = oracledb.connect(**self._get_connection_params())
        cursor = conn.cursor()
        cursor.execute(f'CREATE USER {temp_db} IDENTIFIED BY temp1234')
        cursor.execute(f'GRANT CONNECT, RESOURCE TO {temp_db}')
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def drop_database(self, temp_db: str) -> bool:
        conn = oracledb.connect(**self._get_connection_params())
        cursor = conn.cursor()
        cursor.execute(f'DROP USER {temp_db} CASCADE')
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def verify_backup_integrity(self, temp_db: str, original_count: int) -> bool:
        restored_count = self.get_structure_count(temp_db.upper())
        return restored_count == original_count