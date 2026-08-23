from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.staticfiles import StaticFiles

from src.config import settings
# from src.receipts.router import router as receipts_router
from src.measures.router import router as measures_router

app = FastAPI(title=settings.app_name, version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redirect
if settings.ssl_keyfile and settings.ssl_certfile:
    app.add_middleware(HTTPSRedirectMiddleware)

# Static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routes
# app.include_router(receipts_router)
app.include_router(measures_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        ssl_keyfile=settings.ssl_keyfile,
        ssl_certfile=settings.ssl_certfile,
        reload=settings.debug,
    )
