from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["Generic"])
async def home():
    return {"details": "Welcome to homepage."}
