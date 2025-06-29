from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.crud.snippet import get_snippets_by_song
from backend.crud.usage import get_usage_names_for_snippet, set_usages_for_snippet
from backend.service.snippet import add_new_snippet, edit_existing_snippet, delete_snippet, get_snippet, get_all_snippets

router = APIRouter(prefix="/snippets", tags=["Snippets"])

@router.post("/add")
def add_snippet_route(song_id: int, start: int = None, stop: int = None):
    try:
        snippet_id = add_new_snippet(song_id, start, stop)
        return {"message": "Snippet added successfully", "snippet_id": snippet_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{snippet_id}")
def edit_snippet_route(snippet_id: int, start: int = None, stop: int = None):
    try:
        edit_existing_snippet(snippet_id, start, stop)
        return {"message": "Snippet updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{snippet_id}")
def delete_snippet_route(snippet_id: int):
    delete_snippet(snippet_id)
    return {"message": "Snippet deleted successfully"}

@router.get("/{snippet_id}")
def get_snippet_route(snippet_id: int):
    snippet = get_snippet(snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return snippet

@router.get("/by-song/{song_id}")
def read_snippets_by_song(song_id: int):
    return get_snippets_by_song(song_id)

class SnippetUsagesUpdateRequest(BaseModel):
    snippet_id: int
    usage_names: list[str]

@router.post("/set-usages")
def set_usages(req: SnippetUsagesUpdateRequest):
    return set_usages_for_snippet(req.snippet_id, req.usage_names)

@router.get("/{snippet_id}/usages")
def read_usage_names(snippet_id: int):
    return get_usage_names_for_snippet(snippet_id)

@router.get("/")
def get_all_snippets_route():
    return get_all_snippets()