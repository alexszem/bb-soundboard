from backend.database import SessionLocal
from backend.models import Game, LineupEntry

def with_game_session(func):
    def wrapper(*args, **kwargs):
        session = SessionLocal()
        try:
            game = session.query(Game).first()
            if not game:
                game = Game(current_batter_index=0)
                session.add(game)
                session.commit()
            result = func(session, game, *args, **kwargs)
            return result
        finally:
            session.close()
    return wrapper

@with_game_session
def add_player_to_lineup(session, game, player_name: str, position: int):
    lineup_entries = session.query(LineupEntry).filter(LineupEntry.game_id == game.id).all()
    player_entry = next((e for e in lineup_entries if e.player_name == player_name), None)
    target_entry = next((e for e in lineup_entries if e.position == position), None)

    previous_position = player_entry.position if player_entry else None

    if not target_entry:
        target_entry = LineupEntry(game_id=game.id, position=position, player_name=player_name)
        session.add(target_entry)
    else:
        swap_players(session, lineup_entries, player_entry, target_entry, player_name, previous_position)

    session.commit()

def swap_players(session, lineup_entries, player_entry, target_entry, player_name, previous_position):
    overwritten_player = target_entry.player_name
    target_entry.player_name = player_name

    if player_entry:
        if overwritten_player:
            player_entry_at_prev = next((e for e in lineup_entries if e.position == previous_position), None)
            if player_entry_at_prev:
                player_entry_at_prev.player_name = overwritten_player
            else:
                new_entry = LineupEntry(game_id=player_entry.game_id, position=previous_position, player_name=overwritten_player)
                session.add(new_entry)
        else:
            session.delete(player_entry)
    else:
        if overwritten_player:
            old_position_entry = next((e for e in lineup_entries if e.player_name == overwritten_player), None)
            if old_position_entry:
                old_position_entry.player_name = overwritten_player

def get_full_lineup():
    session = SessionLocal()
    try:
        lineup_entries = session.query(LineupEntry).order_by(LineupEntry.position).all()
        return [
            {
                "position": entry.position,
                "player_name": entry.player_name  # can be None if unoccupied
            }
            for entry in lineup_entries
        ]
    finally:
        session.close()

@with_game_session
def set_next_batter(session, game):
    lineup_size = session.query(LineupEntry).filter(LineupEntry.game_id == game.id).count()
    game.current_batter_index = (game.current_batter_index + 1) % lineup_size
    session.commit()
    return game.current_batter_index

@with_game_session
def get_current_batter(session, game):
    lineup_entry = session.query(LineupEntry).filter(LineupEntry.position == game.current_batter_index).first()
    return {
        "current_index": game.current_batter_index,
        "player_name": lineup_entry.player_name if lineup_entry else None
    }

@with_game_session
def set_current_batter(session, game, index: int):
    game.current_batter_index = index
    session.commit()