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

    def _score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        # Mood match — highest filter weight (3.0)
        if song.mood == user.favorite_mood:
            score += 3.0
            reasons.append(f"mood matches '{song.mood}'")

        # Genre match — secondary filter weight (2.0)
        if song.genre == user.favorite_genre:
            score += 2.0
            reasons.append(f"genre matches '{song.genre}'")

        # Energy similarity — highest ranking weight (2.0)
        energy_sim = 1.0 - abs(user.target_energy - song.energy)
        score += 2.0 * energy_sim
        if energy_sim >= 0.85:
            reasons.append(f"energy level close to your target ({song.energy:.2f})")

        # Danceability — second ranking weight (1.5)
        score += 1.5 * song.danceability
        if song.danceability >= 0.70:
            reasons.append(f"highly danceable ({song.danceability:.2f})")

        # Valence — third ranking weight (1.0)
        score += 1.0 * song.valence

        # Tempo normalized to [0, 1] over 60–180 BPM range (0.5)
        tempo_norm = max(0.0, min(1.0, (song.tempo_bpm - 60) / 120))
        score += 0.5 * tempo_norm

        # Acousticness — prefer acoustic or electronic based on profile (0.5)
        acoustic_score = song.acousticness if user.likes_acoustic else (1.0 - song.acousticness)
        score += 0.5 * acoustic_score
        if user.likes_acoustic and song.acousticness >= 0.70:
            reasons.append(f"acoustic sound matches your preference ({song.acousticness:.2f})")
        elif not user.likes_acoustic and song.acousticness <= 0.25:
            reasons.append(f"electronic sound matches your preference ({song.acousticness:.2f})")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # Filter: keep songs matching mood or genre
        filtered = [s for s in self.songs if s.mood == user.favorite_mood or s.genre == user.favorite_genre]

        # Fall back to full catalog if not enough matches to fill k results
        if len(filtered) < k:
            filtered = self.songs

        scored = sorted(filtered, key=lambda s: self._score_song(user, s)[0], reverse=True)
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = self._score_song(user, song)
        if reasons:
            return "Recommended because: " + "; ".join(reasons)
        return "Similar overall audio profile to your preferences"


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Core weights (always applied):
      Mood match:          +3.0  (primary filter signal)
      Genre match:         +2.0  (secondary filter signal)
      Energy similarity:    2.0  (highest ranking feature)
      Danceability:         1.5
      Valence:              1.0
      Tempo (normalized):   0.5
      Acousticness:         0.5

    Optional user_prefs keys for finer control:
      target_danceability  (float 0–1): score by similarity instead of "higher = better"
      target_valence       (float 0–1): score by similarity instead of "higher = better"
      target_tempo_bpm     (float)    : score by BPM proximity instead of "faster = better"
      likes_acoustic       (bool)     : prefer acoustic (True) or electronic (False) sound
      avoid_mood           (str)      : penalise songs whose mood matches this value (-1.5)
      avoid_genre          (str)      : penalise songs whose genre matches this value (-1.0)
    """
    score = 0.0
    reasons = []

    mood_match = song['mood'] == user_prefs.get('mood', '')
    genre_match = song['genre'] == user_prefs.get('genre', '')

    # Mood match — weight 3.0
    if mood_match:
        score += 3.0
        reasons.append(f"mood matches '{song['mood']}'")

    # Genre match — weight 2.0
    if genre_match:
        score += 2.0
        reasons.append(f"genre matches '{song['genre']}'")

    # Mood avoidance penalty — weight -1.5
    avoid_mood = user_prefs.get('avoid_mood', '')
    if avoid_mood and song['mood'] == avoid_mood:
        score -= 1.5
        reasons.append(f"mood '{song['mood']}' is one you want to avoid")

    # Genre avoidance penalty — weight -1.0
    avoid_genre = user_prefs.get('avoid_genre', '')
    if avoid_genre and song['genre'] == avoid_genre:
        score -= 1.0
        reasons.append(f"genre '{song['genre']}' is one you want to avoid")

    target_energy = user_prefs.get('energy', 0.5)

    # Energy similarity — weight 2.0
    energy_sim = 1.0 - abs(target_energy - song['energy'])
    score += 2.0 * energy_sim
    if energy_sim >= 0.85:
        reasons.append(f"energy level close to target ({song['energy']:.2f})")

    # Danceability — weight 1.5
    # If target_danceability is given, score by proximity; otherwise reward higher values.
    if 'target_danceability' in user_prefs:
        dance_sim = 1.0 - abs(user_prefs['target_danceability'] - song['danceability'])
        score += 1.5 * dance_sim
        if dance_sim >= 0.85:
            reasons.append(f"danceability close to target ({song['danceability']:.2f})")
    else:
        score += 1.5 * song['danceability']
        if song['danceability'] >= 0.70:
            reasons.append(f"highly danceable ({song['danceability']:.2f})")

    # Valence — weight 1.0
    # If target_valence is given, score by proximity; otherwise reward higher values.
    if 'target_valence' in user_prefs:
        valence_sim = 1.0 - abs(user_prefs['target_valence'] - song['valence'])
        score += 1.0 * valence_sim
        if valence_sim >= 0.85:
            reasons.append(f"emotional tone close to target ({song['valence']:.2f})")
    else:
        score += 1.0 * song['valence']

    # Tempo — weight 0.5
    # If target_tempo_bpm is given, score by proximity; otherwise reward faster songs.
    song_tempo_norm = max(0.0, min(1.0, (song['tempo_bpm'] - 60) / 120))
    if 'target_tempo_bpm' in user_prefs:
        target_tempo_norm = max(0.0, min(1.0, (user_prefs['target_tempo_bpm'] - 60) / 120))
        tempo_sim = 1.0 - abs(target_tempo_norm - song_tempo_norm)
        score += 0.5 * tempo_sim
        if tempo_sim >= 0.90:
            reasons.append(f"tempo close to target ({song['tempo_bpm']:.0f} BPM)")
    else:
        score += 0.5 * song_tempo_norm

    # Acousticness — weight 0.5
    likes_acoustic = user_prefs.get('likes_acoustic', False)
    acoustic_score = song['acousticness'] if likes_acoustic else (1.0 - song['acousticness'])
    score += 0.5 * acoustic_score
    if likes_acoustic and song['acousticness'] >= 0.70:
        reasons.append(f"acoustic sound matches preference ({song['acousticness']:.2f})")
    elif not likes_acoustic and song['acousticness'] <= 0.25:
        reasons.append(f"electronic sound matches preference ({song['acousticness']:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Steps:
      1. Filter to songs that match the user's mood or genre (at least one).
      2. Score each filtered song using score_song().
      3. Sort by score descending and return the top k as (song, score, explanation).
    """
    user_mood = user_prefs.get('mood', '')
    user_genre = user_prefs.get('genre', '')

    # Filter: keep songs that match at least mood or genre
    filtered = [s for s in songs if s['mood'] == user_mood or s['genre'] == user_genre]

    # Fall back to full catalog if fewer than k songs passed the filter
    if len(filtered) < k:
        filtered = songs

    scored = []
    for song in filtered:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "similar overall audio profile"
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
