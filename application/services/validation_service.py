from domain.models import EngineType
from infrastructure.logger import SafeBridgeLogger


class ValidationService:

    @staticmethod
    def validate_backup(
        connector,
        backup_file: str,
        temp_db: str,
        original_count: int,
        logger: SafeBridgeLogger
    ):

        # ----------------------------------------
        # VALIDACIÓN ESPECIAL SQL SERVER
        # ----------------------------------------

        if connector.config.engine == EngineType.SQLSERVER:

            logger.info(
                "Verificando integridad del archivo .bak..."
            )

            is_valid = connector.verify_backup_integrity(
                backup_file,
                0
            )

            if not is_valid:

                raise RuntimeError(
                    "El archivo .bak está corrupto "
                    "o SQL Server no pudo validarlo."
                )

            logger.info(
                "Backup SQL Server validado correctamente."
            )

            return True

        # ----------------------------------------
        # VALIDACIÓN NORMAL RESTORE (OTROS MOTORES)
        # ----------------------------------------

        logger.info(
            f"Creando base de datos/esquema temporal '{temp_db}'..."
        )

        connector.create_temp_database(temp_db)

        try:

            logger.info(
                f"Restaurando backup en '{temp_db}'..."
            )

            connector.restore(
                backup_file,
                temp_db
            )

            logger.info(
                "Verificando integridad estructural..."
            )

            is_valid = connector.verify_backup_integrity(
                temp_db,
                original_count
            )

            if not is_valid:

                raise RuntimeError(
                    "Fallo de integridad: "
                    "La restauración no pasó la validación."
                )

            return True

        finally:

            logger.info(
                f"Limpiando entorno: Eliminando '{temp_db}'..."
            )

            connector.drop_database(temp_db)