from fastapi import APIRouter, HTTPException, status
from api.schemas.run import CodeRunRequest, CodeRunResponse
from api.services.k8s_runner import run_code_in_k8s

router = APIRouter(prefix='/run', tags=["run"])

@router.post("/sync", response_model=CodeRunResponse)
async def run_sync(request: CodeRunRequest):
    try:
        result = await run_code_in_k8s(request)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка выполнения кода")