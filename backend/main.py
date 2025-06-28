from fastapi import FastAPI
from .routes import song, usage, lineup, snippet, player, playback

app = FastAPI(title="Music Playback API")

# Include all routers
app.include_router(song.router)
app.include_router(usage.router)
app.include_router(lineup.router)
app.include_router(snippet.router)
app.include_router(player.router)
app.include_router(playback.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)