from fastapi import APIRouter


router = APIRouter(
    prefix="/entities",
    tags=["entities"]
)


@router.get("/datasets", status_code=200)
async def read_datasets():
    return NotImplementedError


@router.get("/models", status_code=200)
async def read_models():
    return NotImplementedError


@router.get("/activeAircraft", status_code=200)
async def read_active_aircraft(manufacturer: str = "any", model: str = "any"):
    return NotImplementedError
