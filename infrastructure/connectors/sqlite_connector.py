import sqlite3
import os
import shutil

from .base_connector import DatabaseConnector

class SQLiteConnector(DatabaseConnector):
    def __init__(self, config):
        super().__init__(config)
        self.db_path = config.host

    def test_connection(self):
        if not os.path.isfile(self.db_path):
            raise FileNotFoundError(f"No se encuentra {self.db_path}")

        conn = sqlite3.connect(self.db_path)
        conn.close()
        return True

    def get_databases(self):
        return [os.path.splitext(os.path.basename(self.db_path))[0]]

    def get_structure_count(self, database: str) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )

        tables = cursor.fetchall()

        cursor.close()
        conn.close()

        return len(tables)

    def backup(self, database, output_path):
        shutil.copy2(self.db_path, output_path)
        return True

    def restore(self, backup_file, temp_db):
        temp_path = os.path.join(
            os.path.dirname(backup_file),
            f"{temp_db}.db"
        )

        shutil.copy2(backup_file, temp_path)

        self._temp_restore_path = temp_path

        return True

    def create_temp_database(self, temp_db):
        return True

    def drop_database(self, temp_db):
        if hasattr(self, '_temp_restore_path'):
            if os.path.exists(self._temp_restore_path):
                os.remove(self._temp_restore_path)

        return True

    def verify_backup_integrity(self, temp_db: str, original_count: int) -> bool:
        temp_path = getattr(self, '_temp_restore_path', None)

        if not temp_path:
            return False

        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )

        restored_tables = cursor.fetchall()

        cursor.close()
        conn.close()

        restored_count = len(restored_tables)

        return restored_count == original_count and restored_count > 0