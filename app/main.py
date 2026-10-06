from fastapi import FastAPI

from app.routers import books, loans, members


def create_app() -> FastAPI:
    app = FastAPI(
        title="nsh-demo-app",
        description="API de biblioteca de préstamos (almacenamiento en memoria).",
        version="0.1.0",
    )
    app.include_router(books.router)
    app.include_router(members.router)
    app.include_router(loans.router)

    @app.get("/health", tags=["meta"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
