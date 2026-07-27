# EVM Project Tracker

Herramienta interna para líderes de proyecto: registrar el avance de actividades y evaluar en tiempo real el estado de cronograma y presupuesto con la metodología de **Valor Ganado (Earned Value Management — EVM)**.

## Estado del proyecto

Actualizar esta lista en cada PR para que el README de `main` siempre refleje el estado real de la entrega.

**Completado**

- [x] Esqueleto del backend (capas, `pyproject.toml`, ruff, app mínima con Swagger en `/docs`)
- [x] Modelos SQLAlchemy (`Project`, `Activity`) con relación 1—N y `ON DELETE CASCADE`
- [x] Constraints de validación en BD (`bac > 0`, `ac >= 0`, porcentajes 0–100)
- [x] Alembic inicializado + migración inicial aplicada y verificada contra Postgres local

**Pendiente**

- [ ] Capa de servicio EVM (cálculo de indicadores + interpretación)
- [ ] Repositories, schemas Pydantic y endpoints CRUD
- [ ] Tests unitarios (services) e integración (endpoints), cobertura ≥80%
- [ ] Frontend Angular (dashboard, semáforo CPI/SPI, gráfica PV/EV/AC)
- [ ] OpenAPI documentado por endpoint + video + cierre de `AI_PROCESS.md`

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Python + FastAPI |
| ORM / migraciones | SQLAlchemy + Alembic |
| Base de datos | PostgreSQL |
| Frontend | Angular *(pendiente)* |
| Tests | pytest + pytest-cov + httpx |
| Linter / formateador | ruff |

## Estructura del backend

Organización por **capas técnicas**, con el cálculo EVM aislado en un subpaquete puro (sin FastAPI ni SQLAlchemy):

```
backend/
├── app/
│   ├── main.py                 # FastAPI app + /health; Swagger en /docs
│   ├── core/
│   │   ├── config.py           # Settings (pydantic-settings), lee .env
│   │   └── database.py         # engine, SessionLocal, Base, get_db()
│   ├── models/                 # entidades SQLAlchemy (Project, Activity)
│   ├── schemas/                # Pydantic request/response
│   ├── repositories/           # acceso a datos
│   ├── services/
│   │   └── evm/                # fórmulas EVM (Python puro, testeable sin API/DB)
│   └── routers/                # endpoints (delgados)
├── alembic/                    # migraciones de base de datos
├── tests/
│   ├── unit/                   # tests de services
│   ├── integration/            # tests de endpoints
│   └── conftest.py
└── pyproject.toml              # deps, ruff, cobertura ≥80% sobre app.services
```

### Modelos

- **`Project`**: `id`, `name`, `created_at`, `updated_at`.
- **`Activity`**: `id`, `project_id` (FK a `projects.id`, `ON DELETE CASCADE`), `name`, `bac`, `planned_progress`, `actual_progress`, `ac`, `created_at`, `updated_at`.
- Los indicadores EVM (PV, EV, CV, SV, CPI, SPI, EAC, VAC) **no se persisten**: se calculan al vuelo en `app/services/evm`, siempre a partir de los datos crudos de `Activity`.
- Validaciones a nivel de base de datos (`CheckConstraint`): `bac > 0`, `ac >= 0`, `planned_progress` y `actual_progress` entre 0 y 100.

## Requisitos

- Python ≥ 3.11
- PostgreSQL corriendo localmente (o accesible por red)

## Configurar la base de datos

1. Crea una base de datos vacía en tu instancia de PostgreSQL, por ejemplo `evm_tracker`.
2. Copia `backend/.env.example` como `backend/.env` y completa el `DATABASE_URL` real:

   ```
   DATABASE_URL=postgresql+psycopg2://postgres:<tu_password>@localhost:5432/evm_tracker
   ```

   `backend/.env` está en `.gitignore` — nunca se sube al repositorio.

3. Con el entorno virtual activo (ver siguiente sección), aplica las migraciones:

   ```bash
   cd backend
   python -m alembic upgrade head
   ```

   Esto crea las tablas `projects` y `activities` con sus foreign keys, `ON DELETE CASCADE` y `CheckConstraint`s.

## Cómo correr el backend

Desde la raíz del repo. Los comandos son iguales entre sistemas operativos, salvo por cómo se crea/activa el entorno virtual.

**Windows (PowerShell):**

```powershell
cd backend

# Crear el entorno virtual (solo la primera vez)
python -m venv venv

# Activar el venv — el prompt debe mostrar (venv)
.\venv\Scripts\Activate.ps1

# Instalar dependencias (runtime + herramientas de desarrollo)
pip install -e ".[dev]"

# Levantar la API (usa python -m para evitar problemas de PATH en Windows)
python -m uvicorn app.main:app --reload
```

Si ves `uvicorn : El término 'uvicorn' no se reconoce...`, casi seguro el venv no está activo (el prompt no muestra `(venv)`). Vuelve a ejecutar `.\venv\Scripts\Activate.ps1` y reintenta con `python -m uvicorn ...`.

**macOS / Linux (bash/zsh):**

```bash
cd backend

# Crear el entorno virtual (solo la primera vez)
python3 -m venv venv

# Activar el venv — el prompt debe mostrar (venv)
source venv/bin/activate

# Instalar dependencias (runtime + herramientas de desarrollo)
pip install -e ".[dev]"

# Levantar la API
python -m uvicorn app.main:app --reload
```

Si ves `command not found: uvicorn` o `python3: command not found`, revisa que el venv esté activo (`which python` debe apuntar a `backend/venv/bin/python`).

Una vez levantada, en cualquier sistema operativo:

- API: http://127.0.0.1:8000
- Health: http://127.0.0.1:8000/health → `{"status":"ok"}`
- Swagger UI: http://127.0.0.1:8000/docs

## Migraciones (Alembic)

Con el entorno virtual activo (ver sección anterior según tu sistema operativo), los comandos son los mismos en Windows, macOS y Linux:

```bash
cd backend

# Generar una migración a partir de cambios en los modelos
python -m alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migraciones pendientes
python -m alembic upgrade head

# Revertir la última migración
python -m alembic downgrade -1
```

La URL de conexión se lee desde `.env` (vía `app.core.config.Settings`); `alembic.ini` no contiene credenciales.

## Lint y formato

Con el entorno virtual activo, desde `backend/` (mismo comando en cualquier sistema operativo):

```bash
ruff check .
ruff format .
```

## Tests

La configuración en `pyproject.toml` exige cobertura mínima del **80%** sobre `app.services`. Los tests unitarios e de integración se agregarán junto con la lógica EVM y los endpoints.

Con el entorno virtual activo, desde `backend/` (mismo comando en cualquier sistema operativo):

```bash
pytest
```

## Documentación del proceso

- [`context.md`](context.md) — brief del desafío técnico
- [`AI_PROCESS.md`](AI_PROCESS.md) — registro cronológico del trabajo con IA
