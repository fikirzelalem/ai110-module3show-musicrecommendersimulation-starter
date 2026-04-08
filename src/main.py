"""
Command line runner for the Music Recommender Simulation.
Tests multiple user profiles to evaluate recommender behavior.
"""

from src.recommender import load_songs, recommend_songs, SCORING_MODES


PROFILES = {
    "High-Energy Pop": {
        "genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": False,
        "likes_popular": True, "preferred_decade": 2020, "preferred_mood_tag": "euphoric",
        "prefers_clean": True, "likes_live": False,
    },
    "Chill Lofi": {
        "genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True,
        "likes_popular": False, "preferred_decade": 2020, "preferred_mood_tag": "peaceful",
        "prefers_clean": True, "likes_live": False,
    },
    "Deep Intense Rock": {
        "genre": "rock", "mood": "intense", "energy": 0.95, "likes_acoustic": False,
        "likes_popular": False, "preferred_decade": 2010, "preferred_mood_tag": "aggressive",
        "prefers_clean": False, "likes_live": True,
    },
    "Moody Electronic": {
        "genre": "electronic", "mood": "moody", "energy": 0.8, "likes_acoustic": False,
        "likes_popular": True, "preferred_decade": 2020, "preferred_mood_tag": "dark",
        "prefers_clean": True, "likes_live": False,
    },
    "Edge Case - High Energy but Relaxed": {
        "genre": "r&b", "mood": "relaxed", "energy": 0.9, "likes_acoustic": False,
        "likes_popular": True, "preferred_decade": 2020, "preferred_mood_tag": "romantic",
        "prefers_clean": True, "likes_live": False,
    },
}


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5, mode: str = "genre-first") -> None:
    print(f"\n{'='*55}")
    print(f"Profile: {label}  |  Mode: {mode}")
    print(f"{'='*55}")
    recommendations = recommend_songs(user_prefs, songs, k=k, mode=mode)
    if not recommendations:
        print("  No recommendations found.")
        return
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"  {i}. {song['title']} by {song['artist']} — Score: {score:.2f}")
        print(f"     Because: {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")

    print("\n\n*** Standard run: all profiles using genre-first mode ***")
    for label, prefs in PROFILES.items():
        print_recommendations(label, prefs, songs)

    print("\n\n*** Scoring mode comparison: Edge Case profile across all modes ***")
    edge_prefs = PROFILES["Edge Case - High Energy but Relaxed"]
    for mode in SCORING_MODES:
        print_recommendations("Edge Case - High Energy but Relaxed", edge_prefs, songs, mode=mode)

    print()


if __name__ == "__main__":
    main()
