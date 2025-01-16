from fastapi import APIRouter

from app.core.exceptions.exceptions import ConflictError

router  = APIRouter(tags=["Checks health"])

@router.get('/health')
@router.head('/health')
@router.patch('/health')
async def get_health():
    """
    Check the health of the service.
    :return: x
    """

    return {'status': 'ok'}