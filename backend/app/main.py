"""
FastAPI application factory and entry point.

Creates and configures the FastAPI application instance with middleware,
routers, and startup/shutdown event handlers.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


# ── Lifespan ─────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events:
    - Startup: Log application start, verify database connectivity.
    - Shutdown: Clean up resources, dispose database connections.
    """
    # ── Startup ──────────────────────────────────────────────────────────
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Environment: {settings.app_env}")
    print(f"Debug mode: {settings.debug}")

    yield

    # ── Shutdown ─────────────────────────────────────────────────────────
    print(f"Shutting down {settings.app_name}")
    from app.database.session import engine
    engine.dispose()
    print("Database connections disposed.")


# ── Application Factory ─────────────────────────────────────────────────────

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns a fully configured FastAPI instance with:
    - CORS middleware
    - Health check endpoint
    - API v1 routers (added in future phases)
    """

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI-Powered Multilingual Content Localization Engine",
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
        lifespan=lifespan,
    )

    # ── CORS Middleware ──────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Health Check ─────────────────────────────────────────────────────

    @app.get(
        "/health",
        tags=["Health"],
        summary="Health check",
        description="Returns the health status of the application.",
    )
    def health_check():
        """
        Basic health check endpoint.

        Returns a simple JSON response indicating the application is running.
        This endpoint requires no authentication and is used by load balancers
        and monitoring tools.
        """
        return {"status": "healthy"}

    # ── API Routers ──────────────────────────────────────────────────────
    # Routers will be included here in future phases:
    # from app.api.v1.router import api_v1_router
    # app.include_router(api_v1_router, prefix="/api/v1")

    return app


# ── Application Instance ────────────────────────────────────────────────────
# Created via the factory so the same pattern works for testing.

app = create_app()


# ── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.is_development,
    )
