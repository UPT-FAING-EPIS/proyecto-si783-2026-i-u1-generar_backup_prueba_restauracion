<center>

![./media/logo-upt.png](./media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERÍA**

**Escuela Profesional de Ingeniería de Sistemas**

**Proyecto: *SQL-SafeBridge: Orquestador de Respaldos y Validación de Integridad (SQL Server)***

Curso: *Base de Datos II*

Docente: *Ing. Patrick José Cuadros Quiroga*

Integrantes:

***Sierra Ruiz, Iker Alberto (2023077090)***

***Cortez Mamani, Julio Samuel (2023077283)***

**Tacna – Perú**

***2026***

</center>

<div style="page-break-after: always; visibility: hidden"></div>

**Sistema: *SQL-SafeBridge: Orquestador de Respaldos y Validación de Integridad (SQL Server)***

**Documento FD04: Diagramas del Sistema — Reverse Engineering**

**Versión *1.0***

| CONTROL DE VERSIONES | | | | | |
|:---:|---|---|---|---|---|
| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
| 1.0 | IASR / JSCM | Ing. P. Cuadros | Ing. P. Cuadros | 30/04/2026 | Versión Original |

<div style="page-break-after: always; visibility: hidden"></div>

---

# ÍNDICE GENERAL

1. [Introducción](#1-introducción)
2. [Diagrama de Clases](#2-diagrama-de-clases)
3. [Diagrama de Base de Datos](#3-diagrama-de-base-de-datos)
4. [Diagrama de Componentes](#4-diagrama-de-componentes)
5. [Diagrama de Despliegue](#5-diagrama-de-despliegue)
6. [Diagrama de Arquitectura](#6-diagrama-de-arquitectura)
7. [Diagrama de Infraestructura (Terraform)](#7-diagrama-de-infraestructura-terraform)

<div style="page-break-after: always; visibility: hidden"></div>

---

## 1. Introducción

### 1.1 Propósito

El presente documento contiene los **diagramas del sistema SQL-SafeBridge** obtenidos mediante **reverse engineering** del código fuente implementado. Se incluyen:

- **Diagrama de Clases:** derivado de la estructura real de archivos y herencia en Python
- **Diagrama de Base de Datos:** modelo de las bases de datos involucradas en el sistema
- **Diagrama de Componentes:** organización modular y dependencias entre componentes
- **Diagrama de Despliegue:** distribución física del sistema en nodos
- **Diagrama de Arquitectura:** vista de alto nivel de las capas y flujo de datos
- **Diagrama de Infraestructura:** recursos cloud definidos con Terraform

### 1.2 Metodología

Los diagramas se obtuvieron analizando directamente el código fuente del repositorio, respetando la estructura real de archivos, clases y dependencias. Se utilizó notación **UML 2.0** para los diagramas de clases, componentes y despliegue, y notación **C4 Model** para el diagrama de arquitectura.

### 1.3 Estructura Real del Código
sql-safebridge/
├── main.py
├── requirements.txt
├── README.md
├── presentation/
│ ├── app_controller.py
│ ├── login_screen.py
│ ├── dashboard_screen.py
│ └── dialogs.py
├── application/
│ ├── orchestrator.py
│ ├── backup_use_case.py
│ ├── restore_use_case.py
│ ├── restore_backup_use_case.py
│ └── validation_use_case.py
├── domain/
│ ├── entities.py
│ └── interfaces.py
├── infrastructure/
│ └── sql_server_repository.py
├── shared/
│ ├── config.py
│ └── logger.py
└── logs/
└── restore_backup_*.log / .json

<div style="page-break-after: always; visibility: hidden"></div>

---

## 2. Diagrama de Clases

### 2.1 Descripción

El diagrama de clases representa las entidades, interfaces y relaciones del sistema siguiendo **Clean Architecture**. Las dependencias fluyen de las capas externas (Presentation, Infrastructure) hacia las capas internas (Domain).

### 2.2 Diagrama

```mermaid
classDiagram
    %% ===== DOMAIN LAYER =====
    class DatabaseRepository {
        <<interface>>
        +connect(server, user, password) bool
        +is_sysadmin() bool
        +get_databases() list
        +execute_backup(db, path) BackupResult
        +execute_restore(filelistonly) FileList
        +execute_restore_with_move(backup, sandbox, moves) RestoreResult
        +execute_checkdb(db) ValidationResult
        +execute_drop(db) bool
    }

    class BackupResult {
        +bool success
        +str file_path
        +str file_name
        +float size_mb
        +float duration_seconds
        +str error_message
    }

    class RestoreResult {
        +bool success
        +str sandbox_db
        +float duration_seconds
        +str error_message
    }

    class ValidationResult {
        +bool success
        +bool is_valid
        +str checkdb_output
        +float duration_seconds
        +str error_message
    }

    class ExecutionResult {
        +BackupResult backup
        +RestoreResult restore
        +ValidationResult validation
        +str final_status
        +float total_duration
        +datetime timestamp
    }

    class Event {
        +str step_name
        +str status
        +str message
        +float duration
    }

    DatabaseRepository <|.. SQLServerRepository

    %% ===== INFRASTRUCTURE LAYER =====
    class SQLServerRepository {
        -str connection_string
        -Connection conn
        +connect(server, user, password) bool
        +is_sysadmin() bool
        +get_databases() list
        +execute_backup(db, path) BackupResult
        +execute_restore(filelistonly) FileList
        +execute_restore_with_move(backup, sandbox, moves) RestoreResult
        +execute_checkdb(db) ValidationResult
        +execute_drop(db) bool
    }

    %% ===== APPLICATION LAYER =====
    class Orchestrator {
        -DatabaseRepository repository
        -Logger logger
        +execute_full_cycle(db, backup_path, sandbox_path) ExecutionResult
        -_execute_backup(db, path) BackupResult
        -_execute_restore(backup, sandbox) RestoreResult
        -_execute_validation(sandbox) ValidationResult
        -_execute_cleanup(sandbox) bool
    }

    class BackupUseCase {
        -DatabaseRepository repository
        +execute(db, path) BackupResult
    }

    class RestoreUseCase {
        +get_file_list(repository, backup_path) FileList
    }

    class RestoreBackupUseCase {
        -DatabaseRepository repository
        +execute(backup_path, sandbox_name, data_path, log_path) RestoreResult
    }

    class ValidationUseCase {
        -DatabaseRepository repository
        +execute(db_name) ValidationResult
    }

    Orchestrator --> DatabaseRepository
    Orchestrator --> Logger
    BackupUseCase --> DatabaseRepository
    RestoreBackupUseCase --> DatabaseRepository
    ValidationUseCase --> DatabaseRepository

    %% ===== PRESENTATION LAYER =====
    class AppController {
        -DatabaseRepository repository
        -LoginScreen login_screen
        -DashboardScreen dashboard
        +show_login()
        +show_dashboard()
        +on_login_success()
    }

    class LoginScreen {
        -AppController controller
        -CTkEntry server_entry
        -CTkEntry user_entry
        -CTkEntry password_entry
        -CTkButton connect_button
        +on_connect_click()
    }

    class DashboardScreen {
        -AppController controller
        -Orchestrator orchestrator
        -CTkComboBox db_selector
        -CTkButton backup_button
        -CTkButton validate_button
        -CTkButton config_button
        -CTkTextbox console
        -CTkProgressBar progress
        +on_backup_click()
        +on_validate_click()
        +update_progress(step, total)
        +append_console(message)
    }

    class ConfigDialog {
        -CTkEntry backup_path_entry
        -CTkEntry sandbox_path_entry
        -CTkButton save_button
        +on_save_click()
    }

    AppController --> LoginScreen
    AppController --> DashboardScreen
    DashboardScreen --> Orchestrator
    DashboardScreen --> ConfigDialog

    %% ===== SHARED KERNEL =====
    class Logger {
        +log_info(message)
        +log_error(message)
        +log_warning(message)
        +save_execution_result(result) bool
        -_write_log(message, level)
        -_write_json(data)
    }

    class Config {
        +str backup_path
        +str sandbox_path
        +int connection_timeout
        +load() dict
        +save(config) bool
    }
### 2.3 Explicación de Relaciones

Relación	Tipo	Descripción
SQLServerRepository → DatabaseRepository	Realización	Implementa la interfaz del repositorio
Orchestrator → DatabaseRepository	Dependencia	Usa el repositorio vía inyección
BackupUseCase → DatabaseRepository	Dependencia	Llama al repositorio para ejecutar backup
AppController → LoginScreen, DashboardScreen	Composición	Controla el ciclo de vida de las pantallas
DashboardScreen → Orchestrator	Dependencia	Invoca la orquestación del flujo
Orchestrator → Logger	Dependencia	Registra eventos y resultados

### 2.4 Principios SOLID Aplicados
Principio	Aplicación
S (Responsabilidad Única)	Cada Use Case tiene una sola responsabilidad
O (Abierto/Cerrado)	Nuevos casos de uso se agregan sin modificar el Orchestrator
L (Sustitución de Liskov)	Cualquier implementación de DatabaseRepository funciona
I (Segregación de Interfaces)	DatabaseRepository expone solo métodos necesarios
D (Inversión de Dependencias)	Capas superiores dependen de abstracciones, no de implementaciones
<div style="page-break-after: always; visibility: hidden"></div>

## 3. Diagrama de Base de Datos

###3.1 Descripción

SQL-SafeBridge no utiliza una base de datos propia para persistencia. Interactúa directamente con SQL Server para ejecutar operaciones sobre las bases de datos existentes. Las evidencias se almacenan en archivos .log y .json.
erDiagram
    SQL_SERVER_INSTANCE {
        string instance_name
        string version
        string edition
    }
    
    USER_DATABASE {
        string database_name
        int size_mb
        string state
        datetime last_backup
    }
    
    BACKUP_FILE {
        string file_name
        string file_path
        float size_mb
        datetime created_at
        string type "FULL"
    }
    
    SANDBOX_DATABASE {
        string database_name
        string status "temporal"
        datetime created_at
        datetime destroyed_at
    }
    
    EXECUTION_LOG {
        string file_name_log
        string file_name_json
        datetime timestamp
        string final_status
        float total_duration_seconds
    }
    
    SQL_SERVER_INSTANCE ||--o{ USER_DATABASE : "contiene"
    USER_DATABASE ||--o{ BACKUP_FILE : "genera"
    BACKUP_FILE ||--o| SANDBOX_DATABASE : "restaura en"
    BACKUP_FILE ||--o{ EXECUTION_LOG : "registrado en"

## 3.3 Entidades

Entidad	Descripción	Persistencia
SQL Server Instance	Instancia de SQL Server donde se ejecutan las operaciones	SQL Server
User Database	Bases de datos existentes en la instancia	SQL Server
Backup File	Archivo .bak generado por el sistema	Sistema de archivos
Sandbox Database	BD temporal restaurada para validación	SQL Server (efímera)
Execution Log	Evidencias en .log y .json	Sistema de archivos (logs/)

## 3.4 Ciclo de Vida de la Base Sandbox

CREACIÓN                     VALIDACIÓN                    DESTRUCCIÓN
   │                             │                              │
   ▼                             ▼                              ▼
┌─────────┐   RESTORE    ┌─────────────┐   DBCC     ┌─────────────┐   DROP    ┌─────────┐
│ Backup  │──────────────▶│ Sandbox DB  │───────────▶│ CHECKDB OK  │──────────▶│ Limpio  │
│  .bak   │               │ _Sandbox    │            │ / ERROR     │           │         │
└─────────┘               └─────────────┘            └─────────────┘           └─────────┘
<div style="page-break-after: always; visibility: hidden"></div>

## 4. Diagrama de Componentes

### 4.1 Descripción

El diagrama de componentes muestra la organización modular del sistema y las dependencias entre paquetes, reflejando la estructura real del código.

### 4.2 Diagrama

graph TB
    subgraph "Presentation Layer"
        AC[AppController<br/>app_controller.py]
        LS[LoginScreen<br/>login_screen.py]
        DS[DashboardScreen<br/>dashboard_screen.py]
        DL[ConfigDialog<br/>dialogs.py]
    end

    subgraph "Application Layer"
        ORCH[Orchestrator<br/>orchestrator.py]
        BUC[BackupUseCase<br/>backup_use_case.py]
        RUC[RestoreUseCase<br/>restore_use_case.py]
        RBUC[RestoreBackupUseCase<br/>restore_backup_use_case.py]
        VUC[ValidationUseCase<br/>validation_use_case.py]
    end

    subgraph "Domain Layer"
        ENT[Entities<br/>entities.py]
        INT[Interfaces<br/>interfaces.py]
    end

    subgraph "Infrastructure Layer"
        REPO[SQLServerRepository<br/>sql_server_repository.py]
    end

    subgraph "Shared Kernel"
        LOG[Logger<br/>logger.py]
        CFG[Config<br/>config.py]
    end

    subgraph "External"
        SQL[(SQL Server)]
        FS[File System<br/>logs/ + backups/]
    end

    %% Dependencias
    AC --> LS
    AC --> DS
    DS --> DL
    DS --> ORCH
    ORCH --> BUC
    ORCH --> RBUC
    ORCH --> VUC
    ORCH --> LOG
    BUC --> INT
    RBUC --> INT
    RBUC --> RUC
    VUC --> INT
    INT -.-> REPO
    REPO --> SQL
    LOG --> FS
    BUC --> FS

### 4.3 Dependencias entre Componentes

Origen	Destino	Tipo	Descripción
AppController	LoginScreen	Composición	Crea y destruye la pantalla de login
AppController	DashboardScreen	Composición	Crea y destruye el dashboard
DashboardScreen	Orchestrator	Uso	Invoca la orquestación del flujo
DashboardScreen	ConfigDialog	Uso	Abre diálogo de configuración
Orchestrator	BackupUseCase	Uso	Delega la operación de backup
Orchestrator	RestoreBackupUseCase	Uso	Delega la operación de restore
Orchestrator	ValidationUseCase	Uso	Delega la operación de validación
Orchestrator	Logger	Uso	Registra eventos y resultados
BackupUseCase	Interfaces	Dependencia	Depende de la abstracción
SQLServerRepository	Interfaces	Implementación	Implementa la interfaz
SQLServerRepository	SQL Server	Conexión	pyodbc / TDS
Logger	File System	Escritura	Genera archivos .log y .json
<div style="page-break-after: always; visibility: hidden"></div>

## 5. Diagrama de Despliegue

### 5.1 Descripción

El diagrama de despliegue muestra la distribución física del sistema en nodos de hardware y software, incluyendo el entorno de desarrollo y el entorno cloud de prueba provisionado con Terraform.

### 5.2 Diagrama

graph TB
    subgraph "Estación de Trabajo (Windows 10/11)"
        subgraph "Aplicación Python"
            MAIN[main.py<br/>Python 3.12+]
            GUI[customtkinter GUI]
        end
        
        subgraph "Dependencias"
            ODBC[ODBC Driver 18]
            PYODBC[pyodbc library]
        end
        
        FS_Local[File System<br/>C:\Backups\<br/>C:\Sandbox\<br/>logs/]
    end

    subgraph "Servidor SQL Server (Local/Remoto)"
        SQLENGINE[SQL Server 2022<br/>Developer Edition]
        USERDB[(User Databases)]
        SANDBOX[(Sandbox DB<br/>Temporal)]
    end

    subgraph "Azure Cloud (Terraform)"
        subgraph "Resource Group"
            VM[VM Standard_B2s<br/>2 vCPU, 4 GB RAM]
            STORAGE[Storage Account<br/>Standard LRS]
        end
    end

    subgraph "GitHub"
        REPO[Repositorio<br/>sql-safebridge]
        WIKI[Wiki]
        ACTIONS[GitHub Actions]
    end

    MAIN --> GUI
    MAIN --> PYODBC
    PYODBC --> ODBC
    ODBC -->|TDS :1433| SQLENGINE
    SQLENGINE --> USERDB
    SQLENGINE --> SANDBOX
    MAIN --> FS_Local
    REPO --> ACTIONS
    MAIN -.->|git push/pull| REPO

### 5.3 Nodos del Sistema

Nodo	Tipo	Componentes	Descripción
Estación de Trabajo	Hardware	Laptop/PC del desarrollador	Windows 10/11, 8 GB RAM mínimo
Aplicación Python	Software	main.py + 4 capas Clean Architecture	Python 3.12+, customtkinter
ODBC Driver	Software	ODBC Driver 18 for SQL Server	Comunicación TDS con SQL Server
SQL Server	Software	SQL Server 2022 Developer Edition	Motor de base de datos
Azure Cloud	Cloud	VM + Storage Account	Entorno de prueba con Terraform
GitHub	Cloud	Repositorio + Wiki + Actions	Control de versiones y CI/CD

### 5.4 Protocolos de Comunicación

Conexión	Protocolo	Puerto
Python → SQL Server	TDS (Tabular Data Stream) vía ODBC	1433
Python → Sistema de Archivos	Operaciones de E/S nativas	—
Git → GitHub	HTTPS / SSH	443 / 22
Terraform → Azure	Azure Resource Manager API	443
<div style="page-break-after: always; visibility: hidden"></div>

## 6. Diagrama de Arquitectura

### 6.1 Descripción

El diagrama de arquitectura utiliza el modelo C4 (Context, Container, Component) para mostrar una vista de alto nivel del sistema, sus usuarios y sistemas externos.

### 6.2 Diagrama de Contexto (Nivel 1)

graph TB
    DBA[👤 DBA<br/>Administrador de BD]
    AUDITOR[👤 Auditor<br/>Control Interno]
    
    subgraph "SQL-SafeBridge"
        SISTEMA[Sistema de Orquestación<br/>de Backups y Validación]
    end
    
    SQL[(SQL Server<br/>Motor de BD)]
    FS[📁 Sistema de Archivos<br/>Backups + Logs]
    AZURE[☁️ Azure Cloud<br/>Terraform IaC]
    
    DBA -->|"Ejecuta backup + validación"| SISTEMA
    AUDITOR -->|"Consulta evidencias y logs"| SISTEMA
    SISTEMA -->|"BACKUP/RESTORE/CHECKDB"| SQL
    SISTEMA -->|"Guarda .bak, .log, .json"| FS
    SISTEMA -.->|"terraform apply/destroy"| AZURE

### 6.3 Diagrama de Contenedores (Nivel 2)

graph TB
    DBA[👤 DBA]
    AUDITOR[👤 Auditor]
    
    subgraph "SQL-SafeBridge"
        GUI[🧩 GUI<br/>customtkinter<br/>Presentation Layer]
        ORCH[⚙️ Orchestrator<br/>Application Layer]
        DOMAIN[🧠 Domain<br/>Entities + Interfaces]
        INFRA[🔌 Infrastructure<br/>SQLServerRepository]
        SHARED[🛠️ Shared Kernel<br/>Logger + Config]
    end
    
    SQL[(SQL Server)]
    FS[📁 File System]
    
    DBA --> GUI
    AUDITOR --> GUI
    GUI --> ORCH
    ORCH --> DOMAIN
    DOMAIN --> INFRA
    INFRA --> SQL
    ORCH --> SHARED
    SHARED --> FS
    GUI --> SHARED

### 6.4 Flujo de Datos Principal

┌──────────┐     ┌──────────────┐     ┌──────────────┐     ┌────────────┐
│  Usuario │────▶│  Dashboard   │────▶│ Orchestrator │────▶│ SQL Server │
│   (DBA)  │     │  (GUI)       │     │  (Flujo)     │     │  (Motor)   │
└──────────┘     └──────────────┘     └──────────────┘     └────────────┘
                      │                      │                     │
                      │ Consola de           │ Logger              │ BACKUP
                      │ eventos              │                     │ RESTORE
                      ▼                      ▼                     │ CHECKDB
               ┌──────────────┐     ┌──────────────┐              │
               │  Resultados  │     │  logs/       │◀─────────────┘
               │  en pantalla │     │  .log + .json│
               └──────────────┘     └──────────────┘

<div style="page-break-after: always; visibility: hidden"></div>

## 7. Diagrama de Infraestructura (Terraform)

### 7.1 Descripción

El diagrama de infraestructura muestra los recursos cloud definidos mediante Terraform para el entorno de prueba del sistema. Estos recursos se gestionan como código en infraestructura/main.tf.

### 7.2 Diagrama

graph TB
    subgraph "Azure Cloud - East US"
        subgraph "Resource Group: rg-sqlsafebridge-tacna"
            SQLSRV[azurerm_mssql_server<br/>sql-sandbox-safebridge<br/>Version 12.0<br/>Serverless Gen5]
            STORAGE[azurerm_storage_account<br/>stsqlsafebridgebackups<br/>Standard LRS<br/>Hot Tier 50 GB]
            RG[azurerm_resource_group<br/>rg-sqlsafebridge-tacna<br/>Contenedor lógico]
        end
    end

    subgraph "Estación de Trabajo"
        TF[Terraform CLI v1.7+<br/>main.tf]
        APP[SQL-SafeBridge App]
    end

    TF -->|"terraform apply"| RG
    RG --> SQLSRV
    RG --> STORAGE
    APP -.->|"Conexión TDS :1433"| SQLSRV
    APP -->|"Guarda .bak"| STORAGE

### 7.3 Recursos Terraform

Recurso	Tipo Azure	SKU / Configuración	Propósito
azurerm_resource_group	Resource Group	rg-sqlsafebridge-tacna	Contenedor lógico de todos los recursos
azurerm_mssql_server	SQL Server	Serverless Gen5, 0.5 vCore min	Entorno sandbox para restore test
azurerm_storage_account	Storage Account	Standard LRS, Hot Tier, 50 GB	Repositorio de archivos .bak

### 7.4 Código Terraform de Referencia

# main.tf - Definición de Infraestructura para SQL-SafeBridge

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg_safebridge" {
  name     = "rg-sqlsafebridge-tacna"
  location = "East US"
}

resource "azurerm_storage_account" "st_backups" {
  name                     = "stsqlsafebridgebackups"
  resource_group_name      = azurerm_resource_group.rg_safebridge.name
  location                 = azurerm_resource_group.rg_safebridge.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_mssql_server" "sql_sandbox" {
  name                         = "sql-sandbox-safebridge"
  resource_group_name          = azurerm_resource_group.rg_safebridge.name
  location                     = azurerm_resource_group.rg_safebridge.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "PasswordSeguro123!"
}

### 7.5 Ciclo de Vida de la Infraestructura

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ terraform    │────▶│ terraform    │────▶│ terraform    │
│ init         │     │ plan         │     │ apply        │
│ (1 vez)      │     │ (validar)    │     │ (desplegar)  │
└──────────────┘     └──────────────┘     └──────────────┘
                                                 │
                                                 ▼
                                          ┌──────────────┐
                                          │ Recursos     │
                                          │ Azure        │
                                          │ desplegados  │
                                          └──────────────┘
                                                 │
                    ┌────────────────────────────┘
                    ▼
             ┌──────────────┐
             │ terraform    │
             │ destroy      │
             │ (limpiar)    │
             └──────────────┘

### 7.6 Costos Mensuales Estimados

Recurso	Costo Mensual (S/)
azurerm_mssql_server (Serverless)	S/ 25.50
azurerm_storage_account (50 GB)	S/ 8.40
azurerm_resource_group	S/ 0.00
Total	S/ 33.90
Tipo de cambio: 1 USD = S/ 3.75. Costos minimizados con modelos serverless y LRS.

Resumen de Diagramas
Diagrama	Tipo	Vista
Clases	UML Estructural	Entidades, interfaces, relaciones de herencia y dependencia
Base de Datos	UML / ER	Entidades de datos y su ciclo de vida
Componentes	UML Estructural	Paquetes, módulos y dependencias entre ellos
Despliegue	UML Físico	Nodos de hardware/software y protocolos
Arquitectura	C4 Model	Contexto, contenedores y flujo de datos
Infraestructura	Cloud / IaC	Recursos Azure definidos en Terraform
Documento elaborado por: Iker Alberto Sierra Ruiz (2023077090) y Julio Samuel Cortez Mamani (2023077283) — Universidad Privada de Tacna, Facultad de Ingeniería, Escuela Profesional de Ingeniería de Sistemas — Tacna, Perú, Abril 2026.


---

## ✅ INSTRUCCIONES FINALES

1. **Guarda el archivo** como `FD04-Diagramas-Reverse-Engineering.md`

2. **Los diagramas Mermaid** se renderizan automáticamente en GitHub. Para el PDF necesitas convertirlos a imágenes:
   - Ve a https://mermaid.live
   - Pega cada bloque de código Mermaid
   - Exporta como PNG
   - Reemplaza los bloques ```mermaid por las imágenes

3. **Genera el PDF:**
   ```bash
   pandoc FD04-Diagramas-Reverse-Engineering.md -o FD04-Diagramas-Reverse-Engineering.pdf --pdf-engine=xelatex
   