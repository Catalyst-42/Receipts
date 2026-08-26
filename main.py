from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.staticfiles import StaticFiles
from src.core.middleware import ProcessTimeMiddleware

from src.config import settings
from src.core.router import router as core_router
from src.measures.router import router as measures_router
from src.nds.router import router as nds_router
from src.payments.router import router as payments_router
from src.products.router import router as products_router
from src.receipts.router import router as receipts_router
from src.registry.router import router as registry_router

app = FastAPI(title=settings.app_name, version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    ProcessTimeMiddleware,
)

# Redirect
if settings.ssl_keyfile and settings.ssl_certfile:
    app.add_middleware(HTTPSRedirectMiddleware)

# Static
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(core_router)

# Core
app.include_router(registry_router)

# Receipts
app.include_router(receipts_router)

# Retailers

# Directories
app.include_router(measures_router)
app.include_router(nds_router)
app.include_router(payments_router)
app.include_router(products_router)


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
