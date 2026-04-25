````markdown name=FD01-Informe-Factibilidad.md
<center>

[comment]: <img src="./media/media/image1.png" style="width:1.088in;height:1.46256in" alt="escudo.png" />

![./media/media/image1.png](./media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERIA**

**Escuela Profesional de Ingeniería de Sistemas**

**Proyecto *SQL-SafeBridge: Orquestador de Respaldos y Validación de Integridad (SQL Server)***

Curso: *Base de Datos II*

Docente: *Ing. Patrick José Cuadros Quiroga*

Integrantes:

***Sierra Ruiz, Iker Alberto (2023077090)***

***Cortez Mamani, Julio Samuel (2023077283)***

**Tacna – Perú**

***2026***

**  
**
</center>

<div style="page-break-after: always; visibility: hidden"></div>

Sistema *SQL-SafeBridge: Orquestador de Respaldos y Validación de Integridad (SQL Server)*

Informe de Factibilidad

Versión *1.0*

|CONTROL DE VERSIONES||||||
| :-: | :- | :- | :- | :- | :- |
|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo|
|1\.0|IASR / JSCM|Ing. P. Cuadros|Ing. P. Cuadros|27/03/2026|Versión Original (adaptada a SQL-SafeBridge)|

<div style="page-break-after: always; visibility: hidden"></div>

# **INDICE GENERAL**

[1. Descripción del Proyecto](#_Toc52661346)

[2. Riesgos](#_Toc52661347)

[3. Análisis de la Situación actual](#_Toc52661348)

[4. Estudio de Factibilidad](#_Toc52661349)

[4.1 Factibilidad Técnica](#_Toc52661350)

[4.2 Factibilidad económica](#_Toc52661351)

[4.3 Factibilidad Operativa](#_Toc52661352)

[4.4 Factibilidad Legal](#_Toc52661353)

[4.5 Factibilidad Social](#_Toc52661354)

[4.6 Factibilidad Ambiental](#_Toc52661355)

[5. Análisis Financiero](#_Toc52661356)

[6. Conclusiones](#_Toc52661357)

<div style="page-break-after: always; visibility: hidden"></div>

**<u>Informe de Factibilidad</u>**

1. <span id="_Toc52661346" class="anchor"></span>**Descripción del Proyecto**

    1.1. Nombre del proyecto

    **SQL-SafeBridge: Orquestador de Respaldos y Validación de Integridad (SQL Server).**

    1.2. Duración del proyecto

    Cuatro (4) meses, equivalentes a un ciclo académico universitario (marzo – julio 2026). El análisis de factibilidad económica se proyecta a un horizonte de un (1) año con el fin de evaluar el retorno de la inversión.

    1.3. Descripción

    En la actualidad, la pérdida de datos representa uno de los principales riesgos operativos para cualquier organización que dependa de sistemas de información. Sin embargo, disponer de un archivo de respaldo no garantiza, por sí solo, que dicho respaldo sea utilizable en una emergencia: múltiples incidentes reales evidencian que los archivos `.bak` pueden quedar corruptos, incompletos, inaccesibles por permisos o no restaurables por errores en la operación o por falta de validación.

    Ante esta problemática, el presente proyecto propone desarrollar **SQL-SafeBridge**, una herramienta de escritorio profesional orientada a la administración de bases de datos SQL Server que automatiza el ciclo crítico de **Copia de Seguridad (Backup)** y **Validación de Recuperación (Restore Test)**. El sistema no se limita a ejecutar comandos T-SQL de manera aislada; orquesta el proceso end-to-end: genera el respaldo, restaura automáticamente el `.bak` en una base de datos temporal (sandbox/espejo), ejecuta validaciones técnicas de integridad y consistencia, y finalmente registra evidencias completas (logs y métricas) para auditoría.

    La solución se implementará siguiendo principios de **Arquitectura Limpia (Clean Architecture)**, separando responsabilidades en capas: (i) **UI Layer** mediante `customtkinter` (interfaz moderna con modo oscuro), (ii) **Use Case Layer** para la orquestación de procesos (backup → restore → validación → limpieza), (iii) **Infrastructure Layer** para la ejecución de comandos T-SQL (BACKUP, RESTORE, DBCC CHECKDB) y conectividad vía `pyodbc`, y (iv) **Entity Layer** para los modelos y reportes de ejecución.

    1.4. Objetivos

       1.4.1 Objetivo general

    Desarrollar una solución de software de escritorio que automatice y asegure la continuidad de datos en SQL Server mediante la ejecución orquestada de copias de seguridad y pruebas de restauración, validando la integridad de los respaldos en un entorno sandbox y generando trazabilidad completa mediante evidencias y auditoría.

        1.4.2 Objetivos Específicos

    - Diseñar e implementar una arquitectura basada en **Clean Architecture** para desacoplar UI, casos de uso, infraestructura y entidades.
    - Implementar un módulo de **respaldo** que ejecute backups full (y opcionalmente diferencial/log según alcance), generando archivos `.bak` con nomenclatura automática (`BD_YYYYMMDD_HHMMSS_FULL.bak`).
    - Implementar un módulo de **restauración espejo (sandbox)** que restaure el backup en una base temporal usando `WITH MOVE` para reubicar archivos `.mdf` y `.ldf` y evitar conflictos con producción.
    - Implementar un módulo de **validación de integridad** que ejecute `DBCC CHECKDB` y verificaciones adicionales (conteo/consistencia básica) entre la base original y la restaurada.
    - Delegar autenticación a SQL Server y habilitar funciones solo si el usuario posee permisos administrativos (por ejemplo, rol `sysadmin` o equivalente definido).
    - Implementar gestión de evidencias mediante generación de **logs detallados** por ejecución (pasos, tiempos, resultados, errores) y actualización de estado en tiempo real en la interfaz.
    - Implementar **limpieza automática** del entorno sandbox (DROP de la BD de prueba) al finalizar la validación, optimizando almacenamiento.

<div style="page-break-after: always; visibility: hidden"></div>

2. <span id="_Toc52661347" class="anchor"></span>**Riesgos**

    A continuación se identifican los principales riesgos que podrían afectar el éxito del proyecto, clasificados por categoría, junto con su probabilidad estimada y la estrategia de mitigación correspondiente.

    | Categoría      | Riesgo                                                                 | Probabilidad | Estrategia de Mitigación                                                                                                   |
    |----------------|------------------------------------------------------------------------|:------------:|----------------------------------------------------------------------------------------------------------------------------|
    | Técnico        | Corrupción o backup no restaurable (archivo `.bak` inconsistente)      | Media        | Restauración automática en sandbox + `DBCC CHECKDB`; registrar evidencia y marcar como no válido ante cualquier error.     |
    | Técnico        | Conflictos de archivos físicos al restaurar (mdf/ldf en rutas ocupadas)| Media        | Usar `RESTORE FILELISTONLY` para detectar logical names y aplicar `WITH MOVE` a rutas controladas para el sandbox.         |
    | Técnico        | Incompatibilidad de versiones / drivers ODBC                            | Media        | Definir versiones objetivo (SQL Server 2022, Python 3.12+, ODBC Driver 18); documentar prerequisitos y usar `venv`.        |
    | Operativo      | Caída del servidor durante backup/restore                               | Baja         | Manejo de excepciones, reintentos controlados cuando aplique, y logs de fallas; validación de estado antes de continuar.   |
    | Almacenamiento | Falta de espacio en disco por acumulación de backups/sandboxes          | Media        | Políticas de retención, alertas de umbral y limpieza automática; parámetros configurables de ruta y retención.             |
    | Seguridad      | Exposición de credenciales o acceso no autorizado a backups             | Media        | No persistir contraseñas; control por roles (sysadmin); permisos NTFS en rutas; opción de cifrado a nivel de storage.      |
    | Seguridad      | Manipulación de evidencias (logs)                                       | Baja         | Logs con sellos de tiempo, rotación y almacenamiento protegido; opcional: hash de logs por ejecución.                       |
    | Operativo      | Errores en scripts T-SQL o en orquestación Python                        | Media        | Pruebas unitarias/integración, escenarios de prueba, y CI con GitHub Actions para validar calidad de código.               |
    | Humano         | Abandono del proyecto por parte de un integrante                        | Baja         | Documentación continua, commits frecuentes, issues y tareas claras, revisión cruzada entre integrantes.                    |
    | Legal/Ético    | Uso indebido de backups con datos sensibles                              | Baja         | Definir política de manejo; restringir accesos; operar en entorno controlado; anonimizar datos en demos si corresponde.    |

<div style="page-break-after: always; visibility: hidden"></div>

3. <span id="_Toc52661348" class="anchor"></span>**Análisis de la Situación actual**

    3.1. Planteamiento del problema

    Las organizaciones modernas (empresas privadas e instituciones académicas) dependen de bases de datos para operar. A pesar de ello, en muchos entornos la gestión de copias de seguridad se sigue realizando de manera manual: un DBA ejecuta comandos en SSMS, sin estandarización, sin pruebas de restauración, y con registros incompletos o inexistentes.

    Esta situación produce tres problemas principales:

    1) **Alta exposición al error humano** (comandos mal escritos, rutas incorrectas, omisión de parámetros, selección errónea de base de datos).  
    2) **Falsa sensación de seguridad**: existe un `.bak`, pero no hay evidencia de que sea restaurable o consistente.  
    3) **Ausencia de trazabilidad**: no se puede responder con evidencia “quién ejecutó qué”, “cuándo”, “en qué servidor” y “cuál fue el resultado”.

    SQL-SafeBridge busca resolver esta brecha automatizando el proceso completo de continuidad de datos, incorporando un **restore test** inmediato, validaciones técnicas y evidencias auditablemente consistentes.

    3.2. Consideraciones de hardware y software

    El siguiente cuadro resume los recursos tecnológicos evaluados para el desarrollo e implantación del sistema:

    | Tipo     | Componente                 | Especificaciones                                                                                 | Estado        |
    |----------|----------------------------|--------------------------------------------------------------------------------------------------|---------------|
    | HARDWARE | Servidor de BD             | Procesador Intel Core i5 / Ryzen 5 (5.ª gen. o sup.), 8 GB RAM mínimo, 500 GB SSD               | Disponible    |
    | HARDWARE | Almacenamiento de respaldo | Disco duro externo 1 TB para redundancia de backups                                              | Por adquirir  |
    | HARDWARE | Equipos de desarrollo      | Laptop/PC serie 5 o superior, 8 GB RAM mínimo, SSD                                              | Disponible    |
    | SOFTWARE | Motor de base de datos     | SQL Server 2022 Developer Edition (licencia gratuita para desarrollo)                            | Disponible    |
    | SOFTWARE | Lenguaje de programación   | Python 3.12+ con librerías `pyodbc`, `hashlib`, `logging`, y GUI con `customtkinter`             | Disponible    |
    | SOFTWARE | Conectividad               | ODBC Driver 18 for SQL Server + protocolo TDS vía `pyodbc`                                       | Disponible    |
    | SOFTWARE | Control de versiones       | Git + GitHub (repositorio privado, plan gratuito)                                                | Disponible    |
    | SOFTWARE | Sistema operativo          | Windows 11 Pro (64 bits)                                                                         | Disponible    |
    | SOFTWARE | IDE / Editor               | Visual Studio Code, SQL Server Management Studio (SSMS)                                          | Disponible    |

    **Justificación tecnológica:** SQL Server se selecciona por su soporte nativo y maduro de `BACKUP/RESTORE` y herramientas de verificación como `DBCC CHECKDB`. Python se elige por su capacidad de orquestación, automatización y ecosistema. `customtkinter` permite una interfaz moderna tipo “aplicación empresarial”. `pyodbc` provee conectividad robusta a SQL Server a través de drivers ODBC estándar.

<div style="page-break-after: always; visibility: hidden"></div>

4. <span id="_Toc52661349" class="anchor"></span>**Estudio de Factibilidad**

    El presente estudio de factibilidad fue preparado por los integrantes del equipo de desarrollo durante las primeras semanas del ciclo académico 2026-I, bajo la supervisión del Ing. Patrick José Cuadros Quiroga. Su propósito es determinar si el proyecto cuenta con los recursos técnicos, económicos, operativos, legales, sociales y ambientales necesarios para ser ejecutado exitosamente.

    4.1. <span id="_Toc52661350" class="anchor"></span>Factibilidad Técnica

    El proyecto es técnicamente viable porque los recursos requeridos se encuentran disponibles y/o son de acceso libre para el equipo de desarrollo:

    - **Hardware:** Los integrantes cuentan con equipos con especificaciones suficientes para ejecutar SQL Server 2022 Developer Edition, herramientas de desarrollo y la aplicación cliente.
    - **Software de base de datos:** SQL Server 2022 Developer Edition incluye las operaciones necesarias (`BACKUP DATABASE`, `RESTORE DATABASE`, `DBCC CHECKDB`), así como soporte de seguridad mediante roles.
    - **Lenguaje de programación:** Python 3.12+ y librerías como `pyodbc` (conectividad), `logging` (auditoría técnica), `hashlib` (huellas/hash de evidencia cuando aplique) y `customtkinter` (GUI) cubren los requisitos del proyecto.
    - **Control de versiones y colaboración:** GitHub facilita trabajo colaborativo, control de cambios y CI con GitHub Actions.
    - **Arquitectura:** La aplicación se desarrollará bajo Clean Architecture, permitiendo desacoplar la lógica del negocio de la interfaz y de la capa de infraestructura (T-SQL), elevando mantenibilidad y testabilidad.

    La arquitectura seguirá un modelo cliente-servidor: la aplicación Python se conectará por red (localhost o instancia remota) a SQL Server vía `pyodbc`. Los archivos de backup se almacenarán en rutas definidas y se restaurarán en una BD sandbox con archivos físicos ubicados en directorios configurables.

    4.2. <span id="_Toc52661351" class="anchor"></span>Factibilidad Económica

    El estudio de viabilidad económica compara los costos del proyecto contra los beneficios esperados. El proyecto utiliza herramientas gratuitas (SQL Server Developer, Python, VS Code, GitHub Free), concentrando el costo principalmente en recurso humano y en un dispositivo de almacenamiento para redundancia.

        4.2.1. Costos Generales

    Los costos generales comprenden gastos en equipos, accesorios y materiales necesarios para el desarrollo del proyecto.

    | Ítem                 | Descripción                                   | Cantidad | Costo Unitario (S/) | Total (S/)    |
    |----------------------|-----------------------------------------------|:--------:|:-------------------:|:-------------:|
    | Laptop de desarrollo | Intel Core i5 / 8 GB RAM (recurso propio)     |    2     |        0.00         |      0.00     |
    | Disco duro externo   | 1 TB — redundancia de backups                 |    1     |      250.00         |    250.00     |
    | Útiles de oficina    | Papelería, carpetas, cuadernos de notas       |    —     |       50.00         |     50.00     |
    | **TOTAL**            |                                               |          |                     | **S/ 300.00** |

        4.2.2. Costos operativos durante el desarrollo

    Costos necesarios para la operatividad de las actividades del equipo durante el período de ejecución del proyecto.

    | Servicio                             | Costo Mensual (S/) | Meses | Total (S/)    |
    |--------------------------------------|:------------------:|:-----:|:-------------:|
    | Energía eléctrica                    |       40.00        |   4   |    160.00     |
    | Internet (fibra óptica)              |      100.00        |   4   |    400.00     |
    | Espacio de trabajo (remoto / propio) |        0.00        |   4   |      0.00     |
    | **TOTAL**                            |                    |       | **S/ 560.00** |

        4.2.3. Costos del ambiente

    Evaluación de los costos asociados a infraestructura tecnológica y licenciamiento requeridos.

    | Concepto                  | Descripción                                             | Costo (S/)  |
    |---------------------------|---------------------------------------------------------|:-----------:|
    | Licencia SQL Server       | Developer Edition — uso libre para desarrollo y pruebas |     0.00    |
    | Repositorio GitHub        | Plan Free — repositorios privados                       |     0.00    |
    | Python y librerías        | Software libre (`pyodbc`, `customtkinter`, etc.)         |     0.00    |
    | Visual Studio Code / SSMS | Herramientas gratuitas de desarrollo                    |     0.00    |
    | **TOTAL**                 |                                                         | **S/ 0.00** |

        4.2.4. Costos de personal

    El equipo de desarrollo está conformado por dos integrantes. Los montos reflejan una remuneración simulada equivalente a practicante/junior en el mercado laboral peruano (2026). El horario de trabajo es de lunes a viernes, de 9:00 a.m. a 1:00 p.m. (4 horas diarias).

    | Rol                                  | Cantidad | Pago Mensual (S/) | Meses | Total (S/)       |
    |--------------------------------------|:--------:|:-----------------:|:-----:|:----------------:|
    | Desarrollador Backend / DBA / DevOps |    1     |     1,300.00      |   4   |    5,200.00      |
    | Desarrollador Frontend / QA          |    1     |     1,200.00      |   4   |    4,800.00      |
    | **TOTAL**                            |          |                   |       | **S/ 10,000.00** |

        4.2.5. Costos totales del desarrollo del sistema

    Resumen de todos los costos del proyecto.

    | Categoría          | Monto (S/)       |
    |--------------------|:----------------:|
    | Costos Generales   |       300.00     |
    | Costos Operativos  |       560.00     |
    | Costos de Ambiente |         0.00     |
    | Costos de Personal |    10,000.00     |
    | **TOTAL GENERAL**  | **S/ 10,860.00** |

    4.3. <span id="_Toc52661352" class="anchor"></span>Factibilidad Operativa

    El sistema propuesto es operativamente viable dado que responde a necesidades concretas y ofrece un procedimiento estandarizado de continuidad de datos:

    - **Automatización del ciclo completo:** Ejecuta backup, restore test, validación y limpieza, eliminando operaciones manuales repetitivas.
    - **Interfaz gráfica profesional:** Permite que un DBA gestione el ciclo desde una GUI intuitiva (consola de eventos, progreso en tiempo real).
    - **Reducción de errores:** Minimiza fallas por comandos T-SQL manuales al encapsular y validar parámetros (rutas, nombres, BD objetivo).
    - **Evidencias y trazabilidad:** Genera logs detallados por ejecución y métricas (duración, tamaño, resultado), facilitando auditorías y revisiones.
    - **Estandarización:** Nomenclatura uniforme de respaldos y políticas de almacenamiento/retención configurables.
    - **Limpieza automática:** Elimina la BD sandbox al finalizar, evitando consumo de recursos permanente.

    **Lista de interesados:** Administradores de base de datos (DBA), equipo de TI, área de auditoría interna, usuarios finales del sistema de información respaldado, y docentes del curso como evaluadores académicos.

    4.4. <span id="_Toc52661353" class="anchor"></span>Factibilidad Legal

    - **Protección de datos personales:** El sistema se alinea con la Ley N.° 29733 (Perú) asegurando que respaldos con datos personales se traten con confidencialidad y accesos restringidos.
    - **Licenciamiento:** Python, bibliotecas y herramientas utilizadas cuentan con licencias permisivas o de uso libre en entornos académicos. SQL Server Developer Edition es gratuito para desarrollo y pruebas (no producción).
    - **Propiedad intelectual:** El código fuente será de autoría de los integrantes. Se propone licenciarlo bajo **MIT License** para fines académicos, manteniendo atribución.
    - **Buenas prácticas de seguridad:** El enfoque de auditoría y control de accesos se alinea con recomendaciones generales de ISO/IEC 27001 (gestión de seguridad), facilitando cumplimiento organizacional.

    4.5. <span id="_Toc52661354" class="anchor"></span>Factibilidad Social

    - **Impacto en usuarios técnicos:** Reduce carga operativa y estrés del DBA, y aumenta la confianza al tener evidencia de restauración válida.
    - **Aceptación:** Al abordar continuidad de datos (necesidad crítica), se espera alta aceptación en equipos TI.
    - **Aprendizaje colaborativo:** Fortalece competencias de ingeniería de software, seguridad, administración SQL Server y pruebas.
    - **Contribución académica:** Puede servir como caso de estudio en cursos de BD, seguridad y continuidad operativa.

    4.6. <span id="_Toc52661355" class="anchor"></span>Factibilidad Ambiental

    - **Consumo de energía:** Impacto mínimo, restringido al uso de laptops y entorno de pruebas durante el desarrollo.
    - **Residuos electrónicos:** Proyecto basado en software, no genera RAEE adicional.
    - **Gestión digital:** Se prioriza documentación digital y repositorio GitHub, minimizando uso de papel.

<div style="page-break-after: always; visibility: hidden"></div>

5. <span id="_Toc52661356" class="anchor"></span>**Análisis Financiero**

    El análisis financiero evalúa beneficios cuantificables y costos desde una perspectiva temporal, determinando si la inversión genera valor neto positivo. El horizonte de evaluación es de un (1) año.

    5.1. Justificación de la Inversión

        5.1.1. Beneficios del Proyecto

    A continuación se describen beneficios tangibles e intangibles del sistema:

    | Beneficios Tangibles                                                                                 | Beneficios Intangibles                                                                 |
    |------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
    | Reducción del tiempo de gestión de backups (manual → automatizado)                                   | Mayor confianza institucional en la integridad y recuperabilidad de datos               |
    | Eliminación de errores por ejecución manual de T-SQL                                                 | Mejora de imagen ante auditorías internas/externas                                      |
    | Ahorro de horas-hombre (planificación, ejecución, verificación y documentación)                      | Fortalecimiento de cultura de seguridad y continuidad                                  |
    | Disminución del riesgo de restauraciones fallidas en incidentes (al contar con restore test validado)| Toma de decisiones mejorada por evidencias y métricas históricas                       |
    | Disponibilidad de trazabilidad completa mediante logs                                                 | Mejor gobernanza de TI (procedimientos repetibles y verificables)                       |

    **Estimación del beneficio anual:** Considerando un ahorro aproximado de 2 horas-hombre por semana (costo referencial S/ 25.00/hora), el ahorro operativo anual sería S/ 2,600.00. Adicionalmente, la validación de restauración y consistencia reduce el riesgo de pérdida de datos. Si se asume un costo conservador de S/ 10,000.00 por incidente y una probabilidad anual del 50 % sin controles robustos, el beneficio esperado por mitigación de riesgo es S/ 5,000.00. Sumando eficiencia y reducción de riesgo (S/ 7,600.00) más el valor generado por estandarización y evidencia (S/ 9,800.00), el **beneficio total anual estimado asciende a S/ 17,400.00**.

        5.1.2. Criterios de Inversión

    | Indicador                 | Año 0 (Inversión) | Año 1 (Beneficio) | Resultado                   |
    |---------------------------|:-----------------:|:-----------------:|-----------------------------|
    | Inversión total           |  S/ -10,860.00    |        —          | Costo del proyecto          |
    | Beneficio anual estimado  |        —          |  S/ 17,400.00     | Ahorro + valor generado     |
    | VAN (tasa 10 %)           |        —          |  S/ 4,958.18      | Positivo — **Aceptar**      |
    | B/C                       |        —          |       1.60        | > 1 — **Aceptar**           |
    | TIR                       |        —          |      60.2 %       | > COK (10 %) — **Aceptar**  |

            5.1.2.1. Relación Beneficio/Costo (B/C)

    **B/C = Beneficio Anual / Costo Total = S/ 17,400.00 / S/ 10,860.00 = 1.60**

    El B/C es mayor que 1, lo que indica que por cada sol invertido se obtienen S/ 1.60 en beneficios. Por lo tanto, el proyecto se **ACEPTA** bajo este criterio.

            5.1.2.2. Valor Actual Neto (VAN)

    Se utiliza una tasa de descuento (COK) del 10 %.

    **VAN = -S/ 10,860.00 + (S/ 17,400.00 / 1.10) = S/ 4,958.18**

    El VAN es mayor que cero, confirmando que el proyecto genera valor neto por encima del costo de oportunidad del capital. Por lo tanto, el proyecto se **ACEPTA** bajo este criterio.

            5.1.2.3. Tasa Interna de Retorno (TIR)

    Aplicando la condición VAN = 0:

    **0 = -S/ 10,860.00 + (S/ 17,400.00 / (1 + TIR)) → TIR = 60.2 %**

    La TIR (60.2 %) es mayor que el COK (10 %), por lo que el proyecto es rentable. Por lo tanto, el proyecto se **ACEPTA** bajo este criterio.

<div style="page-break-after: always; visibility: hidden"></div>

6. <span id="_Toc52661357" class="anchor"></span>**Conclusiones**

Del análisis integral de factibilidad realizado se desprenden las siguientes conclusiones:

- **Factibilidad Técnica — VIABLE:** Se dispone de tecnologías y recursos adecuados: SQL Server 2022 Developer, Python 3.12+, conectividad vía `pyodbc` y una GUI moderna con `customtkinter`. El uso de Clean Architecture mejora mantenibilidad y escalabilidad.

- **Factibilidad Económica — VIABLE:** El costo total estimado del proyecto asciende a S/ 10,860.00, concentrado principalmente en recurso humano. Las herramientas base son gratuitas, reduciendo inversión en licencias.

- **Factibilidad Operativa — VIABLE:** SQL-SafeBridge automatiza el ciclo crítico de continuidad (backup + restore test + validación + evidencia + limpieza), disminuyendo errores manuales y aportando estandarización y trazabilidad.

- **Factibilidad Legal — VIABLE:** El proyecto se alinea con la Ley N.° 29733 de Protección de Datos Personales y utiliza software con licencias compatibles con el uso académico. Se propone licenciamiento MIT para el código del proyecto.

- **Factibilidad Social y Ambiental — VIABLE:** El impacto social es positivo (reducción de carga operativa, aprendizaje colaborativo) y el impacto ambiental es mínimo al tratarse de un proyecto de software con gestión digital.

- **Análisis Financiero — RENTABLE:** Los criterios de inversión son favorables: B/C = 1.60 (> 1), VAN = S/ 4,958.18 (> 0) y TIR = 60.2 % (> COK del 10 %). En conjunto, estos indicadores sustentan la aprobación del proyecto.

En conclusión, el proyecto **"SQL-SafeBridge: Orquestador de Respaldos y Validación de Integridad (SQL Server)"** es técnicamente factible, económicamente rentable y operativamente útil. Se recomienda su aprobación e inicio inmediato para garantizar la entrega en los plazos académicos establecidos.

````