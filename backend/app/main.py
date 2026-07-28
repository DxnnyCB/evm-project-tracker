from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.activities import router as activities_router
from app.routers.projects import router as projects_router

# Orígenes del `ng serve` local (hostname y loopback IP).
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app = FastAPI(
    title="EVM Project Tracker API",
    description=(
        "API REST para gestión de proyectos y actividades, con cálculo automático "
        "de indicadores de Valor Ganado (EVM)."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects_router)
app.include_router(activities_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Verifica que la API está viva. Swagger UI queda disponible en /docs."""
    return {"status": "ok"}
