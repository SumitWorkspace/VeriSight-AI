from __future__ import annotations

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.api.routes import router
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.database import Base, engine
from app.db import models
from app.db.migrations import run_lightweight_migrations
from app.middleware.error_handler import RequestLoggingMiddleware, unhandled_exception_handler
from app.middleware.rate_limiter import SlidingWindowRateLimiter
from app.services.model_service import model_service


logger = logging.getLogger("fake_review_api")


def check_startup_health() -> None:
    logger.info("=" * 60)
    logger.info(" VERISIGHT AI BACKEND STARTUP DIAGNOSTICS")
    logger.info("=" * 60)
    logger.info("App Name:        %s", settings.app_name)
    logger.info("Database URL:    %s", settings.database_url)
    logger.info("Model Directory: %s", settings.model_dir)
    logger.info("Frontend Origin: %s", settings.frontend_origin)

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database Status:  OK (Connection successful & verified)")
    except Exception as exc:
        logger.error("Database Status:  FAILED (Could not execute verification query: %s)", exc)

    if model_service.model_loaded:
        logger.info("Classifier Model: LOADED (High-fidelity Neural Transformer Active)")
    else:
        logger.warning("Classifier Model: WARNING (Model folder not found; using deterministic BaselineClassifier)")
    logger.info("=" * 60)


configure_logging()
Base.metadata.create_all(bind=engine)
run_lightweight_migrations()
check_startup_health()

app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_exception_handler(Exception, unhandled_exception_handler)

async def validation_exception_handler(request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": "Unprocessable Entity",
            "detail": "Invalid request payload size, characters, or structural boundaries.",
            "path": request.url.path,
        },
    )

app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Protect application endpoints with rate limiting
app.add_middleware(SlidingWindowRateLimiter, requests_limit=100, window_seconds=60)
app.add_middleware(RequestLoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
