import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to float/int."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences (max 8.0) and return (score, reasons).

    Max breakdown: genre +1.0, mood +1.5, energy +4.0, acoustic +1.0, valence +0.5 = 8.0
    """
    score = 0.0
    reasons = []

    # Genre match — binary, +1.0
    if song["genre"] == user_prefs["genre"]:
        score += 1.0
        reasons.append(f"genre match (+1.0)")

    # Mood match — binary, +1.5
    if song["mood"] == user_prefs["mood"]:
        score += 1.5
        reasons.append(f"mood match (+1.5)")

    # Energy proximity — quadratic, up to +4.0.
    # Bounds proof: both song["energy"] and target_energy are in [0, 1], so their
    # difference is in [-1, 1] and its square is in [0, 1].  Therefore
    # (1.0 - diff²) is in [0, 1] and 4.0 * (1.0 - diff²) is in [0.0, 4.0]. ✓
    energy_points = 4.0 * (1.0 - (song["energy"] - user_prefs["target_energy"]) ** 2)
    score += energy_points
    reasons.append(f"energy proximity (+{energy_points:.2f})")

    # Acoustic fit — continuous, up to +1.0
    if user_prefs["likes_acoustic"]:
        acoustic_points = song["acousticness"]
    else:
        acoustic_points = 1.0 - song["acousticness"]
    score += acoustic_points
    reasons.append(f"acoustic fit (+{acoustic_points:.2f})")

    # Valence tiebreaker — continuous, up to +0.5
    valence_points = 0.5 * song["valence"]
    score += valence_points
    reasons.append(f"valence (+{valence_points:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort by score descending, and return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        total_score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, total_score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
