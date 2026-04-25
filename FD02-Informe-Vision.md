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
| 1.0 | IASR, JSCM | IASR, JSCM | PCQL | 28/03/2026 | Versión Original |

<div style="page-break-after: always; visibility: hidden"></div>

**Sistema: SQL-SafeBridge — Orquestador de Backups y Prueba de Restauración con Validación de Integridad (SQL Server)**

**Documento de Visión**

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
2. [Posicionamiento](#2-posicionamiento)
   - 2.1 Oportunidad de negocio
   - 2.2 Definición del problema
3. [Descripción de los Interesados y Usuarios](#3-descripción-de-los-interesados-y-usuarios)
   - 3.1 Resumen de los interesados
   - 3.2 Resumen de los usuarios
   - 3.3 Entorno de usuario
   - 3.4 Perfiles de los interesados
   - 3.5 Perfiles de los usuarios
   - 3.6 Necesidades de los interesados y usuarios
4. [Vista General del Producto](#4-vista-general-del-producto)
   - 4.1 Perspectiva del producto
   - 4.2 Resumen de capacidades
   - 4.3 Suposiciones y dependencias
   - 4.4 Costos y precios
   - 4.5 Licenciamiento e instalación
5. [Características del Producto](#5-características-del-producto)
6. [Restricciones](#6-restricciones)
7. [Rangos de Calidad](#7-rangos-de-calidad)
8. [Precedencia y Prioridad](#8-precedencia-y-prioridad)
9. [Otros Requerimientos del Producto](#9-otros-requerimientos-del-producto)
10. [GitHub Wiki — Estructura y Contenido](#10-github-wiki--estructura-y-contenido)
11. [Roadmap del Proyecto](#11-roadmap-del-proyecto)
- [Conclusiones](#conclusiones)
- [Recomendaciones](#recomendaciones)
- [Bibliografía](#bibliografía)
- [Webgrafía](#webgrafía)

<div style="page-break-after: always; visibility: hidden"></div>

---

## 1. Introducción

### 1.1 Propósito

El presente documento de visión establece los requisitos, características y restricciones del sistema **SQL-SafeBridge: Orquestador de Respaldos y Validación de Integridad (SQL Server)**. Su propósito principal es proporcionar una visión clara y compartida del proyecto a todos los interesados (docente, equipo de desarrollo, administradores de bases de datos, auditores internos y responsables de TI), sirviendo como base para el desarrollo del sistema y asegurando alineación respecto a objetivos, alcances, beneficios esperados y criterios de éxito.

Asimismo, este documento facilita la toma de decisiones estratégicas durante las fases posteriores del desarrollo, manteniendo consistencia con los requisitos técnicos y necesidades reales de continuidad de datos en entornos SQL Server.

### 1.2 Alcance

El alcance del proyecto comprende el desarrollo de una **aplicación de escritorio** orientada a entornos SQL Server (instancias locales o remotas) que automatiza el ciclo crítico de **Backup + Restore Test + Validación + Evidencia + Limpieza**, incluyendo:

- Generación de backups (**FULL**) con nomenclatura automática e inteligente (ej. `BD_YYYYMMDD_HHMMSS_FULL.bak`).
- Prueba de restauración automática en una base de datos **sandbox/espejo**, utilizando `WITH MOVE` para reubicar archivos físicos `.mdf` y `.ldf`.
- Auditoría técnica y validación de integridad mediante:
  - `DBCC CHECKDB` sobre la base restaurada.
  - Validaciones comparativas básicas (existencia de objetos críticos y conteos de registros según configuración).
- Registro de evidencias: archivos `.log` detallados, métricas de tiempo, resultados de cada paso y errores capturados.
- Actualización en tiempo real en la interfaz (consola de eventos y barras de progreso).
- Limpieza automática al finalizar (DROP de la base sandbox) para optimizar almacenamiento.
- Documentación técnica y colaborativa mantenida en la **GitHub Wiki** del repositorio.

**Tecnologías base dentro del alcance:**

- Python 3.12+ (orquestación).
- `customtkinter` (UI moderna).
- `pyodbc` + ODBC Driver (conectividad SQL Server vía TDS).
- Terraform v1.7+ (IaC para entorno de prueba en la nube).
- GitHub (repositorio, Actions CI/CD y Wiki).
- Patrones de diseño orientados a **Clean Architecture**.

**Fuera de alcance (para esta versión académica):**

- Soporte multi-motor (por ejemplo Oracle).
- Portal web / despliegue en nube como producto final.
- Recuperación granular de objetos individuales (object-level recovery) tipo enterprise.
- Integraciones corporativas avanzadas (SIEM, AD/LDAP, SMS, etc.), salvo que se simulen.

### 1.3 Definiciones, Siglas y Abreviaturas

| Término | Definición |
|---------|-----------|
| **Backup** | Copia de seguridad de una base de datos (en SQL Server, archivo `.bak`). |
| **Restore Test** | Restauración de prueba del backup en una BD sandbox para verificar recuperabilidad. |
| **Sandbox / Espejo** | Base de datos temporal restaurada desde el backup, separada de producción. |
| **RPO** | Recovery Point Objective — máximo período aceptable de pérdida de datos. |
| **RTO** | Recovery Time Objective — máximo tiempo aceptable para restablecer el servicio. |
| **DBCC CHECKDB** | Comando de SQL Server que valida consistencia lógica y física de una base de datos. |
| **TDS** | Tabular Data Stream — protocolo de comunicación usado por SQL Server. |
| **ODBC** | Open Database Connectivity — estándar para conectividad a bases de datos. |
| **GUI** | Interfaz gráfica de usuario. |
| **Clean Architecture** | Enfoque de arquitectura que separa UI, casos de uso, entidades e infraestructura. |
| **DBA** | Database Administrator — Administrador de Bases de Datos. |
| **Sysadmin** | Rol de servidor en SQL Server con privilegios administrativos máximos. |
| **IaC** | Infrastructure as Code — infraestructura definida y gestionada mediante código. |
| **Terraform** | Herramienta de IaC de HashiCorp para aprovisionar recursos en múltiples proveedores cloud. |
| **Wiki** | Conjunto de páginas colaborativas alojadas en GitHub para documentar el proyecto. |
| **Roadmap** | Plan visual de las fases, hitos y entregas del proyecto a lo largo del tiempo. |
| **CI/CD** | Continuous Integration / Continuous Deployment — prácticas de integración y entrega continua. |

### 1.4 Referencias

Los siguientes documentos y estándares son referencias relevantes para este proyecto:

- Microsoft SQL Server Documentation: Backup and Restore — https://learn.microsoft.com/en-us/sql/
- Microsoft SQL Server Documentation: DBCC CHECKDB — https://learn.microsoft.com/en-us/sql/
- HashiCorp Terraform Documentation — https://developer.hashicorp.com/terraform/docs
- ISO/IEC 27001:2022 — Information Security Management Systems (referencia de buenas prácticas).
- IEEE 830-1998 — Recommended Practice for Software Requirements Specifications.
- GitHub Docs: About Wikis — https://docs.github.com/en/communities/documenting-your-project-with-wikis
- Estándares de Ingeniería de Software de la Universidad Privada de Tacna.

### 1.5 Visión General

**SQL-SafeBridge** es una solución de escritorio diseñada para que la seguridad de los datos no dependa únicamente de "tener un backup", sino de contar con **evidencia automática de que dicho backup es restaurable y consistente**. La visión del sistema es convertir un proceso manual y propenso a errores (backup/restauración) en un flujo orquestado, repetible y auditable.

La herramienta busca brindar al DBA una estación de trabajo moderna que permita:

- Ejecutar respaldos con parámetros seguros y consistentes.
- Restaurar inmediatamente el backup en un entorno temporal.
- Verificar integridad con `DBCC CHECKDB` y validaciones adicionales.
- Registrar evidencias completas de lo sucedido (quién, cuándo, qué, resultado).
- Consultar la documentación del proyecto en la Wiki de GitHub de forma estructurada y actualizada.

<div style="page-break-after: always; visibility: hidden"></div>

---

## 2. Posicionamiento

### 2.1 Oportunidad de Negocio

En muchas organizaciones y entornos académicos, los respaldos aún se gestionan de manera manual en SSMS. En la práctica, esto genera dos problemas críticos: (1) ejecución irregular o no estandarizada, y (2) ausencia de pruebas de restauración, lo cual produce "backups de fe" (se asume que sirven, pero no se comprueba).

La oportunidad de valor de SQL-SafeBridge consiste en ofrecer una solución que reduzca el riesgo operativo mediante:

- Automatización del ciclo de continuidad (backup + restore test).
- Validación técnica inmediata (CHECKDB + pruebas básicas).
- Evidencia auditable con métricas reales de duración y resultados.
- Estándares de nomenclatura, retención y limpieza.

En el segmento objetivo (DBAs, equipos TI y entornos educativos con SQL Server), esta herramienta genera valor por reducción de errores, ahorro de tiempo operativo y mejora de cumplimiento y trazabilidad.

### 2.2 Definición del Problema

El problema central es la falta de verificación continua sobre la recuperabilidad real de los backups y la dependencia de procedimientos manuales.

En particular, se presentan las siguientes situaciones:

- **Backups generados sin prueba de restauración**, por lo que no existe certeza de que funcionarán en un incidente real.
- **Alta probabilidad de error humano** al escribir comandos T-SQL manualmente (rutas, nombres, opciones).
- **Escasa trazabilidad:** se desconoce quién ejecutó una operación, qué parámetros usó o cuál fue el resultado.
- **Falta de métricas reales:** no se mide el tiempo de backup y restore para estimar RTO.

SQL-SafeBridge resuelve esto mediante orquestación y validación automática con evidencias, elevando la confiabilidad del proceso.

<div style="page-break-after: always; visibility: hidden"></div>

---

## 3. Descripción de los Interesados y Usuarios

### 3.1 Resumen de los Interesados

| Interesado | Rol | Interés principal |
|-----------|-----|------------------|
| Administradores de Base de Datos (DBA) | Usuarios principales | Configuran, ejecutan y validan respaldos. |
| Equipo de TI / Soporte | Operativo | Necesita continuidad operativa y procedimientos repetibles. |
| Área de Auditoría / Control Interno | Supervisión | Requiere evidencia de operaciones y trazabilidad. |
| Docente y jurado académico | Evaluador | Evalúan documentación, ingeniería aplicada y cumplimiento del alcance. |
| Usuarios finales del sistema de información | Indirectos | Se benefician de mayor disponibilidad y menor riesgo de pérdida de datos. |

### 3.2 Resumen de los Usuarios

| Usuario | Descripción |
|---------|-------------|
| DBA Senior/Junior | Ejecutan backups, restore test y revisan reportes. |
| Analista de continuidad | Revisa evidencia y métricas históricas. |
| Auditor / Compliance | Revisa logs e historial (modo consulta). |

### 3.3 Entorno de Usuario

- Estaciones de trabajo con Windows (entorno recomendado por compatibilidad con SQL Server/SSMS).
- Conectividad a instancias SQL Server locales o remotas.
- Rutas de almacenamiento con permisos adecuados (NTFS/compartidos).
- Operación típica: ventanas de mantenimiento o ejecución en horarios programados.

### 3.4 Perfiles de los Interesados

**Perfil 1 — Responsable de TI / Infraestructura**
Requiere disminución de riesgos operativos y evidencia documental de continuidad de datos para cumplimiento interno.

**Perfil 2 — DBA**
Requiere automatización, control, seguridad y rapidez, con visibilidad del estado en tiempo real del proceso de backup/restore.

**Perfil 3 — Auditor / Control**
Requiere trazabilidad completa: quién ejecutó la operación, cuándo, qué parámetros se usaron y cuál fue el resultado obtenido.

### 3.5 Perfiles de los Usuarios

**Usuario Tipo 1 — DBA Senior**
Requiere flexibilidad (rutas, opciones, exclusiones, configuración avanzada). Domina SQL Server y valora la automatización con control total.

**Usuario Tipo 2 — DBA Junior**
Requiere guía paso a paso, UI clara, validaciones automáticas y mensajes de error comprensibles.

**Usuario Tipo 3 — Auditor / Docente (consulta)**
Requiere acceso a reportes, historial de ejecuciones y evidencias exportables, sin necesidad de operar la herramienta directamente.

### 3.6 Necesidades de los Interesados y Usuarios

| Necesidad | Prioridad | Solución propuesta |
|-----------|:---------:|-------------------|
| Automatizar ejecución y reducir errores manuales | Alta | Orquestación Python + T-SQL encapsulado |
| Garantizar que el backup sea restaurable | Alta | Restore Test automático en sandbox |
| Validar consistencia y mantener evidencia | Alta | DBCC CHECKDB + logs por ejecución |
| Minimizar impacto en producción | Media | Sandbox separado + limpieza automática |
| Control de acceso por rol | Media | Verificación de permisos vía SQL Server |
| Consultar documentación del proyecto | Media | GitHub Wiki estructurada y actualizada |

<div style="page-break-after: always; visibility: hidden"></div>

---

## 4. Vista General del Producto

### 4.1 Perspectiva del Producto

SQL-SafeBridge actúa como una capa de orquestación entre el DBA y SQL Server, sin reemplazar las capacidades nativas del motor; las utiliza y las hace seguras, repetibles y auditables.

**Arquitectura propuesta (alto nivel):**

```
┌─────────────────────────────────────────────────────────────┐
│                        UI Layer                             │
│            customtkinter — Consola, Progreso, Config        │
├─────────────────────────────────────────────────────────────┤
│                     Use Case Layer                          │
│    Backup → Restore Test → Validación → Evidencia → Limpieza│
├─────────────────────────────────────────────────────────────┤
│                  Infrastructure Layer                       │
│          pyodbc + T-SQL (BACKUP, RESTORE, DBCC)             │
├─────────────────────────────────────────────────────────────┤
│                     Entity Layer                            │
│        Modelos, Reportes, Estados, Eventos, Resultados      │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Resumen de Capacidades

| Capacidad | Descripción |
|-----------|-------------|
| Gestión de conexión segura | Credenciales ingresadas por el usuario; verificación de permisos (sysadmin). |
| Generación automática de backups FULL | Naming estándar (`BD_YYYYMMDD_HHMMSS_FULL.bak`) y parámetros seguros. |
| Restauración sandbox inmediata | Restauración del `.bak` en BD temporal con `WITH MOVE` para evitar conflictos. |
| Validación técnica | `DBCC CHECKDB` y verificaciones comparativas configurables. |
| Evidencias y trazabilidad | Logs por ejecución, métricas de tiempo y resultados. |
| Limpieza automática | Eliminación de BD sandbox al finalizar o ante cancelación controlada. |
| UI en tiempo real | Progreso, estados, consola de eventos y reportes visuales. |

### 4.3 Suposiciones y Dependencias

**Suposiciones técnicas:**

- SQL Server está instalado y accesible en la red local o remota.
- El ODBC Driver 18 for SQL Server está instalado en el equipo cliente.
- El usuario cuenta con permisos suficientes (`sysadmin`) para backup/restore.

**Dependencias técnicas:**

- Python 3.12+, `pyodbc`, `customtkinter`.
- Disponibilidad de rutas de almacenamiento accesibles por el servicio de SQL Server.
- Git + GitHub para versionado y colaboración.

**Dependencias organizacionales/operativas:**

- Adopción por usuarios técnicos y disciplina de revisión de evidencias.
- Disponibilidad de almacenamiento suficiente y políticas de retención definidas.

### 4.4 Costos y Precios

En el contexto académico, el proyecto se desarrolla con herramientas de costo cero en licencias (SQL Server Developer, Python, GitHub, Terraform CLI). Los costos se asocian principalmente a esfuerzo humano y almacenamiento para respaldo. El retorno se expresa como ahorro de tiempo, reducción de riesgos y aumento de confiabilidad operativa. Véase el análisis detallado en el Informe de Factibilidad (FD01).

### 4.5 Licenciamiento e Instalación

- Distribución prevista como ejecutable `.exe` (empaquetado con PyInstaller).
- Dependencia de ODBC Driver 18 instalado en el equipo cliente.
- Instalación simple: ejecutar instalador/portable, configurar conexión y rutas, y comenzar a operar.
- Código fuente publicado en GitHub bajo licencia **MIT**, con documentación en la Wiki del repositorio.

<div style="page-break-after: always; visibility: hidden"></div>

---

## 5. Características del Producto

A continuación se detallan las características principales del sistema SQL-SafeBridge, organizadas por módulo:

### Módulo 1 — Autenticación y Control de Acceso (delegado a SQL Server)

- Ingreso de credenciales SQL Server desde la aplicación.
- Verificación de permisos/rol (`sysadmin`) antes de habilitar funciones críticas.
- Bloqueo de funciones si no se cumplen los permisos requeridos.

### Módulo 2 — Respaldo (Backup FULL)

- Selección de base de datos objetivo.
- Definición de ruta de almacenamiento del archivo `.bak`.
- Generación automática de nombre del archivo con timestamp (`BD_YYYYMMDD_HHMMSS_FULL.bak`).
- Captura de tiempo de ejecución, tamaño del archivo y resultado de la operación.

### Módulo 3 — Restauración Sandbox (Restore Test)

- Creación automática de base temporal con nombre controlado y prefijo identificable.
- Lectura de logical files mediante `RESTORE FILELISTONLY` para construir cláusula `WITH MOVE`.
- Restauración del backup y verificación de accesibilidad de la BD resultante.

### Módulo 4 — Validación de Integridad y Consistencia

- Ejecución de `DBCC CHECKDB` sobre la base restaurada en el sandbox.
- Validaciones comparativas básicas configurables (conteos de registros, tablas críticas, existencia de objetos).
- Marcado del backup como **"Validado"** o **"No Validado"** según el resultado obtenido.

### Módulo 5 — Evidencias y Auditoría

- Log técnico por ejecución (inicio/fin, pasos individuales, errores, métricas de tiempo y tamaño).
- Exportación de evidencias para revisión externa.
- Historial local de ejecuciones (archivo de base de datos local o archivos `.log` nombrados por timestamp).

### Módulo 6 — Limpieza Automática

- DROP de base sandbox al finalizar la validación correctamente o ante falla controlada.
- Limpieza de archivos temporales generados durante el proceso.

### Módulo 7 — Interfaz GUI Profesional

- Consola de eventos en tiempo real con scroll y nivel de detalle configurable.
- Barra de progreso segmentada por fase (Backup / Restore / Validación / Limpieza).
- Indicadores de estado visuales: `✅ OK` / `❌ ERROR` / `🔄 EN PROCESO`.
- Panel de configuración centralizado (servidor, credenciales, rutas, políticas básicas de retención).

<div style="page-break-after: always; visibility: hidden"></div>

---

## 6. Restricciones

- **Motor soportado:** SQL Server (enfocado en SQL Server 2022 Developer para el entorno del curso).
- **Sistema operativo recomendado:** Windows (por compatibilidad y tooling SQL Server).
- **Permisos:** se requiere un usuario con permisos suficientes para `BACKUP DATABASE`, `RESTORE DATABASE` y `DBCC CHECKDB` (idealmente `sysadmin` para simplificar en ámbito académico).
- **Almacenamiento:** se requiere espacio suficiente para backups generados y para restauración sandbox.
- **Rutas y permisos:** la ruta del backup debe ser accesible para el servicio de SQL Server (no solo para el usuario del SO local).
- **Alcance académico:** funciones enterprise (SIEM, AD, multi-tenant, HA/DR multi-site) se consideran fuera de alcance en esta versión.

<div style="page-break-after: always; visibility: hidden"></div>

---

## 7. Rangos de Calidad

| Atributo | Criterio de Aceptación |
|----------|----------------------|
| **Confiabilidad** | Un backup solo se considera "exitoso" si también pasa restore test + DBCC CHECKDB sin errores. |
| **Trazabilidad** | Cada ejecución debe generar un log completo (inicio, pasos, tiempos, resultado, errores). |
| **Usabilidad** | La UI debe permitir operar el flujo principal en ≤5 acciones por parte del usuario. |
| **Seguridad** | No persistir contraseñas en texto plano; logs sin exponer credenciales. |
| **Rendimiento** | Tiempos de ejecución medidos y mostrados para estimar RTO real. |
| **Mantenibilidad** | Código desacoplado por capas (Clean Architecture) y con estándares PEP 8. Cobertura mínima de pruebas: 60 %. |

<div style="page-break-after: always; visibility: hidden"></div>

---

## 8. Precedencia y Prioridad

### Prioridad 1 — Crítica (Fase 1: semanas 1–4)

- Conexión a SQL Server vía `pyodbc`.
- Verificación de permisos (sysadmin).
- Backup FULL con nomenclatura automática.
- Logging básico y UI mínima funcional.

### Prioridad 2 — Alta (Fase 2: semanas 5–8)

- Restore test en sandbox (`RESTORE FILELISTONLY` + `WITH MOVE`).
- `DBCC CHECKDB` sobre la BD sandbox.
- Limpieza automática (DROP sandbox).
- UI con barra de progreso y consola de eventos.

### Prioridad 3 — Media (Fase 3: semanas 9–12)

- Validaciones comparativas configurables (conteos / tablas críticas).
- Reportes e historial de ejecuciones.
- Políticas de retención y alertas de espacio (si el tiempo lo permite).

### Prioridad 4 — Baja (Futuro / Fuera de alcance académico)

- Diferenciales y log backups.
- Integraciones avanzadas y reportes enterprise.
- Exportación avanzada y dashboard histórico.
- Soporte multi-motor (Oracle, PostgreSQL).

<div style="page-break-after: always; visibility: hidden"></div>

---

## 9. Otros Requerimientos del Producto

### Estándares Legales

En el contexto peruano, el sistema se alinea a la **Ley N.° 29733** (Protección de Datos Personales), especialmente en lo referente a confidencialidad y control de acceso a respaldos que puedan contener datos personales. Para fines académicos, se recomienda utilizar datos de prueba o anonimizar información al presentar demostraciones.

### Estándares de Comunicación

- Comunicación con SQL Server a través de `pyodbc` (ODBC/TDS).
- Recomendación: uso de cifrado en tránsito si la instancia lo soporta (TLS), según configuración del SQL Server y el driver ODBC 18.

### Estándares de Calidad y Seguridad

- Validación de entradas (nombre de BD, rutas, parámetros).
- Protección contra SQL Injection mediante parámetros y evitando concatenación insegura de cadenas T-SQL.
- Logs sin exponer contraseñas ni información sensible de conexión.
- Manejo de errores robusto: capturar y reportar excepciones sin detener la aplicación de forma descontrolada.

<div style="page-break-after: always; visibility: hidden"></div>

---

## 10. GitHub Wiki — Estructura y Contenido

La **GitHub Wiki** del repositorio de SQL-SafeBridge es el centro de documentación técnica y colaborativa del proyecto. Está diseñada para ser consultada tanto por el equipo de desarrollo como por evaluadores académicos y usuarios técnicos.

### 10.1 Propósito de la Wiki

La Wiki cumple tres objetivos principales:

1. **Centralizar la documentación técnica** del proyecto (arquitectura, módulos, instalación, uso).
2. **Servir como referencia** para contribuidores al proyecto (guías de configuración, convenciones de código).
3. **Facilitar la evaluación académica** proporcionando acceso estructurado a toda la información del sistema.

### 10.2 Estructura de Páginas de la Wiki

La Wiki se organiza en las siguientes páginas principales, accesibles desde la página de inicio (`Home`):

```
Wiki — SQL-SafeBridge
│
├── 🏠 Home (Inicio)
│     Descripción general, badges de estado (CI, licencia, versión)
│     y tabla de navegación rápida.
│
├── 📋 Descripción del Proyecto
│     Contexto, problema que resuelve, objetivos y alcance.
│
├── 🏛️ Arquitectura del Sistema
│     Diagrama de Clean Architecture, descripción de cada capa
│     (UI, Use Case, Infrastructure, Entity) y flujo de datos.
│
├── ⚙️ Instalación y Configuración
│     Prerrequisitos (Python 3.12+, ODBC Driver 18, SQL Server 2022)
│     Pasos de instalación paso a paso.
│     Configuración de cadena de conexión y rutas de backup.
│
├── 🚀 Guía de Uso
│     Flujo principal paso a paso con capturas de pantalla.
│     Ejecutar backup, restore test, validación y revisión de logs.
│
├── 🗄️ Módulos del Sistema
│     Descripción detallada de cada módulo:
│     Autenticación, Backup, Restore Sandbox, Validación,
│     Evidencias, Limpieza y GUI.
│
├── 🔧 Infraestructura con Terraform
│     Descripción del entorno cloud de prueba.
│     Comandos: terraform init / plan / apply / destroy.
│     Variables de configuración y archivo de estado.
│
├── 🧪 Pruebas
│     Estrategia de pruebas (unitarias, integración, sistema).
│     Cómo ejecutar el suite de pruebas localmente.
│     Resultados de pruebas clave.
│
├── 📊 Evidencias y Logs
│     Formato del archivo de log.
│     Ejemplo de log de ejecución exitosa y de ejecución con error.
│     Cómo interpretar los estados: Validado / No Validado.
│
├── 🤝 Guía de Contribución
│     Convenciones de ramas (main, develop, feature/*, fix/*).
│     Estándar de commits (Conventional Commits).
│     Proceso de Pull Request y revisión de código.
│
├── 🗺️ Roadmap
│     Fases, hitos y estado actual del proyecto.
│     Enlace a GitHub Projects para seguimiento detallado.
│
└── 📜 Licencia y Créditos
      Licencia MIT, autores, referencias y agradecimientos.
```

### 10.3 Página de Inicio (Home) — Contenido Recomendado

La página `Home` de la Wiki debe incluir:

```markdown
# SQL-SafeBridge 🛡️
> Orquestador de Respaldos y Validación de Integridad para SQL Server

![Build Status](https://github.com/usuario/sql-safebridge/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.12+](https://img.shields.io/badge/Python-3.12+-green.svg)
![SQL Server 2022](https://img.shields.io/badge/SQL%20Server-2022-red.svg)

## ¿Qué es SQL-SafeBridge?
SQL-SafeBridge automatiza el ciclo completo de continuidad de datos en SQL Server:
Backup → Restore Test → Validación (DBCC CHECKDB) → Evidencia → Limpieza.

## Navegación rápida
| Sección | Descripción |
|---------|-------------|
| [Instalación](./Instalación-y-Configuración) | Prerrequisitos y pasos de instalación |
| [Guía de Uso](./Guía-de-Uso) | Cómo operar el sistema |
| [Arquitectura](./Arquitectura-del-Sistema) | Diseño técnico del sistema |
| [Roadmap](./Roadmap) | Estado actual y próximas fases |
| [Terraform](./Infraestructura-con-Terraform) | Entorno cloud de prueba |
```

### 10.4 Convenciones de la Wiki

- **Nombre de páginas:** usar guiones para espacios (p. ej., `Guia-de-Uso`).
- **Formato:** Markdown estándar con tablas, bloques de código y encabezados jerárquicos.
- **Actualización:** cada Pull Request que afecte funcionalidad debe incluir actualización de la Wiki correspondiente.
- **Idioma:** español (castellano) como idioma principal, con términos técnicos en inglés donde corresponda.

<div style="page-break-after: always; visibility: hidden"></div>

---

## 11. Roadmap del Proyecto

El roadmap define las fases, hitos principales y entregables del proyecto SQL-SafeBridge a lo largo del ciclo académico 2026-I (marzo – julio 2026).

### 11.1 Visión General del Roadmap

```
MARZO 2026          ABRIL 2026          MAYO 2026           JUNIO 2026          JULIO 2026
│                   │                   │                   │                   │
▼                   ▼                   ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────┐
│   FASE 1      │   │   FASE 2      │   │   FASE 3      │   │   FASE 4      │   │  CIERRE   │
│  Fundamentos  │──▶│  Core Engine  │──▶│  Validación   │──▶│  Integración  │──▶│  y Entrega│
│               │   │               │   │  & Evidencias │   │  & Pulido     │   │           │
└───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘   └───────────┘
```

### 11.2 Detalle de Fases e Hitos

#### Fase 1 — Fundamentos (semanas 1–4: 10/03 – 04/04/2026)

| Hito | Descripción | Estado |
|------|-------------|:------:|
| 🏗️ Estructura del repositorio | Crear repo GitHub, configurar ramas (main/develop), CI básico con GitHub Actions | ✅ Completado |
| 📄 Documentación inicial | Informe de Factibilidad (FD01) y Documento de Visión (FD02) | ✅ Completado |
| 🔌 Conexión SQL Server | Módulo de conexión `pyodbc`, verificación de permisos `sysadmin` | ✅ Completado |
| 🖥️ UI esqueleto | Ventana principal con `customtkinter`, panel de configuración y consola de eventos básica | 🔄 En progreso |
| 🌍 Terraform base | Definición inicial de recursos cloud (`main.tf`, `variables.tf`, `outputs.tf`) | 🔄 En progreso |

#### Fase 2 — Core Engine (semanas 5–8: 07/04 – 02/05/2026)

| Hito | Descripción | Estado |
|------|-------------|:------:|
| 💾 Módulo Backup FULL | Ejecución de `BACKUP DATABASE` con naming automático, captura de métricas | ⏳ Pendiente |
| 🔄 Módulo Restore Sandbox | `RESTORE FILELISTONLY` + `RESTORE DATABASE ... WITH MOVE` a BD temporal | ⏳ Pendiente |
| 🧹 Limpieza automática | DROP de BD sandbox al finalizar; manejo de errores en limpieza | ⏳ Pendiente |
| 📊 Logging básico | Archivo `.log` por ejecución con timestamp, pasos y resultado | ⏳ Pendiente |
| 🎛️ UI Fase 2 | Barra de progreso por fase, actualización de estado en tiempo real | ⏳ Pendiente |

#### Fase 3 — Validación y Evidencias (semanas 9–12: 05/05 – 30/05/2026)

| Hito | Descripción | Estado |
|------|-------------|:------:|
| 🔍 DBCC CHECKDB | Ejecución de validación de integridad sobre la BD sandbox; captura de resultado | ⏳ Pendiente |
| 📋 Validaciones comparativas | Conteo de tablas/registros básico entre BD original y BD sandbox | ⏳ Pendiente |
| 🏷️ Marcado de estado | Marcar backup como "Validado" / "No Validado" con persistencia en historial local | ⏳ Pendiente |
| 📁 Exportación de evidencias | Generar reporte de ejecución exportable (`.txt` / `.log` estructurado) | ⏳ Pendiente |
| 🌍 Terraform validado | Entorno cloud funcional: VM + Storage; prueba end-to-end en cloud | ⏳ Pendiente |

#### Fase 4 — Integración y Pulido (semanas 13–15: 02/06 – 20/06/2026)

| Hito | Descripción | Estado |
|------|-------------|:------:|
| 🔗 Integración end-to-end | Flujo completo funcionando: Backup → Restore → CHECKDB → Evidencia → Limpieza | ⏳ Pendiente |
| 🧪 Suite de pruebas | Pruebas unitarias de módulos críticos y prueba de integración del flujo completo | ⏳ Pendiente |
| 🎨 UI pulida | Indicadores visuales de estado, tema oscuro, mensajes de error claros | ⏳ Pendiente |
| 📖 Wiki completa | Todas las páginas de la Wiki documentadas y actualizadas | ⏳ Pendiente |
| 📦 Empaquetado | Ejecutable `.exe` generado con PyInstaller | ⏳ Pendiente |

#### Cierre y Entrega (semanas 16–17: 23/06 – 04/07/2026)

| Entregable | Descripción |
|------------|-------------|
| 🎓 Informe final | Documentación completa del proyecto (FD01, FD02, FD03 y demás formatos requeridos) |
| 🎤 Presentación | Demo en vivo del sistema ante el docente/jurado |
| 💻 Código fuente | Repositorio GitHub con historial de commits limpio, Wiki completa y README |
| 📊 Evidencias | Logs de ejecución real del sistema durante las pruebas de validación |

### 11.3 Hitos Críticos (Milestones)

| Milestone | Fecha objetivo | Criterio de aceptación |
|-----------|:--------------:|----------------------|
| **M1** — Conexión y Backup funcionando | 02/04/2026 | Backup FULL generado correctamente, log creado. |
| **M2** — Restore Sandbox funcionando | 30/04/2026 | BD sandbox creada y accesible desde la app. |
| **M3** — Validación DBCC + Evidencias | 28/05/2026 | CHECKDB ejecutado, backup marcado como Validado/No Validado. |
| **M4** — Flujo completo integrado | 18/06/2026 | Ciclo end-to-end funcional en un solo clic desde la GUI. |
| **M5** — Entrega final | 04/07/2026 | Código, documentación y demo presentados al docente. |

### 11.4 Seguimiento del Roadmap en GitHub

El seguimiento detallado del roadmap se gestiona en el repositorio mediante:

- **GitHub Projects (Kanban):** tablero con columnas `Backlog` / `In Progress` / `In Review` / `Done`.
- **Issues:** cada hito se descompone en issues etiquetados (`feature`, `bug`, `docs`, `infra`).
- **Milestones:** los 5 milestones descritos están configurados en GitHub con fechas y descripción.
- **Pull Requests:** cada feature se desarrolla en rama propia y se integra vía PR con revisión cruzada.

> **Enlace al tablero:** `https://github.com/[usuario]/sql-safebridge/projects/1` *(actualizar con URL real del repositorio)*

<div style="page-break-after: always; visibility: hidden"></div>

---

## Conclusiones

SQL-SafeBridge propone una solución práctica y alineada con necesidades reales de continuidad de datos en SQL Server: no solo automatiza backups, sino que valida su recuperabilidad mediante restore test y `DBCC CHECKDB`, generando evidencia técnica verificable.

El proyecto mejora significativamente la confiabilidad operativa al transformar procesos manuales en un flujo orquestado, repetible y auditable, incrementando la confianza en los respaldos y permitiendo medir métricas reales para RTO/RPO.

La incorporación de una **GitHub Wiki estructurada** y un **Roadmap detallado** garantizan transparencia en el proceso de desarrollo, facilitan la evaluación académica y sirven como referencia de buenas prácticas de gestión de proyectos de software.

El equipo responsable del proyecto (**Iker Alberto Sierra Ruiz** y **Julio Samuel Cortez Mamani**) asume el compromiso de implementar el sistema con enfoque de ingeniería de software, priorizando calidad, seguridad y mantenibilidad mediante Clean Architecture, documentación continua y gestión ágil en GitHub.

---

## Recomendaciones

- Ejecutar piloto con una base de datos de prueba antes de aplicar a entornos reales.
- Definir rutas y permisos del servicio SQL Server para evitar fallos típicos de backup/restore.
- Establecer una política mínima de retención y limpieza para evitar saturación de almacenamiento.
- Mantener la Wiki de GitHub actualizada con cada entrega o cambio significativo en el sistema.
- Revisar periódicamente el roadmap en GitHub Projects y actualizar el estado de los hitos.
- Incorporar pruebas automatizadas para los casos de uso principales (al menos pruebas de integración del flujo completo).
- Ejecutar `terraform destroy` al finalizar cada sesión de pruebas en la nube para evitar costos innecesarios.

---

## Bibliografía

- IEEE. (1998). *IEEE Std 830-1998: Recommended Practice for Software Requirements Specifications*. Institute of Electrical and Electronics Engineers.
- Sommerville, I. (2015). *Software Engineering* (10th ed.). Pearson Education.
- ISO/IEC. (2022). *ISO/IEC 27001:2022 – Information security management systems*. International Organization for Standardization.
- Mullins, C. S. (2012). *Database Administration: The Complete Guide to Practices and Procedures* (2nd ed.). Addison-Wesley Professional.
- Martin, R. C. (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.

---

## Webgrafía

- Microsoft SQL Server Documentation: https://learn.microsoft.com/en-us/sql/
- Microsoft SQL Server Backup/Restore: https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/
- Microsoft DBCC CHECKDB: https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkdb-transact-sql
- HashiCorp Terraform Documentation: https://developer.hashicorp.com/terraform/docs
- GitHub Docs — About Wikis: https://docs.github.com/en/communities/documenting-your-project-with-wikis
- GitHub Docs — About Project Boards: https://docs.github.com/en/issues/planning-and-tracking-with-projects
- Python Official Documentation: https://docs.python.org/
- pyodbc Documentation: https://github.com/mkleehammer/pyodbc
- customtkinter Documentation: https://github.com/TomSchimansky/CustomTkinter

---

*Documento elaborado por: Iker Alberto Sierra Ruiz (2023077090) y Julio Samuel Cortez Mamani (2023077283) — Universidad Privada de Tacna, Facultad de Ingeniería, Escuela Profesional de Ingeniería de Sistemas — Tacna, Perú, 2026.*
