from fastapi.responses import FileResponse
from fastapi.routing import APIRouter

router = APIRouter(tags=["Core"])


@router.get("/", include_in_schema=False)
async def root() -> FileResponse:
    """Returns a frontend page with receipt scanner"""
    return FileResponse("static/index.html")
