from backend.crud.player import add_player as add_player_crud, edit_player_name as edit_player_name_crud, edit_player_walkup_song as edit_player_walkup_song_crud, delete_player as delete_player_crud, get_player as get_player_crud, get_all_players as get_all_players_crud
from backend.crud.snippet import get_snippet as get_snippet_crud
from .snippet import play_snippet

# Player service layer
def add_new_player(name: str, walkup_snippet_id: int):
    # Validate snippet exists before adding player
    snippet = get_snippet_crud(walkup_snippet_id)
    if not snippet:
        raise ValueError("Walkup snippet does not exist.")
    add_player_crud(name, walkup_snippet_id)

def edit_player_name(old_name: str, new_name: str):
    edit_player_name_crud(old_name, new_name)

def edit_player_walkup_song(player_name: str, new_walkup_snippet_id: int):
    # Validate snippet exists before editing player walkup song
    snippet = get_snippet_crud(new_walkup_snippet_id)
    if not snippet:
        raise ValueError("Walkup snippet does not exist.")
    edit_player_walkup_song_crud(player_name, new_walkup_snippet_id)

def delete_player(player_name: str):
    delete_player_crud(player_name)

def play_player_walkup(player_name: str):
    player = get_player_crud(player_name)
    if not player:
        raise ValueError("Player does not exist.")

    snippet = player['walkup_snippet']
    play_snippet(snippet['id'])

def get_player(player_name: str):
    return get_player_crud(player_name)

def get_all_players():
    return get_all_players_crud()