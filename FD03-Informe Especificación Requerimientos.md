<center>

![./media/logo-upt.png](./media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERÍA**

**Escuela Profesional de Ingeniería de Sistemas**

**Proyecto: SQL-SafeBridge: Orquestador de Respaldos y Validación de Integridad (SQL Server)**

Curso: Base de Datos II

Docente: Mag. Patrick Cuadros Quiroga

Integrantes:

**Iker Alberto Sierra Ruiz (2023077090)**

**Julio Samuel Cortez Mamani (2023077283)**

**Tacna – Perú**

**2026**

</center>

<div style="page-break-after: always; visibility: hidden"></div>

| CONTROL DE VERSIONES | | | | | |
|:---:|---|---|---|---|---|
| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
| 1.0 | IASR, JSCM | IASR, JSCM | PCQL | 30/04/2026 | Versión Original |

<div style="page-break-after: always; visibility: hidden"></div>

**Sistema: SQL-SafeBridge — Orquestador de Backups y Prueba de Restauración con Validación de Integridad (SQL Server)**

**Documento FD03: Historias de Usuario, Criterios de Aceptación y Diagramas de Secuencia**

**Versión 1.0**

<div style="page-break-after: always; visibility: hidden"></div>

---

# ÍNDICE GENERAL

1. [Introducción](#1-introducción)
   - 1.1 Propósito
   - 1.2 Alcance
   - 1.3 Definiciones, Siglas y Abreviaturas
   - 1.4 Referencias
   - 1.5 Visión General
2. [Generalidades de la Empresa](#2-generalidades-de-la-empresa)
   - 2.1 Nombre de la Empresa
   - 2.2 Visión
   - 2.3 Misión
   - 2.4 Organigrama
3. [Visionamiento de Empresa](#3-visionamiento-de-empresa)
   - 3.1 Descripción del Problema
   - 3.2 Objetivos de Negocio
   - 3.3 Objetivos de Diseño
   - 3.4 Alcance del Proyecto
   - 3.5 Viabilidad del Sistema
   - 3.6 Información Obtenida del Levantamiento de Información
4. [Análisis de Procesos](#4-análisis-de-procesos)
   - 4.1 Diagrama de Proceso Actual – Diagrama de Actividades
   - 4.2 Diagrama de Proceso Propuesto – Diagrama de Actividades
5. [Análisis de Requerimientos de Software](#5-análisis-de-requerimientos-de-software)
   - 5.1 Cuadro de Requerimientos Funcionales Iniciales
   - 5.2 Cuadro de Requerimientos No Funcionales
   - 5.3 Cuadro de Requerimientos Funcionales Finales
   - 5.4 Reglas de Negocio
6. [Historias de Usuario](#6-historias-de-usuario)
   - 6.1 HU-001: Autenticación contra SQL Server
   - 6.2 HU-002: Backup FULL Automatizado
   - 6.3 HU-003: Restore Test en Entorno Sandbox
   - 6.4 HU-004: Validación de Integridad con DBCC CHECKDB
   - 6.5 HU-005: Orquestación del Flujo Completo
   - 6.6 HU-006: Sistema de Logging y Evidencias
   - 6.7 HU-007: Interfaz Gráfica con Consola de Eventos
   - 6.8 HU-008: Configuración de Rutas y Parámetros
   - 6.9 Matriz de Trazabilidad con Requerimientos
   - 6.10 Resumen de Issues en GitHub
7. [Criterios de Aceptación en Formato Gherkin](#7-criterios-de-aceptación-en-formato-gherkin)
   - 7.1 HU-001: Autenticación contra SQL Server
   - 7.2 HU-002: Backup FULL Automatizado
   - 7.3 HU-003: Restore Test en Entorno Sandbox
   - 7.4 HU-004: Validación de Integridad con DBCC CHECKDB
   - 7.5 HU-005: Orquestación del Flujo Completo
   - 7.6 HU-006: Sistema de Logging y Evidencias
   - 7.7 HU-007: Interfaz Gráfica con Consola de Eventos
   - 7.8 HU-008: Configuración de Rutas y Parámetros
8. [Diagramas de Secuencia](#8-diagramas-de-secuencia)
   - 8.1 Login y Autenticación
   - 8.2 Flujo Completo Backup + Validación
   - 8.3 Manejo de Error durante el Flujo
   - 8.4 Generación de Evidencias
9. [Fase de Desarrollo](#9-fase-de-desarrollo)
   - 9.1 Perfiles de Usuario
   - 9.2 Modelo Conceptual
   - 9.3 Modelo Lógico
10. [Milestones y Plan de Implementación](#10-milestones-y-plan-de-implementación)
- [Conclusiones](#conclusiones)
- [Recomendaciones](#recomendaciones)
- [Bibliografía](#bibliografía)
- [Webgrafía](#webgrafía)

<div style="page-break-after: always; visibility: hidden"></div>

---

## 1. Introducción

### 1.1 Propósito

El presente documento **FD03 — Historias de Usuario, Criterios de Aceptación y Diagramas de Secuencia** tiene como propósito detallar los requerimientos funcionales del sistema **SQL-SafeBridge** en formato de historias de usuario ágiles, especificar sus criterios de aceptación mediante escenarios Gherkin, y modelar las interacciones del sistema mediante diagramas de secuencia UML.

Este documento sirve como especificación funcional detallada para el equipo de desarrollo y como artefacto de validación para los interesados del proyecto, asegurando que cada funcionalidad esté correctamente definida, sea verificable y esté alineada con los objetivos del sistema definidos en el Documento de Visión (FD02).

### 1.2 Alcance

El alcance de este documento comprende:

- **8 historias de usuario** registradas como Issues en GitHub (#19 al #26), cubriendo el flujo completo del sistema: autenticación, backup, restore test, validación, orquestación, logging, interfaz gráfica y configuración.
- **16 escenarios Gherkin** (2 por cada historia de usuario: un escenario exitoso y un escenario de error o condición límite).
- **4 diagramas de secuencia UML** en formato Mermaid que modelan las interacciones principales entre actores, capas de la arquitectura y SQL Server.
- **Matriz de trazabilidad** que vincula cada historia de usuario con los requerimientos funcionales y no funcionales definidos en el FD02.
- **Perfiles de usuario, modelo conceptual y modelo lógico** como parte de la fase de desarrollo.
- **Plan de implementación** organizado por milestones alineados con el roadmap del proyecto.

Quedan fuera del alcance de este documento:

- Especificaciones técnicas de bajo nivel (consultar documentación de arquitectura en la GitHub Wiki).
- Pruebas unitarias detalladas (consultar plan de pruebas en la GitHub Wiki).

### 1.3 Definiciones, Siglas y Abreviaturas

| Término | Definición |
|---------|-----------|
| **HU** | Historia de Usuario — descripción de una funcionalidad desde la perspectiva del usuario. |
| **Gherkin** | Lenguaje de dominio específico para describir escenarios de prueba en formato DADO/CUANDO/ENTONCES. |
| **Issue** | Unidad de trabajo registrada en GitHub que representa una tarea, mejora o bug. |
| **Label** | Etiqueta de clasificación aplicada a Issues en GitHub (ej. `feature`, `bug`, `high-priority`). |
| **Milestone** | Hito del proyecto que agrupa Issues con una fecha objetivo común. |
| **UML** | Unified Modeling Language — lenguaje estándar para modelar sistemas de software. |
| **Mermaid** | Herramienta de diagramación basada en texto, compatible con Markdown y GitHub. |
| **Clean Architecture** | Enfoque de arquitectura que separa UI, casos de uso, entidades e infraestructura. |
| **DBA** | Database Administrator — Administrador de Bases de Datos. |
| **Sandbox** | Base de datos temporal restaurada desde el backup, separada de producción. |
| **DBCC CHECKDB** | Comando de SQL Server que valida consistencia lógica y física de una base de datos. |
| **RTO** | Recovery Time Objective — máximo tiempo aceptable para restablecer el servicio. |
| **RPO** | Recovery Point Objective — máximo período aceptable de pérdida de datos. |
| **SHA256** | Secure Hash Algorithm de 256 bits — función hash criptográfica para verificar integridad de archivos. |

### 1.4 Referencias

Los siguientes documentos y estándares son referencias relevantes para este documento:

- Documento de Visión SQL-SafeBridge (FD02) — Versión 1.0, marzo 2026.
- Informe de Factibilidad SQL-SafeBridge (FD01) — Versión 1.0, marzo 2026.
- GitHub Issues del repositorio SQL-SafeBridge: Issues #19 al #26.
- Microsoft SQL Server Documentation: BACKUP/RESTORE — https://learn.microsoft.com/en-us/sql/
- Microsoft SQL Server Documentation: DBCC CHECKDB — https://learn.microsoft.com/en-us/sql/
- IEEE 830-1998 — Recommended Practice for Software Requirements Specifications.
- Especificación Gherkin — https://cucumber.io/docs/gherkin/
- GitHub Docs: About Wikis — https://docs.github.com/en/communities/documenting-your-project-with-wikis

### 1.5 Visión General

El documento FD03 se estructura en las siguientes secciones principales:

1. **Generalidades de la Empresa:** Nombre, visión, misión y organigrama de SQL-SafeBridge.
2. **Visionamiento de Empresa:** Problema identificado, objetivos de negocio, objetivos de diseño y alcance.
3. **Análisis de Procesos:** Diagramas de actividades del proceso actual y propuesto.
4. **Análisis de Requerimientos:** Requerimientos funcionales, no funcionales y reglas de negocio.
5. **Historias de Usuario:** Cada funcionalidad en formato "Como... Quiero... Para...", vinculada a su Issue en GitHub.
6. **Criterios de Aceptación en Formato Gherkin:** Escenarios de prueba exitosos y de error.
7. **Diagramas de Secuencia:** Interacciones entre actores, capas de arquitectura y SQL Server.
8. **Fase de Desarrollo:** Perfiles de usuario, modelo conceptual y modelo lógico.
9. **Milestones y Plan de Implementación:** Organización del trabajo en hitos.

<div style="page-break-after: always; visibility: hidden"></div>

---

## 2. Generalidades de la Empresa

### 2.1 Nombre de la Empresa

**SQL-SafeBridge**

### 2.2 Visión

Consolidarnos como la principal aliada tecnológica en la región de Tacna, liderando soluciones de protección y resiliencia de datos corporativos con innovación y confiabilidad.

### 2.3 Misión

Proveer soluciones automatizadas de respaldo y recuperación que garanticen la continuidad del negocio de nuestros clientes, reduciendo riesgos operativos y asegurando el cumplimiento normativo.

### 2.4 Organigrama
┌─────────────────────┐
│ Gerente General │
│ Iker Sierra Ruiz │
└──────────┬──────────┘
│
┌─────────────────────┼─────────────────────┐
│ │ │
┌────────────▼──────────┐ ┌───────▼──────────┐ ┌───────▼──────────┐
│ Jefe de Desarrollo │ │ Jefe de Calidad │ │ Jefe de Soporte │
│ Julio Cortez Mamani │ │ (Por designar) │ │ (Por designar) │
└───────────┬───────────┘ └──────────────────┘ └──────────────────┘
│
┌───────────┼───────────┐
│ │ │
┌───▼────┐ ┌───▼────┐ ┌───▼────┐
│ Backend│ │Frontend│ │ QA │
│ Dev │ │ Dev │ │ Tester │
└────────┘ └────────┘ └────────┘

<div style="page-break-after: always; visibility: hidden"></div>

---

## 3. Visionamiento de Empresa

### 3.1 Descripción del Problema

Actualmente, existe una brecha de seguridad alarmante: mientras los administradores de bases de datos dedican entre el 20% y 30% de su tiempo a tareas manuales de backup, la mayoría de las empresas omite las pruebas de recuperación. Este escenario no solo amenaza la integridad de la información, sino que expone a la entidad a sanciones legales por incumplimiento de estándares como ISO 27001, PCI-DSS y normativas locales de protección de datos.

Los problemas específicos identificados son:

| Problema | Impacto |
|----------|---------|
| Backups manuales propensos a error humano | Pérdida de datos, retrasos operativos |
| Ausencia de pruebas de restauración | Backups inservibles detectados solo en emergencias |
| Falta de validación de integridad | Datos corruptos no detectados a tiempo |
| Sin registro de evidencias | Incumplimiento normativo y de auditoría |
| Procesos no estandarizados | Dependencia del conocimiento individual del DBA |

### 3.2 Objetivos de Negocio

- **OB-01:** Automatizar el ciclo de backup para liberar el 80% del tiempo técnico del DBA.
- **OB-02:** Garantizar restauraciones exitosas mediante pruebas automáticas en entorno sandbox.
- **OB-03:** Asegurar cumplimiento normativo absoluto con generación de evidencias auditables.

### 3.3 Objetivos de Diseño

- **OD-01:** Interfaz gráfica intuitiva (máximo 3 clics por operación).
- **OD-02:** Tiempo de restauración de prueba < 4 horas.
- **OD-03:** Soporte para SQL Server (versión inicial).
- **OD-04:** Arquitectura limpia con separación de capas (Clean Architecture).
- **OD-05:** Generación automática de logs en formato .log y .json.

### 3.4 Alcance del Proyecto

| Aspecto | Detalle |
|---------|---------|
| Duración | 4 meses (marzo - junio 2026) |
| Funcionalidades | Backups automáticos + validación DBCC + pruebas de restauración + logging |
| Motor soportado | SQL Server 2022 (Developer/Express) |
| Tipo de aplicación | Escritorio (Python + customtkinter) |
| Exclusiones | Soporte Oracle (fase 2), interfaz web (fase 3) |
| Entregables | Aplicación de escritorio, documentación técnica, manual de usuario |

### 3.5 Viabilidad del Sistema

*(Por completar con análisis de factibilidad técnica, operativa y económica)*

### 3.6 Información Obtenida del Levantamiento de Información

*(Por completar con resultados de entrevistas, encuestas u observaciones realizadas durante la fase de relevamiento)*

<div style="page-break-after: always; visibility: hidden"></div>

---

## 4. Análisis de Procesos

### 4.1 Diagrama de Proceso Actual – Diagrama de Actividades

El siguiente diagrama modela el flujo actual de trabajo del DBA al realizar backups y pruebas de restauración de forma manual:

```mermaid
flowchart TD
    A[Inicio] --> B[DBA recuerda hacer backup]
    B --> C[Ejecuta script manual en SSMS]
    C --> D[Espera finalización]
    D --> E{¿Terminó sin errores?}
    E -->|Sí| F[Guarda archivo .bak en disco]
    E -->|No| G[Revisa errores y reintenta]
    G --> C
    F --> H[Registra en Excel manualmente]
    H --> I{¿Hay tiempo para restore test?}
    I -->|Sí| J[Restaura manualmente en otra BD]
    I -->|No| K[Omite prueba de restauración]
    J --> L[Ejecuta DBCC CHECKDB manualmente]
    L --> M[Registra resultado en Excel]
    K --> N[Fin - Backup sin validar]
    M --> O[Fin - Backup validado]
    
### 4.2 Diagrama de Proceso Propuesto – Diagrama de Actividades
El siguiente diagrama modela el flujo automatizado propuesto con SQL-SafeBridge:
flowchart TD
    A[Inicio] --> B[DBA autentica en SQL-SafeBridge]
    B --> C[Selecciona base de datos]
    C --> D[Clic en Backup + Validación]
    D --> E[Sistema ejecuta BACKUP DATABASE]
    E --> F[Genera archivo .bak con naming automático]
    F --> G[Sistema restaura en sandbox]
    G --> H{¿Restauración exitosa?}
    H -->|Sí| I[Sistema ejecuta DBCC CHECKDB]
    H -->|No| J[Registra error y detiene flujo]
    I --> K{¿CHECKDB sin errores?}
    K -->|Sí| L[Marcar backup como Validado]
    K -->|No| M[Marcar backup como No Validado]
    L --> N[Generar evidencias .log y .json]
    M --> N
    J --> N
    N --> O[Limpiar BD sandbox]
    O --> P[Mostrar resultado en GUI]
    P --> Q[Fin]

Mejoras del proceso propuesto:

Automatización completa: el DBA solo requiere 3 clics.

Nomenclatura estandarizada de archivos.

Trazabilidad automática con logs estructurados.

Validación de integridad obligatoria en cada ejecución.

Limpieza automática del entorno sandbox.

<div style="page-break-after: always; visibility: hidden"></div>
5. Análisis de Requerimientos de Software
5.1 Cuadro de Requerimientos Funcionales Iniciales
ID	REQUERIMIENTO
RF-01	Permitir programar backups diarios y semanales
RF-02	Soportar conexiones con SQL Server
RF-03	Calcular y almacenar hash SHA256 de los backups
RF-04	Ejecutar la restauración de prueba automáticamente
RF-05	Enviar alertas de seguridad por correo
RF-06	Tener una interfaz de escritorio intuitiva
RF-07	Generar logs de auditoría en formatos .log y .json
RF-08	Permitir recuperar la base de datos desde el backup
5.2 Cuadro de Requerimientos No Funcionales
ID	REQUERIMIENTO
RNF-1	Disponibilidad del sistema a tiempo completo
RNF-2	Tener el menor tiempo de restauración posible
RNF-3	Tener una seguridad especial para los datos personales
RNF-4	Cumplir con las normas de auditoría (ISO 27001)
RNF-5	Ser accesible y fácil de usar
RNF-6	Las credenciales no deben persistirse en texto plano
5.3 Cuadro de Requerimientos Funcionales Finales
(Por completar tras la validación con stakeholders y refinamiento de los requerimientos iniciales)

5.4 Reglas de Negocio
ID	REGLA DE NEGOCIO
RN-01	El backup solo se considera válido si supera la prueba de Hash SHA256
RN-02	No se pueden eliminar backups que no superen los 30 días de antigüedad
RN-03	Cada restauración de prueba se debe realizar en un entorno aislado (sandbox)
RN-04	Solo usuarios con rol sysadmin pueden ejecutar operaciones de backup
RN-05	Las evidencias deben conservarse por un mínimo de 90 días
RN-06	El sistema debe validar que la ruta de backup sea accesible antes de ejecutar
RN-07	La BD sandbox debe eliminarse automáticamente tras la validación
RN-08	Los logs no deben contener contraseñas ni datos sensibles
<div style="page-break-after: always; visibility: hidden"></div>
6. Historias de Usuario
A continuación se presentan las historias de usuario registradas como Issues en GitHub, siguiendo el formato estándar de redacción de requerimientos ágiles. Cada historia está vinculada a un Issue real del repositorio y se complementa con su información de trazabilidad, capa arquitectónica y archivos de implementación.

6.1 HU-001: Autenticación contra SQL Server
Campo	Valor
Issue GitHub	#19
Como	DBA
Quiero	Autenticarme con credenciales SQL Server
Para	Acceder de forma segura al sistema y gestionar backups
Capa arquitectónica	Presentation + Infrastructure
Labels	feature, authentication, high-priority
Milestone	M1 — Conexión y Backup
Archivos	presentation/login_screen.py, infrastructure/sql_server_repository.py
Tecnología	customtkinter para UI, pyodbc para conexión
Descripción detallada:

El sistema debe proporcionar una pantalla de login donde el DBA ingrese las credenciales de SQL Server (servidor, usuario y contraseña). Una vez ingresadas, el sistema debe verificar que la conexión sea exitosa y que el usuario posea el rol sysadmin, requerido para ejecutar operaciones de backup y restore. Si el usuario no cumple con los permisos necesarios, el sistema debe denegar el acceso y mostrar un mensaje informativo. Las credenciales no deben persistirse en texto plano en ningún momento.

6.2 HU-002: Backup FULL Automatizado
Campo	Valor
Issue GitHub	#20
Como	DBA
Quiero	Ejecutar backups FULL con un clic desde la GUI
Para	Estandarizar las copias de seguridad y evitar errores manuales
Capa arquitectónica	Application
Labels	feature, backup, high-priority
Milestone	M1 — Conexión y Backup
Archivos	application/backup_use_case.py
Dependencia	HU-001 (Autenticación exitosa)
Descripción detallada:

El sistema debe permitir al DBA seleccionar una base de datos desde un dropdown y ejecutar un backup FULL con un solo clic. El nombre del archivo .bak debe generarse automáticamente siguiendo el formato BD_YYYYMMDD_HHMMSS_FULL.bak. El sistema debe capturar y registrar métricas de la operación: tiempo de inicio, tiempo de finalización, duración total y tamaño del archivo generado. El progreso debe mostrarse en tiempo real en la consola de eventos de la GUI.

6.3 HU-003: Restore Test en Entorno Sandbox
Campo	Valor
Issue GitHub	#21
Como	DBA
Quiero	Restaurar el backup en una base de datos sandbox
Para	Verificar que el respaldo es realmente recuperable antes de un incidente real
Capa arquitectónica	Application
Labels	feature, restore, high-priority
Milestone	M2 — Restore Sandbox
Archivos	application/restore_use_case.py, application/restore_backup_use_case.py
Dependencia	HU-002 (Backup generado exitosamente)
Descripción detallada:

Una vez generado el backup, el sistema debe restaurarlo automáticamente en una base de datos temporal (sandbox) para verificar su recuperabilidad. El proceso implica: (1) leer los logical files del backup mediante RESTORE FILELISTONLY, (2) construir la cláusula WITH MOVE para reubicar los archivos .mdf y .ldf en la ruta de sandbox configurada, y (3) ejecutar la restauración. La base de datos sandbox debe crearse con un sufijo identificable (ej. _Sandbox) y debe quedar accesible para consultas de validación posteriores.

6.4 HU-004: Validación de Integridad con DBCC CHECKDB
Campo	Valor
Issue GitHub	#22
Como	Auditor
Quiero	Ejecutar DBCC CHECKDB en la base de datos restaurada
Para	Confirmar que los datos no tienen corrupción y son íntegros
Capa arquitectónica	Application
Labels	feature, validation, audit
Milestone	M3 — Validación DBCC
Archivos	application/validation_use_case.py
Dependencia	HU-003 (Restore Test exitoso)
Descripción detallada:

Sobre la base de datos sandbox restaurada, el sistema debe ejecutar el comando DBCC CHECKDB para validar la integridad física y lógica de los datos. El resultado del CHECKDB debe ser capturado y analizado: si no se encuentran errores de asignación ni de consistencia, el backup debe marcarse como "Validado"; si se detectan errores, debe marcarse como "No Validado". El resultado completo debe registrarse en los logs de evidencias y mostrarse en la consola de eventos de la GUI.

6.5 HU-005: Orquestación del Flujo Completo
Campo	Valor
Issue GitHub	#23
Como	DBA
Quiero	Que el sistema ejecute Backup → Restore → Validación → Evidencia → Limpieza automáticamente
Para	Ahorrar tiempo y evitar errores al ejecutar cada paso manualmente
Capa arquitectónica	Application
Labels	feature, orchestration, core
Milestone	M4 — Flujo Completo
Archivos	application/orchestrator.py
Dependencia	HU-002, HU-003, HU-004, HU-006, HU-008
Descripción detallada:

El orquestador es el componente central que coordina la ejecución secuencial del flujo completo: Backup → Restore Test → Validación (DBCC CHECKDB) → Generación de Evidencias → Limpieza de Sandbox. Debe ejecutar cada fase en orden, verificando que la fase anterior se complete exitosamente antes de avanzar. Si alguna fase falla, el orquestador debe detener el flujo, registrar el error indicando la fase donde ocurrió, y notificar al usuario a través de la GUI. El progreso de cada fase debe actualizarse en tiempo real en el dashboard.

6.6 HU-006: Sistema de Logging y Evidencias
Campo	Valor
Issue GitHub	#24
Como	Auditor
Quiero	Logs detallados en formato .log y .json por cada ejecución
Para	Tener trazabilidad completa de quién ejecutó qué, cuándo y con qué resultado
Capa arquitectónica	Shared Kernel
Labels	feature, logging, audit
Milestone	M3 — Validación DBCC
Archivos	shared/logger.py
Carpeta de salida	logs/
Descripción detallada:

Cada ejecución del flujo (o de operaciones individuales) debe generar dos archivos de evidencia: un archivo .log con formato legible que incluya timestamps, descripción de cada paso, métricas (tiempos, tamaños) y resultados; y un archivo .json con los mismos datos en formato estructurado para procesamiento automatizado. Los archivos deben nombrarse con el patrón restore_backup_YYYYMMDD_HHMMSS. Bajo ninguna circunstancia los logs deben contener contraseñas ni datos sensibles de conexión.

6.7 HU-007: Interfaz Gráfica con Consola de Eventos
Campo	Valor
Issue GitHub	#25
Como	Usuario
Quiero	Ver el progreso de cada paso en tiempo real en la GUI
Para	Saber qué está ocurriendo sin necesidad de revisar archivos de log
Capa arquitectónica	Presentation
Labels	feature, UI, enhancement
Milestone	M2 — Restore Sandbox
Archivos	presentation/dashboard_screen.py, presentation/dialogs.py
Tecnología	customtkinter
Descripción detallada:

La interfaz gráfica debe incluir un dashboard con una consola de eventos que muestre en tiempo real el progreso de cada operación. Debe utilizar indicadores visuales claros: ✅ para éxito, ❌ para error, 🔄 para operaciones en progreso, y 🧹 para limpieza. Debe incluir una barra de progreso segmentada por fases del flujo. El dashboard debe permitir seleccionar la base de datos de un dropdown, y ofrecer botones para ejecutar Backup, Validación (flujo completo) y acceder a Configuración.

6.8 HU-008: Configuración de Rutas y Parámetros
Campo	Valor
Issue GitHub	#26
Como	DBA
Quiero	Configurar las rutas de almacenamiento de backups y sandbox
Para	Adaptar el sistema a la infraestructura de mi organización
Capa arquitectónica	Presentation
Labels	feature, configuration, enhancement
Milestone	M2 — Restore Sandbox
Archivos	presentation/dialogs.py
Tecnología	customtkinter
Descripción detallada:

El sistema debe proporcionar un diálogo de configuración accesible desde el dashboard, donde el DBA pueda establecer las rutas de almacenamiento para los archivos de backup y para los archivos de la base de datos sandbox. Las rutas ingresadas deben ser validadas (existencia o posibilidad de creación) antes de guardarse. La configuración debe persistir entre sesiones para evitar que el usuario deba reingresarla cada vez.

6.9 Matriz de Trazabilidad con Requerimientos
La siguiente matriz vincula cada historia de usuario con los requerimientos funcionales (RF) y no funcionales (RNF) definidos en el Documento de Visión (FD02), así como con las reglas de negocio (RN) aplicables.

Historia de Usuario	RF-01	RF-02	RF-03	RF-04	RF-05	RF-06	RF-07	RF-08	RNF-1	RNF-2	RNF-3	RNF-4	RNF-5	RNF-6	RN-01	RN-02	RN-03	RN-04	RN-05	RN-06	RN-07	RN-08
HU-001 Autenticación		✅							✅		✅	✅		✅				✅				
HU-002 Backup FULL	✅		✅																	✅		
HU-003 Restore Sandbox				✅				✅		✅							✅					
HU-004 DBCC CHECKDB							✅					✅			✅							
HU-005 Orquestador	✅			✅																	✅	
HU-006 Logging							✅		✅			✅							✅			✅
HU-007 GUI						✅							✅									
HU-008 Configuración						✅										✅				✅		
6.10 Resumen de Issues en GitHub
#	Historia de Usuario	Issue	Prioridad	Milestone	Estado
| 1 | Autenticación	#19	Alta	M1	✅
| 2 |	Backup FULL	#20	Alta	M1	
| 3 | Restore Sandbox | #21 | Alta | M2 | ✅ |
| 4 | DBCC CHECKDB | #22 | Alta | M3 | ✅ |
| 5 | Orquestador | #23 | Alta | M4 | ✅ |
| 6 | Logging | #24 | Alta | M3 | ✅ |
| 7 | GUI | #25 | Media | M2 | ✅ |
| 8 | Configuración | #26 | Media | M2 | ✅ |

<div style="page-break-after: always; visibility: hidden"></div>

---

## 7. Criterios de Aceptación en Formato Gherkin

Por cada historia de usuario se presentan dos escenarios de prueba en formato Gherkin (DADO... CUANDO... ENTONCES...): un **escenario exitoso** que describe el comportamiento esperado bajo condiciones normales, y un **escenario de error o condición límite** que describe el comportamiento ante fallos o condiciones excepcionales.

---

### 7.1 HU-001: Autenticación contra SQL Server

```gherkin
Feature: Autenticación contra SQL Server
  Como DBA
  Quiero autenticarme con credenciales SQL Server
  Para acceder de forma segura al sistema

  Scenario: Login exitoso con credenciales válidas y rol sysadmin
    DADO QUE el usuario tiene credenciales válidas de SQL Server
    Y el usuario tiene el rol sysadmin
    CUANDO ingresa servidor "localhost\SQLEXPRESS", usuario "admin" y contraseña "****"
    Y hace clic en "Conectar"
    ENTONCES el sistema muestra el Dashboard principal
    Y el sistema registra "Conexión establecida" en los logs
    Y habilita todas las funciones de backup y restore

  Scenario: Login fallido por falta de permisos sysadmin
    DADO QUE el usuario tiene credenciales válidas de SQL Server
    PERO el usuario NO tiene el rol sysadmin
    CUANDO ingresa servidor, usuario y contraseña
    Y hace clic en "Conectar"
    ENTONCES el sistema muestra el mensaje "Permisos insuficientes: se requiere rol sysadmin"
    Y NO habilita las funciones de backup
    Y registra el intento fallido en los logs
### 7.2 HU-002: Backup FULL Automatizado
Feature: Backup FULL Automatizado
  Como DBA
  Quiero ejecutar backups FULL con un clic
  Para estandarizar las copias de seguridad

  Scenario: Backup FULL generado exitosamente
    DADO QUE el usuario está autenticado con rol sysadmin
    Y ha seleccionado la base de datos "VentasDB"
    Y la ruta de backup "C:\Backups\" es accesible
    CUANDO hace clic en "Ejecutar Backup"
    ENTONCES el sistema ejecuta BACKUP DATABASE correctamente
    Y genera el archivo "VentasDB_20260430_143000_FULL.bak"
    Y calcula y almacena el hash SHA256 del archivo
    Y muestra el tamaño del archivo en la consola
    Y registra tiempo de inicio, fin y tamaño en logs

  Scenario: Backup fallido por ruta inaccesible
    DADO QUE el usuario está autenticado con rol sysadmin
    Y ha seleccionado una base de datos
    PERO la ruta de backup no es accesible por SQL Server
    CUANDO hace clic en "Ejecutar Backup"
    ENTONCES el sistema muestra "Error: Ruta de backup no accesible"
    Y NO genera archivo .bak
    Y registra el error en los logs con nivel ERROR
### 7.3 HU-003: Restore Test en Entorno Sandbox
Feature: Restore Test en Entorno Sandbox
  Como DBA
  Quiero restaurar el backup en una BD temporal
  Para verificar que el respaldo es recuperable

  Scenario: Restauración exitosa en sandbox
    DADO QUE existe un archivo .bak válido en "C:\Backups\"
    Y el usuario tiene permisos suficientes
    CUANDO se ejecuta el restore test
    ENTONCES el sistema lee los logical files con RESTORE FILELISTONLY
    Y restaura la BD en "VentasDB_Sandbox" usando WITH MOVE
    Y la BD sandbox queda accesible para consultas
    Y registra "Restauración completada" en la consola

  Scenario: Restauración fallida por espacio insuficiente
    DADO QUE existe un archivo .bak válido
    PERO el espacio en disco es insuficiente
    CUANDO se ejecuta el restore test
    ENTONCES el sistema muestra "Error: Espacio insuficiente en disco"
    Y NO crea la BD sandbox
    Y registra el error en logs
###   7.3 HU-003: Restore Test en Entorno Sandbox
Feature: Restore Test en Entorno Sandbox
  Como DBA
  Quiero restaurar el backup en una BD temporal
  Para verificar que el respaldo es recuperable

  Scenario: Restauración exitosa en sandbox
    DADO QUE existe un archivo .bak válido en "C:\Backups\"
    Y el usuario tiene permisos suficientes
    CUANDO se ejecuta el restore test
    ENTONCES el sistema lee los logical files con RESTORE FILELISTONLY
    Y restaura la BD en "VentasDB_Sandbox" usando WITH MOVE
    Y la BD sandbox queda accesible para consultas
    Y registra "Restauración completada" en la consola

  Scenario: Restauración fallida por espacio insuficiente
    DADO QUE existe un archivo .bak válido
    PERO el espacio en disco es insuficiente
    CUANDO se ejecuta el restore test
    ENTONCES el sistema muestra "Error: Espacio insuficiente en disco"
    Y NO crea la BD sandbox
    Y registra el error en logs
### 7.4 HU-004: Validación de Integridad con DBCC CHECKDB
Feature: Validación de Integridad con DBCC CHECKDB
  Como auditor
  Quiero ejecutar DBCC CHECKDB en la BD restaurada
  Para confirmar la integridad de los datos

  Scenario: DBCC CHECKDB sin errores
    DADO QUE la BD sandbox "VentasDB_Sandbox" está accesible
    Y los datos fueron restaurados correctamente
    CUANDO se ejecuta DBCC CHECKDB
    ENTONCES el resultado es "CHECKDB found 0 allocation errors and 0 consistency errors"
    Y el sistema marca el backup como "Validado"
    Y registra "CHECKDB: Sin errores" en logs

  Scenario: DBCC CHECKDB detecta corrupción
    DADO QUE la BD sandbox está accesible
    PERO existen errores de consistencia en los datos
    CUANDO se ejecuta DBCC CHECKDB
    ENTONCES el sistema detecta los errores
    Y marca el backup como "No Validado"
    Y registra el detalle de errores en logs
    Y muestra "CHECKDB: Errores detectados" en la consola
### 7.5 HU-005: Orquestación del Flujo Completo
Feature: Orquestación del Flujo Completo
  Como DBA
  Quiero ejecutar el ciclo completo automáticamente
  Para ahorrar tiempo y evitar errores manuales

  Scenario: Flujo completo exitoso
    DADO QUE el usuario está autenticado
    Y ha seleccionado la base de datos y configurado rutas
    CUANDO hace clic en "Ejecutar Backup + Validación"
    ENTONCES el orquestador ejecuta en secuencia:
    Y 1. Backup FULL completado
    Y 2. Restore Test completado
    Y 3. DBCC CHECKDB completado sin errores
    Y 4. Evidencias generadas (.log y .json)
    Y 5. BD sandbox eliminada
    Y el sistema muestra "Proceso completado exitosamente"
    Y registra tiempo total de ejecución

  Scenario: Flujo interrumpido por error en restore
    DADO QUE el backup se generó correctamente
    PERO ocurre un error durante la restauración
    CUANDO el orquestador detecta el error
    ENTONCES detiene el flujo
    Y registra el error indicando la fase donde ocurrió
    Y NO ejecuta los pasos siguientes
    Y limpia recursos temporales si es posible
### 7.6 HU-006: Sistema de Logging y Evidencias
Feature: Sistema de Logging y Evidencias
  Como auditor
  Quiero logs detallados por cada ejecución
  Para tener trazabilidad completa

  Scenario: Generación de logs tras ejecución exitosa
    DADO QUE se ejecutó el flujo completo exitosamente
    CUANDO finaliza la orquestación
    ENTONCES se genera el archivo "restore_backup_YYYYMMDD_HHMMSS.log"
    Y se genera el archivo "restore_backup_YYYYMMDD_HHMMSS.json"
    Y el archivo .log contiene timestamps, pasos y resultado de cada fase
    Y el archivo .json contiene datos estructurados con métricas
    Y ningún archivo contiene contraseñas

  Scenario: Logs registran errores correctamente
    DADO QUE ocurrió un error durante el backup
    CUANDO se captura la excepción
    ENTONCES el archivo .log registra el error con nivel ERROR
    Y el archivo .json incluye "final_status": "backup_failed"
    Y se detalla el mensaje de error sin exponer información sensible
### 7.7 HU-007: Interfaz Gráfica con Consola de Eventos
Feature: Interfaz Gráfica con Consola de Eventos
  Como usuario
  Quiero ver el progreso en tiempo real en la GUI
  Para saber qué está ocurriendo sin revisar archivos

  Scenario: Consola muestra progreso del flujo completo
    DADO QUE el usuario ejecutó "Backup + Validación"
    CUANDO el orquestador avanza por cada fase
    ENTONCES la consola muestra en tiempo real:
    Y "✅ Conexión establecida"
    Y "🔄 Iniciando backup FULL..."
    Y "✅ Backup completado (X MB)"
    Y "🔄 Restaurando en sandbox..."
    Y "✅ Restauración completada"
    Y "🔄 Ejecutando DBCC CHECKDB..."
    Y "✅ CHECKDB: Sin errores"
    Y "🧹 Limpiando sandbox..."
    Y "✅ Proceso completado (X segundos)"

  Scenario: Consola muestra error con indicador visual
    DADO QUE ocurre un error durante la ejecución
    CUANDO el sistema captura la excepción
    ENTONCES la consola muestra "❌ Error: [descripción]"
    Y el indicador visual cambia a estado de error
    Y se mantiene visible el historial de pasos anteriores
### 7.8 HU-008: Configuración de Rutas y Parámetros
Feature: Configuración de Rutas y Parámetros
  Como DBA
  Quiero configurar las rutas de almacenamiento
  Para adaptar el sistema a mi infraestructura

  Scenario: Configuración de rutas guardada exitosamente
    DADO QUE el usuario abre el diálogo de configuración
    CUANDO ingresa ruta de backups "C:\Backups\"
    Y ruta de sandbox "C:\Sandbox\"
    Y hace clic en "Guardar"
    ENTONCES el sistema valida que las rutas existan o las crea
    Y persiste la configuración
    Y muestra "Configuración guardada correctamente"

  Scenario: Configuración rechazada por ruta inválida
    DADO QUE el usuario abre el diálogo de configuración
    CUANDO ingresa una ruta con caracteres no permitidos
    Y hace clic en "Guardar"
    ENTONCES el sistema muestra "Ruta inválida"
    Y NO guarda la configuración
    Y mantiene la configuración anterior
<div style="page-break-after: always; visibility: hidden"></div>

---

## 8. Diagramas de Secuencia

A continuación se presentan los diagramas de secuencia UML para los flujos principales del sistema. Los diagramas están representados en formato **Mermaid**, compatible con GitHub Markdown.

---

### 8.1 Diagrama de Secuencia: Login y Autenticación

**Flujo:** El usuario ingresa credenciales → LoginScreen → SQLServerRepository → SQL Server

```mermaid
sequenceDiagram
    actor Usuario
    participant LoginScreen
    participant SQLServerRepository
    participant SQLServer

    Usuario->>LoginScreen: Ingresa servidor, usuario, contraseña
    Usuario->>LoginScreen: Clic en "Conectar"
    LoginScreen->>SQLServerRepository: connect(server, user, password)
    SQLServerRepository->>SQLServer: pyodbc.connect()

    alt Conexión exitosa con sysadmin
        SQLServer-->>SQLServerRepository: Conexión OK
        SQLServerRepository->>SQLServer: SELECT IS_SRVROLEMEMBER('sysadmin')
        SQLServer-->>SQLServerRepository: 1 (es sysadmin)
        SQLServerRepository-->>LoginScreen: Conexión exitosa
        LoginScreen->>Usuario: Mostrar Dashboard
    else Usuario sin sysadmin
        SQLServer-->>SQLServerRepository: Conexión OK
        SQLServerRepository->>SQLServer: SELECT IS_SRVROLEMEMBER('sysadmin')
        SQLServer-->>SQLServerRepository: 0 (no es sysadmin)
        SQLServerRepository-->>LoginScreen: Permisos insuficientes
        LoginScreen->>Usuario: Mostrar "Permisos insuficientes"
    else Error de conexión
        SQLServer-->>SQLServerRepository: Error de conexión
        SQLServerRepository-->>LoginScreen: Error
        LoginScreen->>Usuario: Mostrar "Error de conexión"
    end