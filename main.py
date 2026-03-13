import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.logging import init_logger
from src.routes.graph import graph_router
from src.core.settings import DevelopmentSettings as Settings

app = FastAPI()
settings = Settings()
init_logger(settings)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graph_router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)