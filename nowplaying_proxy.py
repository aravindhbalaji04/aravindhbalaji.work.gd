import os

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


def _parse_frontend_origins():
    raw = os.getenv("FRONTEND_ORIGINS", "")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


FRONTEND_ORIGINS = _parse_frontend_origins() or ["http://localhost:5500"]

# CORS origins are configured via FRONTEND_ORIGINS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME")


@app.get("/api/nowplaying")
def now_playing():
    if not LASTFM_API_KEY or not LASTFM_USERNAME:
        raise HTTPException(
            status_code=500,
            detail="Missing LASTFM_API_KEY or LASTFM_USERNAME environment variables.",
        )

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
