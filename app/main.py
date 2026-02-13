# main.py
from __future__ import annotations
import sys
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Use relative imports from app package
from .routers import forecast, historic, sti
from .config import settings

app = FastAPI(
    title="Pangu MVP STI API",
    description="API para servir índices STI desde NetCDF en S3",
    version="0.1.0",
)

# CORS Configuration
origins = settings.CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(forecast.router)
app.include_router(historic.router, prefix="/historic", tags=["Historic"])
app.include_router(sti.router)



# --------------------------------------------------------------------
# Endpoints básicos
# --------------------------------------------------------------------

import logging
logging.getLogger(__name__).info("Logging is alive")




@app.get("/health")
def health():
    return {"status": "ok"}

