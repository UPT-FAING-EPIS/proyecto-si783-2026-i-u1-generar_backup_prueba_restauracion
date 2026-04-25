````markdown name=FD02-Informe-Vision.md
<center>

![./media/logo-upt.png](./media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERIA**

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

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

|CONTROL DE VERSIONES||||||
| :-: | :- | :- | :- | :- | :- |
|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo|
|1.0|IASR, JSCM|IASR, JSCM|PCQL|28/03/2026|Versión Original (adaptada a SQL-SafeBridge)|

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

**Sistema: SQL-SafeBridge — Orquestador de Backups y Prueba de Restauración con Validación de Integridad (SQL Server)**

**Documento de Visión**

**Versión 1.0**

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

|CONTROL DE VERSIONES||||||
| :-: | :- | :- | :- | :- | :- |
|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo|
|1.0|IASR, JSCM|IASR, JSCM|PCQL|28/03/2026|Versión Original (adaptada a SQL-SafeBridge)|

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

**INDICE GENERAL**

[1. Introducción](#introducción)

1.1 Propósito

1.2 Alcance

1.3 Definiciones, Siglas y Abreviaturas

1.4 Referencias

1.5 Visión General

[2. Posicionamiento](#posicionamiento)

2.1 Oportunidad de negocio

2.2 Definición del problema

[3. Descripción de los interesados y usuarios](#descripción-de-los-interesados-y-usuarios)

3.1 Resumen de los interesados

3.2 Resumen de los usuarios

3.3 Entorno de usuario

3.4 Perfiles de los interesados

3.5 Perfiles de los Usuarios

3.6 Necesidades de los interesados y usuarios

[4. Vista General del Producto](#vista-general-del-producto)

4.1 Perspectiva del producto

4.2 Resumen de capacidades

4.3 Suposiciones y dependencias

4.4 Costos y precios

4.5 Licenciamiento e instalación

[5. Características del producto](#características-del-producto)

[6. Restricciones](#restricciones)

[7. Rangos de calidad](#rangos-de-calidad)

[8. Precedencia y Prioridad](#precedencia-y-prioridad)

[9. Otros requerimientos del producto](#otros-requerimientos-del-producto)

[CONCLUSIONES](#conclusiones)

[RECOMENDACIONES](#recomendaciones)

[BIBLIOGRAFIA](#bibliografia)

[WEBGRAFIA](#webgrafia)

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

## Introducción

### 1.1 Propósito

El presente documento de visión establece los requisitos, características y restricciones del sistema **SQL-SafeBridge: Orquestador de Respaldos y Validación de Integridad (SQL Server)**. Su propósito principal es proporcionar una visión clara y compartida del proyecto a todos los interesados (docente, equipo de desarrollo, administradores de bases de datos, auditores internos y responsables de TI), sirviendo como base para el desarrollo del sistema y asegurando alineación respecto a objetivos, alcances, beneficios esperados y criterios de éxito.

Asimismo, este documento facilita la toma de decisiones estratégicas durante las fases posteriores del desarrollo, manteniendo consistencia con los requisitos técnicos y necesidades reales de continuidad de datos en entornos SQL Server.

### 1.2 Alcance

El alcance del proyecto comprende el desarrollo de una **aplicación de escritorio** orientada a entornos SQL Server (instancias locales o remotas) que automatiza el ciclo crítico de **Backup + Restore Test + Validación + Evidencia + Limpieza**, incluyendo:

- Generación de backups (principalmente **FULL**) con nomenclatura automática e inteligente (ej. `BD_YYYYMMDD_HHMMSS_FULL.bak`).
- Prueba de restauración automática en una base de datos **sandbox/espejo**, utilizando `WITH MOVE` para reubicar archivos físicos `.mdf` y `.ldf`.
- Auditoría técnica y validación de integridad mediante:
  - `DBCC CHECKDB` sobre la base restaurada.
  - Validaciones comparativas básicas (por ejemplo, existencia de objetos críticos y conteos de registros según configuración).
- Registro de evidencias: archivos `.log` detallados, métricas de tiempo, resultados de cada paso y errores capturados.
- Actualización en tiempo real en la interfaz (consola de eventos y barras de progreso).
- Limpieza automática al finalizar (DROP de la base sandbox) para optimizar almacenamiento.

**Tecnologías base dentro del alcance:**
- Python 3.12+ (orquestación).
- `customtkinter` (UI moderna).
- `pyodbc` + ODBC Driver (conectividad SQL Server vía TDS).
- Patrones de diseño orientados a **Clean Architecture**.

**Fuera de alcance (para esta versión académica):**
- Soporte multi-motor (por ejemplo Oracle).
- Portal web / despliegue en nube.
- Recuperación granular de objetos individuales (object-level recovery) tipo enterprise.
- Integraciones corporativas avanzadas (SIEM, AD/LDAP, SMS, etc.), salvo que se simulen.

### 1.3 Definiciones, Siglas y Abreviaturas

- **Backup**: Copia de seguridad de una base de datos (en SQL Server, archivo `.bak`).
- **Restore Test**: Restauración de prueba del backup en una BD sandbox para verificar recuperabilidad.
- **Sandbox / Espejo**: Base de datos temporal restaurada desde el backup, separada de producción.
- **RPO (Recovery Point Objective)**: Punto objetivo de recuperación; máximo período aceptable de pérdida de datos.
- **RTO (Recovery Time Objective)**: Tiempo objetivo de recuperación; máximo tiempo aceptable para restablecer el servicio.
- **DBCC CHECKDB**: Comando de SQL Server que valida consistencia lógica y física de una base de datos.
- **TDS**: Tabular Data Stream (protocolo de comunicación usado por SQL Server).
- **ODBC**: Open Database Connectivity (estándar para conectividad a bases de datos).
- **GUI**: Interfaz gráfica de usuario.
- **Clean Architecture**: Enfoque de arquitectura que separa UI, casos de uso, entidades e infraestructura.
- **DBA**: Database Administrator (Administrador de Bases de Datos).
- **Sysadmin**: Rol de servidor en SQL Server con privilegios administrativos máximos.

### 1.4 Referencias

Los siguientes documentos y estándares son referencias relevantes para este proyecto:

- Microsoft SQL Server Documentation: Backup and Restore (https://learn.microsoft.com/en-us/sql/)
- Microsoft SQL Server Documentation: DBCC CHECKDB (https://learn.microsoft.com/en-us/sql/)
- ISO/IEC 27001:2022 - Information Security Management Systems (referencia de buenas prácticas)
- IEEE 830-1998 - Recommended Practice for Software Requirements Specifications
- Estándares de Ingeniería de Software de la Universidad Privada de Tacna

### 1.5 Visión General

**SQL-SafeBridge** es una solución de escritorio diseñada para que la seguridad de los datos no dependa únicamente de “tener un backup”, sino de contar con **evidencia automática de que dicho backup es restaurable y consistente**. La visión del sistema es convertir un proceso manual y propenso a errores (backup/restauración) en un flujo orquestado, repetible y auditable.

La herramienta busca brindar al DBA una estación de trabajo moderna que permita:
- Ejecutar respaldos con parámetros seguros y consistentes.
- Restaurar inmediatamente el backup en un entorno temporal.
- Verificar integridad con `DBCC CHECKDB` y validaciones adicionales.
- Registrar evidencias completas de lo sucedido (quién, cuándo, qué, resultado).

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

## Posicionamiento

### 2.1 Oportunidad de negocio

En muchas organizaciones y entornos académicos, los respaldos aún se gestionan de manera manual en SSMS. En la práctica, esto genera dos problemas críticos: (1) ejecución irregular o no estandarizada, y (2) ausencia de pruebas de restauración, lo cual produce “backups de fe” (se asume que sirven, pero no se comprueba).

La oportunidad de negocio (y de valor) de SQL-SafeBridge consiste en ofrecer una solución que reduzca el riesgo operativo mediante:

- Automatización del ciclo de continuidad (backup + restore test).
- Validación técnica inmediata (CHECKDB + pruebas básicas).
- Evidencia auditable con métricas reales de duración y resultados.
- Estándares de nomenclatura, retención y limpieza.

En el segmento objetivo (DBAs, equipos TI y entornos educativos con SQL Server), esta herramienta genera valor por reducción de errores, ahorro de tiempo operativo y mejora de cumplimiento y trazabilidad.

### 2.2 Definición del problema

El problema central es la falta de verificación continua sobre la recuperabilidad real de los backups y la dependencia de procedimientos manuales.

En particular, se presentan las siguientes situaciones:

- **Backups generados sin prueba de restauración**, por lo que no existe certeza de que funcionarán en un incidente real.
- **Alta probabilidad de error humano** al escribir comandos T-SQL manualmente (rutas, nombres, opciones).
- **Escasa trazabilidad**: se desconoce quién ejecutó una operación, qué parámetros usó o cuál fue el resultado.
- **Falta de métricas reales**: no se mide el tiempo de backup y restore para estimar RTO.

SQL-SafeBridge resuelve esto mediante orquestación y validación automática con evidencias, elevando la confiabilidad del proceso.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

## Descripción de los interesados y usuarios

### 3.1 Resumen de los interesados

- **Administradores de Base de Datos (DBA):** usuarios principales; configuran, ejecutan y validan respaldos.
- **Equipo de TI / Soporte:** necesita continuidad operativa y procedimientos repetibles.
- **Área de Auditoría/Control Interno (cuando aplique):** requiere evidencia de operaciones y trazabilidad.
- **Docente y jurado académico:** evalúan documentación, ingeniería aplicada y cumplimiento del alcance.
- **Usuarios finales del sistema de información (indirectos):** se benefician de mayor disponibilidad y menor riesgo.

### 3.2 Resumen de los usuarios

- DBA Senior/Junior: ejecutan backups, restore test y revisan reportes.
- Analista de continuidad: revisa evidencia y métricas.
- Auditor/Compliance (modo consulta): revisa logs/historial.

### 3.3 Entorno de usuario

- Estaciones de trabajo con Windows (entorno recomendado por SQL Server/SSMS).
- Conectividad a instancias SQL Server locales o remotas.
- Rutas de almacenamiento con permisos adecuados (NTFS/compartidos).
- Operación típica: ventanas de mantenimiento o ejecución en horarios definidos.

### 3.4 Perfiles de los interesados

**Perfil 1 - Responsable de TI / Infraestructura:** requiere disminución de riesgos y evidencia de continuidad.

**Perfil 2 - DBA:** requiere automatización, control, seguridad y rapidez, con visibilidad del estado.

**Perfil 3 - Auditor / Control:** requiere trazabilidad: quién, cuándo, qué, resultados.

### 3.5 Perfiles de los Usuarios

**Usuario Tipo 1 - DBA Senior:** requiere flexibilidad (rutas, opciones, exclusiones, configuración avanzada).

**Usuario Tipo 2 - DBA Junior:** requiere guía paso a paso, UI clara, validaciones y mensajes entendibles.

**Usuario Tipo 3 - Auditor/Docente (consulta):** requiere reportes, historial y evidencias descargables.

### 3.6 Necesidades de los interesados y usuarios

- Automatizar ejecución y reducir errores manuales.
- Garantizar que el backup sea restaurable (restore test).
- Validar consistencia (CHECKDB) y mantener evidencia.
- Minimizar impacto en producción con sandbox y limpieza.
- Permitir control de acceso: habilitar funciones solo a usuarios autorizados (por rol en SQL Server).

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

## Vista General del Producto

### 4.1 Perspectiva del producto

SQL-SafeBridge actúa como una capa de orquestación entre el DBA y SQL Server, sin reemplazar las capacidades nativas del motor; las utiliza y las hace seguras, repetibles y auditables.

Arquitectura propuesta (alto nivel):
- **UI Layer:** aplicación de escritorio (customtkinter) con consola de eventos, progreso y configuración.
- **Use Case Layer:** orquestación del flujo (backup → restore test → validación → evidencia → limpieza).
- **Infrastructure Layer:** ejecución de T-SQL y conectividad (pyodbc).
- **Entity Layer:** modelos de ejecución, reportes, estados, eventos y resultados.

### 4.2 Resumen de capacidades

- **Gestión de conexión segura:** credenciales ingresadas por el usuario; verificación de permisos (p. ej., sysadmin).
- **Generación automática de backups FULL:** con naming estándar y parámetros seguros.
- **Restauración sandbox inmediata:** restauración del `.bak` en una BD temporal evitando conflicto de archivos con `WITH MOVE`.
- **Validación técnica:** `DBCC CHECKDB` y verificaciones comparativas configurables.
- **Evidencias y trazabilidad:** logs por ejecución, métricas de tiempo y resultados.
- **Limpieza automática:** eliminación de BD sandbox al finalizar o ante cancelación controlada.
- **UI en tiempo real:** progreso, estados, consola y reportes.

### 4.3 Suposiciones y dependencias

**Suposiciones técnicas:**
- SQL Server está instalado y accesible.
- Existe ODBC Driver instalado (por ejemplo ODBC Driver 18 for SQL Server).
- El usuario cuenta con permisos suficientes (p. ej., sysadmin) para backup/restore.

**Dependencias técnicas:**
- Python 3.12+, `pyodbc`, `customtkinter`.
- Disponibilidad de rutas de almacenamiento accesibles por el servicio de SQL Server.

**Dependencias organizacionales/operativas:**
- Adopción por usuarios técnicos y disciplina de revisión de evidencias.
- Disponibilidad de almacenamiento y políticas de retención.

### 4.4 Costos y precios

En el contexto académico, el proyecto se desarrolla con herramientas de costo cero en licencias (SQL Server Developer, Python, GitHub). Los costos se asocian principalmente a esfuerzo humano y almacenamiento para respaldo. El retorno se expresa como ahorro de tiempo, reducción de riesgos y aumento de confiabilidad operativa.

### 4.5 Licenciamiento e instalación

- Distribución prevista como ejecutable `.exe` (por ejemplo, empaquetado con PyInstaller).
- Dependencia de driver ODBC instalado en el equipo cliente.
- Instalación simple: ejecutar instalador/portable, configurar conexión y rutas, y operar.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

## Características del producto

A continuación se detallan las características principales del sistema SQL-SafeBridge, organizadas en módulos:

**Módulo 1 — Autenticación y Control de Acceso (delegado a SQL Server):**
- Ingreso de credenciales SQL Server desde la app.
- Verificación de permisos/rol (p. ej., sysadmin) antes de habilitar funciones críticas.
- Bloqueo de funciones si no se cumplen permisos.

**Módulo 2 — Respaldo (Backup FULL):**
- Selección de base de datos objetivo.
- Definición de ruta de almacenamiento.
- Generación automática de nombre del archivo `.bak`.
- Captura de tiempo, tamaño y resultado.

**Módulo 3 — Restauración Sandbox (Restore Test):**
- Creación automática de base temporal con nombre controlado.
- Lectura de logical files (por ejemplo, `RESTORE FILELISTONLY`) para construir `WITH MOVE`.
- Restauración y verificación de accesibilidad.

**Módulo 4 — Validación de Integridad y Consistencia:**
- Ejecución de `DBCC CHECKDB` en la base restaurada.
- Validaciones comparativas básicas configurables (conteos, tablas críticas).
- Marcado del backup como “Validado” o “No Validado” según resultado.

**Módulo 5 — Evidencias y Auditoría:**
- Log técnico por ejecución (inicio/fin, pasos, errores, métricas).
- Exportación de evidencias para revisión.
- Historial local de ejecuciones (según implementación: archivo/DB local).

**Módulo 6 — Limpieza Automática:**
- DROP de base sandbox al finalizar validación (o ante falla controlada).
- Limpieza de archivos temporales si se generaron.

**Módulo 7 — Interfaz GUI profesional:**
- Consola de eventos en tiempo real.
- Barra de progreso por fase.
- Indicadores de estado: OK/ERROR/EN PROCESO.
- Configuración centralizada (servidor, credenciales, rutas, políticas básicas).

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

## Restricciones

- **Motor soportado:** SQL Server (enfocado en SQL Server 2022 Developer para el entorno del curso).
- **Sistema operativo recomendado:** Windows (por compatibilidad y tooling SQL Server).
- **Permisos:** se requiere un usuario con permisos suficientes para `BACKUP DATABASE`, `RESTORE DATABASE` y `DBCC CHECKDB` (idealmente `sysadmin` para simplificar en ámbito académico).
- **Almacenamiento:** se requiere espacio suficiente para backups y para restauración sandbox.
- **Rutas y permisos:** la ruta del backup debe ser accesible para el servicio de SQL Server (no solo para el usuario local).
- **Alcance académico:** funciones enterprise (SIEM, AD, multi-tenant, HA/DR multi-site) se consideran fuera de alcance.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

## Rangos de calidad

- **Confiabilidad:** un backup solo se considera “exitoso” si también pasa restore test + CHECKDB.
- **Trazabilidad:** cada ejecución debe generar evidencia (log) completa.
- **Usabilidad:** la UI debe permitir operar el flujo principal con pasos guiados.
- **Seguridad:** no persistir contraseñas en texto plano; minimizar exposición de credenciales.
- **Rendimiento:** tiempos de ejecución medidos y mostrados para estimar RTO real.
- **Mantenibilidad:** código desacoplado por capas (Clean Architecture) y con estándares (PEP 8).

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

## Precedencia y Prioridad

**Prioridad 1 — Crítica (Fase 1):**
- Conexión a SQL Server vía `pyodbc`.
- Verificación de permisos (sysadmin).
- Backup FULL con nomenclatura automática.
- Logging básico y UI mínima.

**Prioridad 2 — Alta (Fase 2):**
- Restore test en sandbox (FILELISTONLY + WITH MOVE).
- DBCC CHECKDB.
- Limpieza automática (DROP sandbox).
- UI con progreso y consola.

**Prioridad 3 — Media (Fase 3):**
- Validaciones comparativas configurables (conteos/tablas críticas).
- Reportes/Historial de ejecuciones.
- Políticas de retención y alertas de espacio (si el tiempo lo permite).

**Prioridad 4 — Baja (Futuro):**
- Diferenciales/log backups.
- Integraciones avanzadas y reportes enterprise.
- Exportación avanzada y dashboard histórico.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

## Otros requerimientos del producto

### Estándares Legales

En el contexto peruano, el sistema se alinea a la **Ley N.° 29733** (Protección de Datos Personales), especialmente en lo referente a confidencialidad y control de acceso a respaldos que puedan contener datos personales. Para fines académicos, se recomienda utilizar datos de prueba o anonimizar información al presentar demostraciones.

### Estándares de Comunicación

- Comunicación con SQL Server a través de `pyodbc` (ODBC/TDS).
- Recomendación: uso de cifrado en tránsito si la instancia lo soporta (TLS), según configuración de SQL Server y driver.

### Estándares de Calidad y Seguridad

- Validación de entradas (nombre de BD, rutas, parámetros).
- Protección contra SQL Injection mediante parámetros y evitando concatenación insegura.
- Logs sin exponer contraseñas.
- Manejo de errores robusto: capturar y reportar excepciones sin detener la app sin control.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

## CONCLUSIONES

SQL-SafeBridge propone una solución práctica y alineada con necesidades reales de continuidad de datos en SQL Server: no solo automatiza backups, sino que valida su recuperabilidad mediante restore test y `DBCC CHECKDB`, generando evidencia técnica verificable.

El proyecto mejora significativamente la confiabilidad operativa al transformar procesos manuales en un flujo orquestado, repetible y auditable, incrementando la confianza en los respaldos y permitiendo medir métricas reales para RTO/RPO.

El equipo responsable del proyecto (**Iker Alberto Sierra Ruiz** y **Julio Samuel Cortez Mamani**) asume el compromiso de implementar el sistema con enfoque de ingeniería de software, priorizando calidad, seguridad y mantenibilidad mediante Clean Architecture y documentación adecuada.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

## RECOMENDACIONES

- Ejecutar piloto con una base de datos de prueba antes de aplicar a entornos reales.
- Definir rutas y permisos de servicio SQL Server para evitar fallos típicos de backup/restore.
- Establecer una política mínima de retención y limpieza para evitar saturación de almacenamiento.
- Mantener evidencias por ejecución (logs) y revisarlas periódicamente.
- Incorporar pruebas automatizadas para los casos de uso principales (al menos pruebas de integración del flujo).

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

## BIBLIOGRAFIA

- IEEE. (1998). IEEE Std 830-1998: Recommended Practice for Software Requirements Specifications. Institute of Electrical and Electronics Engineers.
- Sommerville, I. (2015). Software Engineering (10th ed.). Pearson Education.
- ISO/IEC. (2022). ISO/IEC 27001:2022 – Information security management systems. International Organization for Standardization.
- Mullins, C. S. (2012). Database Administration: The Complete Guide to Practices and Procedures (2nd ed.). Addison-Wesley Professional.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

## WEBGRAFIA

- Microsoft SQL Server Official Documentation: https://learn.microsoft.com/en-us/sql/
- Microsoft SQL Server Backup/Restore: https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/
- Microsoft DBCC CHECKDB: https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkdb-transact-sql
- Python Official Documentation: https://docs.python.org/
- pyodbc Documentation: https://github.com/mkleehammer/pyodbc
- customtkinter Documentation: https://github.com/TomSchimansky/CustomTkinter
- GitHub: https://github.com

````