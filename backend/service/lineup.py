from backend.crud.lineup import add_player_to_lineup as add_player_to_lineup_crud, set_next_batter, get_current_batter, set_current_batter as set_current_batter_crud, get_full_lineup as get_full_lineup_crud
from .player import play_player_walkup

def add_player_to_lineup(player_name: str, position: int):
    add_player_to_lineup_crud(player_name, position)

def set_current_batter(index: int):
    set_current_batter_crud(index)

def get_full_lineup():
    return get_full_lineup_crud()

def play_current_batter_walkup():
    current_batter = get_current_batter()
    lineup = get_full_lineup_crud()
    position = current_batter
    player_name = next((entry['player_name'] for entry in lineup if entry['position'] == position), None)
    if player_name:
        play_player_walkup(player_name)
    else:
        raise ValueError("No player assigned to current batter position.")

def play_next_batter_walkup():
    next_batter_index = set_next_batter()
    lineup = get_full_lineup_crud()
    player_name = next((entry['player_name'] for entry in lineup if entry['position'] == next_batter_index), None)
    if player_name:
        play_player_walkup(player_name)
    else:
        raise ValueError("No player assigned to next batter position.")