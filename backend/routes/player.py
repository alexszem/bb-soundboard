from fastapi import APIRouter, HTTPException
from backend.service.player import add_new_player, edit_player_name, edit_player_walkup_song, delete_player, get_player, get_all_players

router = APIRouter(prefix="/players", tags=["Players"])

@router.post("/add")
def add_player_route(name: str, walkup_snippet_id: int):
    try:
        add_new_player(name, walkup_snippet_id)
        return {"message": "Player added successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/edit_name")
def edit_player_name_route(old_name: str, new_name: str):
    edit_player_name(old_name, new_name)
    return {"message": "Player name updated successfully"}

@router.put("/edit_walkup")
def edit_player_walkup_song_route(player_name: str, new_walkup_snippet_id: int):
    try:
        edit_player_walkup_song(player_name, new_walkup_snippet_id)
        return {"message": "Player walkup song updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{player_name}")
def delete_player_route(player_name: str):
    delete_player(player_name)
    return {"message": "Player deleted successfully"}

@router.get("/{player_name}")
def get_player_route(player_name: str):
    player = get_player(player_name)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.get("/")
def get_all_players_route():
    return get_all_players()