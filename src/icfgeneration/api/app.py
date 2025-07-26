"""
Main FastAPI application module.
"""

from dotenv import load_dotenv


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from icfgeneration.api.routes import protocol
from icfgeneration.logger.logger_setup import loguru_setup

from icfgeneration.utils.constants import env_path

load_dotenv(env_path)

logger = loguru_setup()


# Create FastAPI app
app = FastAPI(
    title="ICF Generation API",
    description="API for ICF generation using LLMs",
    version="0.1.0",
    docs_url="/docs",  # Swagger UI endpoint
    redoc_url="/redoc",  # ReDoc endpoint
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(protocol.router)


@app.get("/")
async def root():
    """
    Root endpoint that redirects to the API documentation.
    """
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
