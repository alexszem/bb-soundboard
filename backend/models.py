from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from .enums import UsageNamePgEnum

class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, index=True)
    artist = Column(String)
    name = Column(String)
    length = Column(Integer)
    file_ending = Column(String)

    snippets = relationship("Snippet", back_populates="song", cascade="all, delete")

class Snippet(Base):
    __tablename__ = "snippets"
    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("songs.id"))
    start = Column(Integer)
    stop = Column(Integer)

    song = relationship("Song", back_populates="snippets")
    usages = relationship("Usage", back_populates="snippet", cascade="all, delete")
    players = relationship("Player", back_populates="walkup_snippet")

class Usage(Base):
    __tablename__ = "usages"
    id = Column(Integer, primary_key=True, index=True)
    snippet_id = Column(Integer, ForeignKey("snippets.id"))
    usage_name = Column(UsageNamePgEnum, default="UNKNOWN")

    snippet = relationship("Snippet", back_populates="usages")

class Player(Base):
    __tablename__ = "players"
    name = Column(String, primary_key=True)
    walkup_snippet_id = Column(Integer, ForeignKey("snippets.id"))

    walkup_snippet = relationship("Snippet", back_populates="players")

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    current_batter_index = Column(Integer, default=0)  # persisted current batter position

    lineup = relationship("LineupEntry", back_populates="game", cascade="all, delete")

class LineupEntry(Base):
    __tablename__ = "lineup_entries"
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    position = Column(Integer)
    player_name = Column(String, ForeignKey("players.name"), nullable=True)  # position can be unoccupied

    game = relationship("Game", back_populates="lineup")
    player = relationship("Player")