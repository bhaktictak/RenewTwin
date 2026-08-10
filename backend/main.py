from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database.db import init_db
from .routes import assets, dashboard, predict

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title='RenewTwin API',
    description='AI-Powered Digital Twin for Renewable Energy Asset Management',
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assets.router)
app.include_router(dashboard.router)
app.include_router(predict.router)

@app.get("/")
async def root():
    return {
        "title": "RenewTwin API",
        "description": "AI-Powered Digital Twin for Renewable Energy Asset Management",
        "docs_url": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
