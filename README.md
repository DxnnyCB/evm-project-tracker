# EVM Project Tracker

Herramienta interna para líderes de proyecto: registrar el avance de actividades y evaluar en tiempo real el estado de cronograma y presupuesto con la metodología de **Valor Ganado (Earned Value Management — EVM)**.

> **Estado actual (`feature/project-structure`):** esqueleto del backend listo (capas, dependencias, linter y app mínima con Swagger). Aún no hay lógica EVM, endpoints CRUD ni frontend.

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
│   ├── core/                   # config, database (próximo)
│   ├── models/                 # entidades SQLAlchemy
│   ├── schemas/                # Pydantic request/response
│   ├── repositories/           # acceso a datos
│   ├── services/
│   │   └── evm/                # fórmulas EVM (Python puro, testeable sin API/DB)
│   └── routers/                # endpoints (delgados)
├── tests/
│   ├── unit/                   # tests de services
│   ├── integration/            # tests de endpoints
│   └── conftest.py
└── pyproject.toml              # deps, ruff, cobertura ≥80% sobre app.services
```

## Requisitos

- Python ≥ 3.11
- (Opcional por ahora) PostgreSQL — aún no hay conexión configurada

## Cómo correr el backend

```bash
cd backend

# Crear y activar el entorno virtual (Windows)
python -m venv venv
.\venv\Scripts\activate

# Instalar dependencias (runtime + herramientas de desarrollo)
pip install -e ".[dev]"

# Levantar la API
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Health: http://127.0.0.1:8000/health → `{"status":"ok"}`
- Swagger UI: http://127.0.0.1:8000/docs

## Lint y formato

Desde `backend/`:

```bash
ruff check .
ruff format .
```

## Tests

La configuración en `pyproject.toml` exige cobertura mínima del **80%** sobre `app.services`. Los tests unitarios e de integración se agregarán junto con la lógica EVM y los endpoints.

```bash
cd backend
pytest
```

## Documentación del proceso

- [`context.md`](context.md) — brief del desafío técnico
- [`AI_PROCESS.md`](AI_PROCESS.md) — registro cronológico del trabajo con IA
