import os

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for local frontend dev and GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY", "8453947459c1a6b0e4464db7027e145f")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME", "aravindhbalaji")


@app.get("/api/nowplaying")
def now_playing():
    url = (
        f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks"
        f"&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json&limit=1"
    )
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        track = data.get("recenttracks", {}).get("track", [{}])[0]
        return {"track": track}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
