from fastapi import FastAPI

app = FastAPI(
    title="EVM Project Tracker API",
    description=(
        "API REST para gestión de proyectos y actividades, con cálculo automático "
        "de indicadores de Valor Ganado (EVM)."
    ),
    version="0.1.0",
)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Verifica que la API está viva. Swagger UI queda disponible en /docs."""
    return {"status": "ok"}
