from fastapi import Depends
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter

from src.crpt.dependencies import get_crpt_service
from src.crpt.service import CrptService
from src.users.dependencies import get_admin
from src.users.schemes import User

router = APIRouter(prefix="/admin/crpt", tags=["CRPT"])


@router.get("/export")
async def download_export(
    admin: User = Depends(get_admin),
    crpt_service: CrptService = Depends(get_crpt_service),
) -> StreamingResponse:
    """Returns dump of all crpt QR codes"""
    result = await crpt_service.export()
    return result
