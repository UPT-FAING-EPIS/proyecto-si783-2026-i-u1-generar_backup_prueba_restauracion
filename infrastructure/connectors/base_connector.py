from abc import ABC, abstractmethod
from typing import List

class DatabaseConnector(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def test_connection(self) -> bool:
        pass

    @abstractmethod
    def get_databases(self) -> List[str]:
        pass

    @abstractmethod
    def get_structure_count(self, database: str) -> int:
        """Cuenta tablas (Relacional) o colecciones (NoSQL)."""
        pass

    @abstractmethod
    def backup(self, database: str, output_path: str) -> bool:
        pass

    @abstractmethod
    def restore(self, backup_file: str, temp_db: str) -> bool:
        pass

    @abstractmethod
    def create_temp_database(self, temp_db: str) -> bool:
        pass

    @abstractmethod
    def drop_database(self, temp_db: str) -> bool:
        pass

    @abstractmethod
    def verify_backup_integrity(self, temp_db: str, original_count: int) -> bool:
        """Compara la estructura restaurada con la original."""
        pass