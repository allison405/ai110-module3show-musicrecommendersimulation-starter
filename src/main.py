"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Default "pop/happy" profile
    user_prefs = {
        "genre":          "pop",
        "mood":           "happy",
        "target_energy":  0.80,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("  Music Recommender — Top 5 Picks")
    print("=" * 50)
    print(f"  Profile: {user_prefs['genre']} | {user_prefs['mood']} | energy {user_prefs['target_energy']}")
    print("=" * 50)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f} / 7.00")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        for reason in explanation.split(", "):
            print(f"    + {reason}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
