import os
import threading
import queue

from datetime import datetime

from application.services.connection_service import ConnectionService
from application.services.validation_service import ValidationService

from infrastructure.logger import SafeBridgeLogger


class BackupProcess:

    def __init__(
        self,
        config,
        db_name,
        output_path,
        logger: SafeBridgeLogger
    ):

        self.config = config
        self.db_name = db_name
        self.output_path = output_path
        self.logger = logger

        self.queue = queue.Queue()

        self.thread = None

    def start(self):

        self.thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self.thread.start()

        return self.thread

    def _run(self):

        try:

            connector = ConnectionService.get_connector(
                self.config
            )

            # ----------------------------------------
            # Analizar estructura original
            # ----------------------------------------

            self.logger.info(
                "Analizando estructura original..."
            )

            original_count = connector.get_structure_count(
                self.db_name
            )

            if original_count <= 0:

                raise RuntimeError(
                    "La base de datos no contiene "
                    "tablas válidas."
                )

            # ----------------------------------------
            # Generar backup
            # ----------------------------------------

            self.logger.info(
                f"Generando backup de "
                f"'{self.db_name}' -> "
                f"'{self.output_path}'"
            )

            connector.backup(
                self.db_name,
                self.output_path
            )

            # ----------------------------------------
            # Validar archivo generado
            # ----------------------------------------

            if not os.path.exists(
                self.output_path
            ):

                raise RuntimeError(
                    "El archivo backup "
                    "no fue generado."
                )

            if os.path.getsize(
                self.output_path
            ) <= 0:

                raise RuntimeError(
                    "El archivo backup está vacío."
                )

            self.logger.info(
                "Backup generado correctamente."
            )

            # ----------------------------------------
            # Restauración de prueba
            # ----------------------------------------

            temp_db = (
                "tmp_validation_"
                + datetime.now().strftime(
                    "%Y%m%d%H%M%S"
                )
            )

            self.logger.info(
                "Iniciando restauración de prueba..."
            )

            ValidationService.validate_backup(
                connector,
                self.output_path,
                temp_db,
                original_count,
                self.logger
            )

            self.logger.info(
                "Validación completada exitosamente."
            )

            self.queue.put((
                "success",
                "Backup generado y validado correctamente."
            ))

        except Exception as e:

            self.logger.error(
                f"Error en backup: {str(e)}"
            )

            self.queue.put((
                "error",
                str(e)
            ))