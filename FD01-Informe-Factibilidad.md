<center>

[comment]: <img src="./media/media/image1.png" style="width:1.088in;height:1.46256in" alt="escudo.png" />

![./media/media/image1.png](./media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERIA**

**Escuela Profesional de Ingeniería de Sistemas**

**Proyecto *Generador de Backup y Prueba de Restauración***

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

Sistema *Generador de Backup y Prueba de Restauración*

Informe de Factibilidad

Versión *1.0*

|CONTROL DE VERSIONES||||||
| :-: | :- | :- | :- | :- | :- |
|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo|
|1\.0|IASR / JSCM|Ing. P. Cuadros|Ing. P. Cuadros|27/03/2026|Versión Original|

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

    Generador de Backup y Prueba de Restauración.

    1.2. Duración del proyecto

    Cuatro (4) meses, equivalentes a un ciclo académico universitario (marzo – julio 2026). El análisis de factibilidad económica se proyecta a un horizonte de un (1) año con el fin de evaluar el retorno de la inversión.

    1.3. Descripción

    En la actualidad, la pérdida de datos representa uno de los principales riesgos operativos para cualquier organización que dependa de sistemas de información. Estudios del sector indican que más del 60 % de los incidentes críticos de pérdida de datos se producen por fallas en procesos manuales o ausencia de una estrategia de respaldo formal. Ante esta problemática, el presente proyecto propone desarrollar una solución de ingeniería de software que automatice íntegramente el ciclo de vida de las copias de seguridad en un motor de base de datos SQL Server.

    El sistema no se limita a la ejecución de comandos T-SQL de forma aislada; integra una arquitectura completa compuesta por tres capas: (i) el motor de base de datos, que ejecuta las operaciones nativas de backup y restauración; (ii) una capa de aplicación desarrollada en Python que actúa como interfaz de gestión para el usuario; y (iii) una capa transversal de seguridad y auditoría que registra cada operación, controla el acceso mediante roles DBA y garantiza la trazabilidad del sistema. La solución será validada en un entorno controlado que simula escenarios reales de falla y recuperación.

    1.4. Objetivos

       1.4.1 Objetivo general

    Desarrollar una solución de software que optimice y automatice la gestión de copias de seguridad de una base de datos SQL Server, permitiendo identificar, capturar y validar la integridad de los respaldos en un entorno controlado, con trazabilidad completa mediante auditoría de operaciones.

        1.4.2 Objetivos Específicos

    - Diseñar una arquitectura de software multicapa (BD – Aplicación – Seguridad) que soporte las operaciones de backup y restauración.
    - Implementar scripts de automatización en Python para la generación programada de backups (full, diferencial e incremental) en SQL Server.
    - Desarrollar un módulo de validación de integridad que verifique la restauración exitosa de cada backup generado mediante checksums SHA-256.
    - Implementar una capa de seguridad basada en roles DBA que controle el acceso a las funciones críticas del sistema.
    - Configurar un sistema de auditoría que registre automáticamente el historial de operaciones (quién, cuándo y qué acción realizó).
    - Desarrollar una interfaz gráfica amigable (GUI) en Python que permita gestionar el ciclo de vida de los backups sin conocimientos avanzados de SQL.

<div style="page-break-after: always; visibility: hidden"></div>

2. <span id="_Toc52661347" class="anchor"></span>**Riesgos**

    A continuación se identifican los principales riesgos que podrían afectar el éxito del proyecto, clasificados por categoría, junto con su probabilidad estimada y la estrategia de mitigación correspondiente.

    | Categoría      | Riesgo                                                            | Probabilidad | Estrategia de Mitigación                                                                          |
    |----------------|-------------------------------------------------------------------|:------------:|---------------------------------------------------------------------------------------------------|
    | Técnico        | Corrupción de archivos de backup                                  | Media        | Implementar validación de integridad mediante checksums (SHA-256) tras cada generación de backup. |
    | Técnico        | Versiones incompatibles entre SQL Server y scripts Python         | Media        | Definir y documentar versiones específicas desde el inicio; usar entornos virtuales (venv).       |
    | Técnico        | Caída del servidor durante la generación del backup               | Baja         | Configurar mecanismos de reintento automático y notificación al administrador.                    |
    | Almacenamiento | Falta de espacio en disco para almacenar backups                  | Media        | Implementar políticas de retención automática y alertas de umbral de almacenamiento.              |
    | Seguridad      | Acceso no autorizado a los archivos de backup                     | Media        | Aplicar cifrado AES-256 en los archivos generados y control de roles DBA.                         |
    | Operativo      | Errores en los scripts de automatización                          | Media        | Realizar pruebas unitarias e integración continua con GitHub Actions.                             |
    | Humano         | Abandono del proyecto por parte de un integrante                  | Baja         | Documentar todo el código y mantener repositorio actualizado para continuidad.                    |
    | Operativo      | Pérdida de los registros de auditoría                             | Baja         | Almacenar logs en una tabla dedicada con escritura protegida y respaldo separado.                 |

<div style="page-break-after: always; visibility: hidden"></div>

3. <span id="_Toc52661348" class="anchor"></span>**Análisis de la Situación actual**

    3.1. Planteamiento del problema

    Las organizaciones modernas, tanto empresas privadas como instituciones académicas, generan volúmenes crecientes de datos que constituyen activos críticos. Sin embargo, en muchos entornos —especialmente medianas empresas y entidades educativas— la gestión de copias de seguridad sigue realizándose de forma manual: el administrador de base de datos (DBA) ejecuta comandos T-SQL directamente en la consola, sin un calendario definido, sin verificación de integridad y sin registro auditable de cada operación.

    Esta situación genera tres problemas centrales: (1) alta exposición al error humano en la escritura de comandos, (2) ausencia de evidencia de que los backups son realmente restaurables, y (3) falta de trazabilidad ante auditorías de seguridad o incidentes de pérdida de datos. El presente proyecto busca resolver esta brecha mediante la automatización del proceso completo, desde la generación hasta la verificación del respaldo.

    3.2. Consideraciones de hardware y software

    El siguiente cuadro resume los recursos tecnológicos evaluados para el desarrollo e implantación del sistema:

    | Tipo     | Componente                 | Especificaciones                                                                         | Estado        |
    |----------|----------------------------|------------------------------------------------------------------------------------------|---------------|
    | HARDWARE | Servidor de BD             | Procesador Intel Core i5 / Ryzen 5 (5.ª gen. o sup.), 8 GB RAM mínimo, 500 GB SSD       | Disponible    |
    | HARDWARE | Almacenamiento de respaldo | Disco duro externo 1 TB para redundancia de backups                                      | Por adquirir  |
    | HARDWARE | Equipos de desarrollo      | Laptop/PC serie 5 o superior, 8 GB RAM mínimo, SSD                                      | Disponible    |
    | SOFTWARE | Motor de base de datos     | SQL Server 2022 Developer Edition (licencia gratuita para desarrollo)                    | Disponible    |
    | SOFTWARE | Lenguaje de programación   | Python 3.11+ con librerías pyodbc, schedule, tkinter / PyQt5                             | Disponible    |
    | SOFTWARE | Control de versiones       | Git + GitHub (repositorio privado, plan gratuito)                                        | Disponible    |
    | SOFTWARE | Sistema operativo          | Windows 11 Pro (64 bits)                                                                 | Disponible    |
    | SOFTWARE | IDE / Editor               | Visual Studio Code, SQL Server Management Studio (SSMS)                                  | Disponible    |

    **Justificación tecnológica:** SQL Server fue seleccionado por su integración nativa con instrucciones T-SQL de backup/restore, su compatibilidad con entornos Windows y su licencia Developer Edition gratuita para uso académico. Python fue elegido por su amplia disponibilidad de librerías de automatización (pyodbc, schedule) y su capacidad para construir interfaces gráficas multiplataforma con tkinter o PyQt5. GitHub facilita el trabajo colaborativo y el control de versiones del código fuente.

<div style="page-break-after: always; visibility: hidden"></div>

4. <span id="_Toc52661349" class="anchor"></span>**Estudio de Factibilidad**

    El presente estudio de factibilidad fue preparado por los integrantes del equipo de desarrollo durante las primeras semanas del ciclo académico 2026-I, bajo la supervisión del Ing. Patrick José Cuadros Quiroga. Su propósito es determinar si el proyecto cuenta con los recursos técnicos, económicos, operativos, legales, sociales y ambientales necesarios para ser ejecutado exitosamente. El resultado esperado es la aprobación del proyecto como viable en todas las dimensiones evaluadas.

    4.1. <span id="_Toc52661350" class="anchor"></span>Factibilidad Técnica

    El proyecto es técnicamente viable porque todos los recursos tecnológicos requeridos se encuentran disponibles y son de acceso libre o de uso propio del equipo:

    - **Hardware:** Los integrantes cuentan con laptops con procesadores Intel Core i5 de quinta generación, 8 GB de RAM y almacenamiento SSD, que superan los requisitos mínimos para ejecutar SQL Server 2022 Developer Edition y Python 3.11.
    - **Software de base de datos:** SQL Server 2022 Developer Edition provee todas las funcionalidades necesarias (BACKUP, RESTORE, CHECKSUM, roles de seguridad, auditoría con DDL Triggers y Server Audit) sin costo alguno.
    - **Lenguaje de programación:** Python 3.11 con las librerías pyodbc (conexión a SQL Server), schedule (automatización de tareas), hashlib (validación SHA-256) y PyQt5/tkinter (GUI) cubre todos los requerimientos funcionales del proyecto.
    - **Control de versiones y colaboración:** GitHub con plan gratuito permite trabajo colaborativo, integración continua y respaldo del código fuente en la nube.
    - **Infraestructura de red:** El proyecto opera en red local (localhost) durante el desarrollo, por lo que no requiere servidor dedicado, dominio ni infraestructura de red adicional.

    La arquitectura del sistema sigue un modelo cliente-servidor simplificado: la aplicación Python (cliente) se comunica con la instancia local de SQL Server (servidor) a través de la librería pyodbc mediante conexión TCP/IP. Los archivos de backup se almacenan en una ruta local y en el disco externo de respaldo.

    4.2. <span id="_Toc52661351" class="anchor"></span>Factibilidad Económica

    El propósito del estudio de viabilidad económica es determinar los beneficios económicos del proyecto propuesto para la organización, en contraposición con los costos. El equipo cuenta con las herramientas necesarias para la implantación del sistema y las herramientas de software son en su totalidad de uso libre y gratuito, por lo que la inversión inicial en infraestructura informática es mínima.

        4.2.1. Costos Generales

    Los costos generales comprenden los gastos en equipos, accesorios y materiales de uso diario necesarios para el desarrollo del proyecto.

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

    Evaluación de los costos asociados a la infraestructura tecnológica y licenciamiento de software requeridos para el desarrollo e implantación del sistema.

    | Concepto                  | Descripción                                             | Costo (S/)  |
    |---------------------------|---------------------------------------------------------|:-----------:|
    | Licencia SQL Server       | Developer Edition — uso libre para desarrollo y pruebas |     0.00    |
    | Repositorio GitHub        | Plan Free — repositorios privados ilimitados            |     0.00    |
    | Python y librerías        | Software libre (pyodbc, schedule, tkinter/PyQt5)        |     0.00    |
    | Visual Studio Code / SSMS | Herramientas gratuitas de desarrollo                    |     0.00    |
    | **TOTAL**                 |                                                         | **S/ 0.00** |

        4.2.4. Costos de personal

    El equipo de desarrollo está conformado por dos integrantes con roles diferenciados. Los montos reflejan una remuneración simulada equivalente a la de un practicante/junior en el mercado laboral peruano (2026). El horario de trabajo es de lunes a viernes, de 9:00 a.m. a 1:00 p.m. (4 horas diarias).

    | Rol                         | Cantidad | Pago Mensual (S/) | Meses | Total (S/)       |
    |-----------------------------|:--------:|:-----------------:|:-----:|:----------------:|
    | Desarrollador Backend / DBA |    1     |     1,300.00      |   4   |    5,200.00      |
    | Desarrollador Frontend / QA |    1     |     1,200.00      |   4   |    4,800.00      |
    | **TOTAL**                   |          |                   |       | **S/ 10,000.00** |

        4.2.5. Costos totales del desarrollo del sistema

    Resumen de todos los costos del proyecto. La forma de pago del personal es mensual durante los cuatro meses de desarrollo.

    | Categoría          | Monto (S/)       |
    |--------------------|:----------------:|
    | Costos Generales   |       300.00     |
    | Costos Operativos  |       560.00     |
    | Costos de Ambiente |         0.00     |
    | Costos de Personal |    10,000.00     |
    | **TOTAL GENERAL**  | **S/ 10,860.00** |

    4.3. <span id="_Toc52661352" class="anchor"></span>Factibilidad Operativa

    El sistema propuesto es operativamente viable dado que resuelve necesidades concretas de los usuarios finales y cuenta con los medios para ser sostenido en el tiempo:

    - **Automatización de backups:** Elimina la necesidad de ejecutar comandos SQL manualmente, reduciendo el tiempo de administración en aproximadamente un 80 % y disminuyendo los errores operativos.
    - **Interfaz gráfica amigable:** El usuario DBA podrá gestionar el ciclo completo de backups desde una GUI intuitiva, sin requerir conocimiento avanzado de T-SQL, lo que amplía el perfil de usuarios que pueden operar el sistema.
    - **Reducción de errores:** El sistema valida automáticamente la integridad de cada backup generado mediante checksum SHA-256, garantizando que el archivo sea restaurable antes de marcarlo como exitoso.
    - **Estandarización de políticas de recuperación:** Los backups siguen una nomenclatura uniforme (`bd_nombre_YYYYMMDD_HHMMSS.bak`) y son almacenados en rutas predefinidas, facilitando la localización y restauración por cualquier miembro autorizado del equipo técnico.
    - **Fortalecimiento de la seguridad y auditoría:** Se implementará segregación de funciones mediante roles DBA; únicamente usuarios con permisos explícitos podrán ejecutar operaciones críticas. Cada acción quedará registrada en un log automático con usuario, fecha, hora y tipo de operación.
    - **Lista de interesados:** Administradores de base de datos (DBA), equipo de TI, área de auditoría interna, usuarios finales del sistema de información respaldado, y docentes del curso de Base de Datos II como evaluadores académicos.

    4.4. <span id="_Toc52661353" class="anchor"></span>Factibilidad Legal

    - **Protección de datos personales:** El sistema cumple con los principios establecidos en la Ley N.° 29733 — Ley de Protección de Datos Personales del Perú — garantizando que los backups que contengan datos personales sean tratados con confidencialidad, almacenados de forma segura y accesibles únicamente por personal autorizado.
    - **Propiedad intelectual del código fuente:** El código desarrollado en el presente proyecto es de autoría exclusiva de los integrantes del equipo. Cualquier uso por parte de terceros requerirá el consentimiento expreso de ambos autores. Se licenciará bajo MIT License para uso académico.
    - **Software libre:** Todas las herramientas utilizadas (Python, SQL Server Developer Edition, GitHub, VS Code) cuentan con licencias que permiten su uso libre en entornos académicos y de desarrollo, sin incurrir en infracción de derechos de autor.
    - **Regulación de auditoría:** El sistema implementa políticas de auditoría alineadas con las buenas prácticas de la norma ISO/IEC 27001 (gestión de seguridad de la información), lo que facilita el cumplimiento ante auditorías institucionales.

    4.5. <span id="_Toc52661354" class="anchor"></span>Factibilidad Social

    - **Impacto en los usuarios:** El proyecto tendrá un impacto positivo en los administradores de base de datos al automatizar tareas repetitivas, reducir la carga operativa y disminuir el estrés asociado a la gestión manual de respaldos en entornos de producción.
    - **Aceptación del proyecto:** Al tratarse de una herramienta que garantiza la continuidad operativa y la seguridad de los datos, su adopción por parte del equipo técnico será alta. La interfaz amigable reduce la curva de aprendizaje y favorece una transición fluida.
    - **Aprendizaje colaborativo:** El proyecto fomenta el trabajo en equipo entre los dos integrantes, promoviendo la comunicación constante, la distribución equitativa de responsabilidades y la adquisición de competencias en ingeniería de software, administración de bases de datos y seguridad informática.
    - **Contribución académica:** El sistema podrá ser utilizado como caso de estudio o material didáctico en cursos de Base de Datos, Seguridad Informática y Gestión de TI de la Universidad Privada de Tacna.

    4.6. <span id="_Toc52661355" class="anchor"></span>Factibilidad Ambiental

    - **Consumo de energía:** El impacto energético es mínimo, limitado al uso de las laptops de los integrantes (aproximadamente 65 W cada una) y la conexión a internet durante el período de desarrollo de cuatro meses.
    - **Residuos electrónicos:** El proyecto está enfocado íntegramente en software; no implica la adquisición ni el descarte de componentes electrónicos, por lo que no genera residuos de aparatos eléctricos y electrónicos (RAEE).
    - **Impacto ambiental directo:** No se utilizan recursos naturales físicos en el desarrollo del sistema. El proyecto no genera emisiones, vertimientos ni residuos sólidos de impacto ambiental significativo.
    - **Gestión documental digital:** Se priorizó el uso de documentación digital y almacenamiento en la nube (GitHub, Google Drive) para minimizar el consumo de papel. El uso de impresión quedará restringido a la entrega física final del informe académico.

<div style="page-break-after: always; visibility: hidden"></div>

5. <span id="_Toc52661356" class="anchor"></span>**Análisis Financiero**

    El plan financiero evalúa los beneficios cuantificables y los costos del proyecto desde una perspectiva temporal, con el objetivo de determinar si la inversión genera valor neto positivo. Su misión fundamental es detectar situaciones financieramente inadecuadas. El horizonte de evaluación es de un (1) año, tomando como referencia el costo total de desarrollo y los beneficios proyectados para el primer año de operación.

    5.1. Justificación de la Inversión

        5.1.1. Beneficios del Proyecto

    El beneficio se calcula como el margen económico menos los costes de oportunidad, que son los márgenes que hubieran podido obtenerse de haber dedicado el capital y el esfuerzo a otras actividades. A continuación se describen los beneficios tangibles e intangibles del sistema:

    | Beneficios Tangibles                                                                  | Beneficios Intangibles                                                                  |
    |---------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
    | Reducción del tiempo de gestión de backups en aprox. 80 % (de manual a automatizado)  | Mayor confianza de la organización en la integridad de sus datos                        |
    | Eliminación de errores por comandos SQL mal escritos                                  | Mejora de la imagen institucional ante auditorías internas y externas                   |
    | Ahorro estimado de 2 horas-hombre por semana en tareas de administración              | Fortalecimiento de la cultura de seguridad y buenas prácticas en el equipo TI           |
    | Reducción de costos por recuperación ante incidentes de pérdida de datos              | Cumplimiento proactivo de normativas de protección de datos (Ley N.° 29733)             |
    | Disponibilidad de trazabilidad completa mediante logs de auditoría                    | Mejora en la toma de decisiones gracias a reportes de estado de backups en tiempo real  |

    **Estimación del beneficio anual:** Considerando que el sistema ahorra aproximadamente 2 horas-hombre por semana (a un costo referencial de S/ 25.00/hora), el ahorro operativo anual asciende a S/ 2,600.00. Adicionalmente, la automatización y validación de backups reduce el riesgo de pérdida de datos, cuyo costo de recuperación en un incidente típico puede oscilar entre S/ 5,000.00 y S/ 15,000.00. Tomando un valor conservador de S/ 10,000.00 de riesgo mitigado con una probabilidad del 50 % de ocurrencia anual sin el sistema, el beneficio esperado por mitigación de riesgo asciende a S/ 5,000.00. Sumando el valor de eficiencia y estándar de calidad (S/ 9,800.00), el **beneficio total anual estimado asciende a S/ 17,400.00**.

        5.1.2. Criterios de Inversión

    | Indicador                 | Año 0 (Inversión) | Año 1 (Beneficio) | Resultado                   |
    |---------------------------|:-----------------:|:-----------------:|-----------------------------|
    | Inversión total           |  S/ -10,860.00    |        —          | Costo del proyecto          |
    | Beneficio anual estimado  |        —          |  S/ 17,400.00     | Ahorro + valor generado     |
    | VAN (tasa 10 %)           |        —          |  S/ 4,958.18      | Positivo — **Aceptar**      |
    | B/C                       |        —          |       1.60        | > 1 — **Aceptar**           |
    | TIR                       |        —          |      60.2 %       | > COK (10 %) — **Aceptar**  |

            5.1.2.1. Relación Beneficio/Costo (B/C)

    En base a los costos y beneficios identificados se evalúa si es factible el desarrollo del proyecto. Si se presentan varias alternativas de solución se evaluará cada una de ellas para determinar la mejor solución desde el punto de vista del retorno de la inversión.

    **B/C = Beneficio Anual / Costo Total = S/ 17,400.00 / S/ 10,860.00 = 1.60**

    El B/C es mayor que 1, lo que indica que por cada sol invertido en el proyecto se obtienen S/ 1.60 en beneficios. Por lo tanto, el proyecto se **ACEPTA** bajo este criterio.

            5.1.2.2. Valor Actual Neto (VAN)

    Valor actual de los beneficios netos que genera el proyecto. Se utiliza una tasa de descuento (COK) del 10 %, equivalente a la tasa de referencia del mercado financiero peruano para inversiones de bajo riesgo.

    **VAN = -S/ 10,860.00 + (S/ 17,400.00 / 1.10) = S/ 4,958.18**

    El VAN es mayor que cero, lo que confirma que el proyecto genera valor neto por encima del costo de oportunidad del capital. Por lo tanto, el proyecto se **ACEPTA** bajo este criterio.

            5.1.2.3. Tasa Interna de Retorno (TIR)

    Es la tasa porcentual que indica la rentabilidad promedio anual que genera el capital invertido en el proyecto. El costo de oportunidad de capital (COK) es la tasa de interés que podría haberse obtenido con el dinero invertido en el proyecto. Aplicando la condición VAN = 0:

    **0 = -S/ 10,860.00 + (S/ 17,400.00 / (1 + TIR)) → TIR = 60.2 %**

    La TIR (60.2 %) es significativamente mayor que el COK (10 %), lo que demuestra que el proyecto es altamente rentable en su primer año de operación. Por lo tanto, el proyecto se **ACEPTA** bajo este criterio.

<div style="page-break-after: always; visibility: hidden"></div>

6. <span id="_Toc52661357" class="anchor"></span>**Conclusiones**

Del análisis integral de factibilidad realizado se desprenden las siguientes conclusiones:

- **Factibilidad Técnica — VIABLE:** El equipo cuenta con todos los recursos de hardware y software necesarios para el desarrollo e implantación del sistema. Las tecnologías seleccionadas (SQL Server 2022 Developer, Python 3.11, GitHub) son maduras, ampliamente documentadas y de uso libre, lo que elimina barreras técnicas para la ejecución del proyecto.

- **Factibilidad Económica — VIABLE:** El costo total del proyecto asciende a S/ 10,860.00. Dado que gran parte de los recursos son propios y las herramientas de software son gratuitas, la inversión real se concentra en el costo del recurso humano. El análisis confirma que el gasto es justificado y sostenible dentro del presupuesto académico.

- **Factibilidad Operativa — VIABLE:** El sistema aporta beneficios tangibles inmediatos (reducción de tiempo, eliminación de errores) y beneficios estratégicos (auditoría, seguridad, trazabilidad) que mejoran significativamente la gestión de bases de datos respecto al proceso manual actual.

- **Factibilidad Legal — VIABLE:** El proyecto cumple con la Ley N.° 29733 de Protección de Datos Personales del Perú y hace uso exclusivo de software con licencias compatibles con el uso académico y de desarrollo.

- **Factibilidad Social y Ambiental — VIABLE:** El impacto social es positivo (reducción de carga operativa, aprendizaje colaborativo) y el impacto ambiental es prácticamente nulo al tratarse de un proyecto íntegramente de software.

- **Análisis Financiero — RENTABLE:** Los tres criterios de inversión confirman la viabilidad financiera: B/C = 1.60 (> 1), VAN = S/ 4,958.18 (> 0) y TIR = 60.2 % (> COK del 10 %). En conjunto, estos indicadores demuestran que el proyecto generará un retorno significativo sobre la inversión en su primer año de operación.

En conclusión, el proyecto **"Generador de Backup y Prueba de Restauración"** es técnicamente factible, económicamente rentable y operativamente útil. Se recomienda su aprobación e inicio inmediato para garantizar la entrega en los plazos académicos establecidos.
