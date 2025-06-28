from fastapi import APIRouter, HTTPException
from backend.service.usage import add_new_usage, edit_existing_usage, delete_existing_usage, play_random_snippet_by_usage, get_usage, get_all_usages

router = APIRouter(prefix="/usages", tags=["Usages"])

@router.post("/add")
def add_usage_route(snippet_id: int, usage_name: str):
    try:
        usage_id = add_new_usage(snippet_id, usage_name)
        return {"message": "Usage added successfully", "usage_id": usage_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{usage_id}")
def delete_usage_route(usage_id: int):
    delete_existing_usage(usage_id)
    return {"message": "Usage deleted successfully"}

@router.get("/play_random/{usage_name}")
def play_random_usage_route(usage_name: str):
    try:
        play_random_snippet_by_usage(usage_name)
        return {"message": "Playing random snippet for usage"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{usage_id}")
def get_usage_route(usage_id: int):
    usage = get_usage(usage_id)
    if not usage:
        raise HTTPException(status_code=404, detail="Usage not found")
    return usage

@router.get("/")
def get_all_usages_route():
    return get_all_usages()