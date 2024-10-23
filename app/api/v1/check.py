from fastapi import APIRouter

router  = APIRouter(tags=["Checks health"])

@router.get('/health')
@router.head('/health')
@router.patch('/health')
@router.put('/health')
@router.delete('/health')
@router.post('/health')
async def get_health():
    """
    Check the health of the service.
    :return: x
    """
    return {'status': 'ok'}