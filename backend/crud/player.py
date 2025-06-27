from backend.crud.utils import with_session
from backend.models import Player
from backend.crud.snippet import get_snippet

@with_session
def add_player(session, name: str, walkup_snippet_id: int):
    player = Player(name=name, walkup_snippet_id=walkup_snippet_id)
    session.add(player)
    session.commit()

@with_session
def edit_player_name(session, old_name: str, new_name: str):
    player = session.query(Player).filter(Player.name == old_name).first()
    if player:
        player.name = new_name
        session.commit()

@with_session
def edit_player_walkup_song(session, player_name: str, new_walkup_snippet_id: int):
    player = session.query(Player).filter(Player.name == player_name).first()
    if player:
        player.walkup_snippet_id = new_walkup_snippet_id
        session.commit()

@with_session
def delete_player(session, player_name: str):
    player = session.query(Player).filter(Player.name == player_name).first()
    if player:
        session.delete(player)
        session.commit()

@with_session
def get_player(session, player_name: str):
    player = session.query(Player).filter(Player.name == player_name).first()
    if player:
        snippet_data = get_snippet(player.walkup_snippet_id)
        return {
            "name": player.name,
            "walkup_snippet": snippet_data
        }
    return None

@with_session
def get_all_players(session):
    players = session.query(Player).all()
    result = []
    for player in players:
        snippet_data = get_snippet(player.walkup_snippet_id)
        result.append({
            "name": player.name,
            "walkup_snippet": snippet_data
        })
    return result