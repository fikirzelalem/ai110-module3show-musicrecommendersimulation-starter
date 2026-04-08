from typing import List, Dict, Tuple
from dataclasses import dataclass
import csv


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score all songs for a user and return the top-k matches sorted by score."""
        prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dicts = [
            {
                "id": s.id,
                "title": s.title,
                "artist": s.artist,
                "genre": s.genre,
                "mood": s.mood,
                "energy": s.energy,
                "tempo_bpm": s.tempo_bpm,
                "valence": s.valence,
                "danceability": s.danceability,
                "acousticness": s.acousticness,
            }
            for s in self.songs
        ]
        scored = [(s, score_song(prefs, d)[0]) for s, d in zip(self.songs, song_dicts)]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-English explanation of why a song was recommended."""
        prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "acousticness": song.acousticness,
        }
        _, reasons = score_song(prefs, song_dict)
        return "; ".join(reasons) if reasons else "Partial match based on available features"


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with typed values."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
                "popularity": int(row["popularity"]),
                "release_decade": int(row["release_decade"]),
                "mood_tag": row["mood_tag"],
                "explicit": int(row["explicit"]),
                "live_feel": float(row["live_feel"]),
            })
    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs


SCORING_MODES = {
    "genre-first":    {"genre": 3.0, "mood": 1.0, "energy": 1.0},
    "mood-first":     {"genre": 1.0, "mood": 3.0, "energy": 1.0},
    "energy-focused": {"genre": 1.0, "mood": 1.0, "energy": 2.0},
}


def score_song(user_prefs: Dict, song: Dict, weights: Dict = None) -> Tuple[float, List[str]]:
    """Score a single song against user preferences; returns (score, reasons)."""
    if weights is None:
        weights = SCORING_MODES["genre-first"]

    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        pts = weights["genre"]
        score += pts
        reasons.append(f"genre match: {song['genre']} (+{pts})")

    if song["mood"] == user_prefs.get("mood"):
        pts = weights["mood"]
        score += pts
        reasons.append(f"mood match: {song['mood']} (+{pts})")

    energy_diff = abs(song["energy"] - user_prefs.get("energy", 0.5))
    energy_points = round(weights["energy"] * (1.0 - energy_diff), 2)
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points})")

    if user_prefs.get("likes_acoustic") and song["acousticness"] > 0.6:
        score += 0.5
        reasons.append("acoustic bonus (+0.5)")

    if user_prefs.get("likes_popular") and song.get("popularity", 0) > 70:
        popularity_bonus = round(song["popularity"] / 250, 2)
        score += popularity_bonus
        reasons.append(f"popularity bonus (+{popularity_bonus})")

    if user_prefs.get("preferred_decade") and song.get("release_decade") == user_prefs["preferred_decade"]:
        score += 0.5
        reasons.append(f"era match: {song['release_decade']}s (+0.5)")

    if user_prefs.get("preferred_mood_tag") and song.get("mood_tag") == user_prefs["preferred_mood_tag"]:
        score += 0.75
        reasons.append(f"mood tag match: {song['mood_tag']} (+0.75)")

    if user_prefs.get("prefers_clean") and song.get("explicit", 0) == 1:
        score -= 0.5
        reasons.append("explicit penalty (-0.5)")

    if user_prefs.get("likes_live") and song.get("live_feel", 0) > 0.5:
        score += 0.3
        reasons.append(f"live feel bonus (+0.3)")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "genre-first") -> List[Tuple[Dict, float, str]]:
    """Score and rank all songs, returning the top-k as (song, score, explanation) tuples."""
    weights = SCORING_MODES.get(mode, SCORING_MODES["genre-first"])
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights=weights)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    return scored[:k]
