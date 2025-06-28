from fastapi import APIRouter, HTTPException
from backend.crud.lineup import get_current_batter
from backend.service.lineup import add_player_to_lineup, set_current_batter, get_full_lineup, play_current_batter_walkup, play_next_batter_walkup

router = APIRouter(prefix="/lineup", tags=["Lineup"])

@router.post("/add_player")
def add_player_route(player_name: str, position: int):
    add_player_to_lineup(player_name, position)
    return {"message": "Player added to lineup"}

@router.put("/set_current_batter")
def set_current_batter_route(index: int):
    set_current_batter(index)
    return {"message": "Current batter set successfully"}

@router.get("/")
def get_full_lineup_route():
    lineup = get_full_lineup()
    current_position = get_current_batter()
    return {
        "current_position": current_position,
        "lineup": lineup
    }

@router.get("/play_current_batter_walkup")
def play_current_batter_route():
    try:
        play_current_batter_walkup()
        return {"message": "Playing current batter's walkup song"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/play_next_batter_walkup")
def play_next_batter_route():
    try:
        play_next_batter_walkup()
        return {"message": "Playing next batter's walkup song"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))