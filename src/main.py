"""
Command line runner for the Music Recommender Simulation.

Run from project root: python3 -m src.main
"""

from .recommender import load_songs, recommend_songs


# --- User Profiles ---

PROFILES = {
    "High-Energy Pop": {
        "genre":          "pop",
        "mood":           "happy",
        "target_energy":  0.90,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre":          "lofi",
        "mood":           "chill",
        "target_energy":  0.38,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre":          "rock",
        "mood":           "intense",
        "target_energy":  0.92,
        "likes_acoustic": False,
    },
    # --- Adversarial / Edge Case Profiles ---
    "Conflicting: High Energy + Melancholic": {
        # High energy but sad mood — tests whether energy or mood drives ranking
        "genre":          "hip-hop",
        "mood":           "melancholic",
        "target_energy":  0.90,
        "likes_acoustic": False,
    },
    "Ghost Genre (no catalog match)": {
        # Genre doesn't exist in the catalog — categorical match never fires
        "genre":          "bossa nova",
        "mood":           "relaxed",
        "target_energy":  0.45,
        "likes_acoustic": True,
    },
    "Extremes: Dead Silent + Electronic": {
        # target_energy=0.0 — punishes nearly every song; likes_acoustic=False
        # reveals whether near-zero energy songs even exist to bubble up
        "genre":          "ambient",
        "mood":           "peaceful",
        "target_energy":  0.0,
        "likes_acoustic": False,
    },
}


def print_results(profile_name: str, user_prefs: dict, recommendations: list) -> None:
    print("\n" + "=" * 55)
    print(f"  {profile_name}")
    print("=" * 55)
    print(f"  genre={user_prefs['genre']} | mood={user_prefs['mood']} | "
          f"energy={user_prefs['target_energy']} | acoustic={user_prefs['likes_acoustic']}")
    print("-" * 55)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']} by {song['artist']}")
        print(f"       Score : {score:.2f} / 7.00")
        print(f"       Genre : {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        for reason in explanation.split(", "):
            print(f"       + {reason}")
    print("\n" + "=" * 55)


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_results(profile_name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
