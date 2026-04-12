"""
Command line runner for the Music Recommender Simulation.

Run from the project root:
    python -m src.main

Or from the src/ directory:
    python main.py
"""

import sys
import os

# Allow running as `python main.py` from inside src/
sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# User profiles
# Each dict is a taste profile. Supported keys:
#   genre            (str)   — preferred genre
#   mood             (str)   — preferred mood
#   energy           (float) — target energy level 0–1
#   likes_acoustic   (bool)  — True = prefers acoustic; False = prefers electronic
#   target_danceability (float) — preferred danceability 0–1 (optional)
#   target_valence      (float) — preferred emotional positivity 0–1 (optional)
#   target_tempo_bpm    (float) — preferred BPM (optional)
#   avoid_mood       (str)   — mood to down-rank (optional)
#   avoid_genre      (str)   — genre to down-rank (optional)
# ---------------------------------------------------------------------------

PROFILES = [
    {
        "name": "Gym Warrior",
        "description": "Crushing a workout — needs maximum energy and drive.",
        "genre": "pop",
        "mood": "intense",
        "energy": 0.95,
        "likes_acoustic": False,
        "target_danceability": 0.88,
        "target_tempo_bpm": 138,
        "avoid_mood": "chill",
    },
    {
        "name": "Deep Focus",
        "description": "Long coding session — low distraction, steady flow.",
        "genre": "lofi",
        "mood": "focused",
        "energy": 0.38,
        "likes_acoustic": True,
        "target_danceability": 0.50,
        "target_valence": 0.55,
        "target_tempo_bpm": 80,
        "avoid_mood": "excited",
        "avoid_genre": "metal",
    },
    {
        "name": "Late Night Driver",
        "description": "Cruising alone at 2 AM — moody and cinematic.",
        "genre": "synthwave",
        "mood": "moody",
        "energy": 0.72,
        "likes_acoustic": False,
        "target_valence": 0.38,
        "target_tempo_bpm": 112,
        "avoid_mood": "happy",
    },
    {
        "name": "Sunday Acoustic",
        "description": "Slow morning with coffee — warm, organic, unhurried.",
        "genre": "folk",
        "mood": "relaxed",
        "energy": 0.28,
        "likes_acoustic": True,
        "target_danceability": 0.40,
        "target_valence": 0.68,
        "target_tempo_bpm": 86,
        "avoid_genre": "edm",
        "avoid_mood": "intense",
    },
    {
        "name": "Party Mode",
        "description": "Pre-game energy — loud, fast, impossible not to move.",
        "genre": "edm",
        "mood": "excited",
        "energy": 0.93,
        "likes_acoustic": False,
        "target_danceability": 0.92,
        "target_tempo_bpm": 140,
        "avoid_mood": "sad",
        "avoid_genre": "classical",
    },
    {
        "name": "Jazz Evening",
        "description": "Dinner at home — sophisticated, relaxed, slightly smoky.",
        "genre": "jazz",
        "mood": "relaxed",
        "energy": 0.36,
        "likes_acoustic": True,
        "target_danceability": 0.52,
        "target_valence": 0.68,
        "target_tempo_bpm": 90,
        "avoid_mood": "intense",
        "avoid_genre": "metal",
    },
    {
        "name": "Rainy Day Feels",
        "description": "Overcast sky, comfort food, a little melancholy.",
        "genre": "blues",
        "mood": "sad",
        "energy": 0.34,
        "likes_acoustic": True,
        "target_valence": 0.28,
        "target_tempo_bpm": 74,
        "avoid_mood": "excited",
        "avoid_genre": "edm",
    },
    {
        "name": "Hip Hop Head",
        "description": "Walking through the city — sharp, rhythmic, confident.",
        "genre": "hip-hop",
        "mood": "focused",
        "energy": 0.70,
        "likes_acoustic": False,
        "target_danceability": 0.82,
        "target_tempo_bpm": 96,
        "avoid_mood": "relaxed",
    },
]


def print_recommendations(profile: dict, recommendations: list) -> None:
    print("=" * 60)
    print(f"  {profile['name'].upper()}")
    print(f"  {profile['description']}")
    print("=" * 60)
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"  {i}. {song['title']} by {song['artist']}")
        print(f"     Score: {score:.2f}  |  {song['genre']} / {song['mood']}  |  energy {song['energy']:.2f}")
        print(f"     Why: {explanation}")
    print()


def main() -> None:
    # Resolve path relative to project root regardless of where the script is run from
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "..", "data", "songs.csv")

    songs = load_songs(csv_path)
    print(f"Loaded {len(songs)} songs.\n")

    for profile in PROFILES:
        recs = recommend_songs(profile, songs, k=5)
        print_recommendations(profile, recs)


if __name__ == "__main__":
    main()
