
import datetime as _dt
import sys
import os
import io

# Fix Unicode issues in Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from engines.synthesis import SynthesisEngine

# Mock data for Colombo match evaluation
# Sri Lanka vs New Zealand
jam_data = {
    "lat": 6.9271,
    "lon": 79.8612,
    "planet_positions": {
        "Sun": 11, "Mars": 11, "Jupiter": 2, "Mercury": 12, "Venus": 11, "Saturn": 11, "Moon": 4, "Snake": 7
    },
    "ruling_planet": "Venus",
    "transits": {
        "Sun": {"rasi_num": 11, "status": "Neutral"},
        "Mars": {"rasi_num": 11, "status": "Neutral"},
        "Jupiter": {"rasi_num": 2, "status": "Neutral"},
        "Mercury": {"rasi_num": 12, "status": "Debilitated"},
        "Venus": {"rasi_num": 11, "status": "Friendly"},
        "Saturn": {"rasi_num": 11, "status": "Own"},
        "Moon": {"rasi_num": 4, "status": "Own"},
        "Snake": {"rasi_num": 7, "status": "Enemy"}
    },
    "inner_planets": {
        "Udayam": {"rasi_num": 6}, # Virgo Lagna
        "Arudam": {"rasi_num": 3},
        "Kavippu": {"rasi_num": 12}
    },
    "query_time": "2026-02-25T16:45:00",
    "query_text": "placeholder"
}

def test_cricket(text):
    print(f"\nQUERY: {text}")
    jam_data['query_text'] = text
    se = SynthesisEngine(jam_data, text)
    print(f"Detected Intent: {se.intent}")
    conclusion = se._generate_conclusion()
    print("\n--- CONCLUSION OUTPUT ---")
    print(conclusion)
    
    if hasattr(se, 'cricket_data'):
        print("\n[CRICKET DATA FOUND]")
        print(f"Toss Winner: {se.cricket_data['toss_winner']}")
        print(f"Team A Score: {se.cricket_data['team_a_score']} ({se.cricket_data['team_a_interp']})")
        print(f"Team B Score: {se.cricket_data['team_b_score']} ({se.cricket_data['team_b_interp']})")
        print(f"Winner: {se.cricket_data['predicted_winner']}")

print("--- VERIFYING CRICKET PREDICTION WORKSHEET ---")

# Test Case 1: Pakistan vs England (Simulating Pallekele 10 AM)
jam_data['query_text'] = "Pakistan vs England match"
jam_data['inner_planets'] = {
    "Udayam": {"rasi_num": 9}, # Sagittarius (Pakistan Lagna)
    "Arudam": {"rasi_num": 12},
    "Kavippu": {"rasi_num": 3}
}
# Mock L1 (Jupiter) slightly weak in 8H, L7 (Mercury) slightly strong
# Moon in 4 (Cancer) is 8H from Lagna (Afflicted), 2H from 7H (Steady)
jam_data['transits'] = {
    "Jupiter": {"rasi_num": 4, "status": "Neutral"}, # L1 (score 2)
    "Mercury": {"rasi_num": 2, "status": "Neutral"},  # L7 (score 2)
    "Saturn": {"rasi_num": 10, "status": "Own"},            # 2H from UDM (Malefic on 2)
    "Moon": {"rasi_num": 4, "status": "Neutral"},          # Afflicted for A (8H), Steady for B (2H)
    "Snake": {"rasi_num": 1, "status": "Enemy"}
}
jam_data['planet_positions'] = {k: v['rasi_num'] for k, v in jam_data['transits'].items()}

test_cricket("Pakistan vs England match Pallekele 10 AM")

# Test Case 2: Colombo example
# Reset to Colombo logic
jam_data['query_text'] = "New Zealand vs Sri Lanka cricket match in Colombo at 4:45 PM"
# ... old colombo mock could go here but let's just run another case
q2 = "Who will win the match between India vs Zimbabwe in Chennai?"
test_cricket(q2)
