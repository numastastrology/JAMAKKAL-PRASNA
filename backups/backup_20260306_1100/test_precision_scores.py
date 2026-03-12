
import sys
import os
# Mock a few things since we're outside the full engine
class MockJamakkal:
    def __init__(self, data):
        self.data = data
    def get(self, k, default=None):
        return self.data.get(k, default)

from engines.synthesis import SynthesisEngine

def test_precision():
    print("--- Precision Verification: India (Mars, 18.2) vs England (Venus, 17.3) ---")
    
    # Mock jam_data to match user's screenshot exactly
    jam_data = {
        'udayam': 1, # Lagna at Aries -> Mars
        'house_lords': {1: 'Mars', 2: 'Venus', 3: 'Mercury', 4: 'Moon', 5: 'Sun', 6: 'Mercury', 7: 'Venus', 8: 'Mars', 9: 'Jupiter', 10: 'Saturn', 11: 'Saturn', 12: 'Jupiter'},
        'positions': {
            'Jama Mars': 1, # Lagna
            'Jama Venus': 7, # Descendant
            'Jama Sun': 5, 'Jama Moon': 4, 'Jama Mercury': 3, 'Jama Jupiter': 9, 'Jama Saturn': 10, 'Jama Snake': 8,
            'Mars': 1, 'Venus': 7, 'Sun': 5, 'Moon': 4, 'Mercury': 3, 'Jupiter': 9, 'Saturn': 10, 'Snake': 8
        },
        'planet_strengths': {'Mars': 18.2, 'Venus': 17.3, 'Sun': 15.0, 'Jupiter': 14.0, 'Saturn': 13.0, 'Mercury': 12.0, 'Moon': 11.0},
        'transits': {'Mars': {'status': ''}, 'Venus': {'status': ''}},
        'ruling_planet': 'Venus', 
        'latitude': 18.9389,
        'longitude': 72.8258,
        'query_text': "India (Suryakumar Yadav) vs England (Harry Brook)\nVenue: Wankhede, Mumbai",
        'is_strict_competition_mode': True,
        'toss_winner': 'England',
        'toss_decision': 'Elects to Bowl / Field'
    }
    
    # The SynthesisEngine takes the result of JamakkalEngine.compute_all()
    engine = SynthesisEngine(jam_data, jam_data['query_text'])
    res = engine._calculate_cricket_prediction()
    
    bat_first = res['bat_first']
    bat_second = res['bat_second']
    
    print(f"Batting First: {bat_first} -> Score: {res['bat_first_score']}")
    print(f"Batting Second: {bat_second} -> Score: {res['bat_second_score']}")
    print(f"Predicted Winner: {res['predicted_winner']}")
    
    def mid(r): mn, mx = map(int, r.split('-')); return (mn+mx)/2
    score_a = mid(res['bat_first_score'])
    score_b = mid(res['bat_second_score'])
    
    print(f"DEBUG: Score 1={score_a}, Score 2={score_b}")
    
    if "India" in res['predicted_winner']:
        print("[SUCCESS] India wins!")
    else:
        print("[FAIL] England still wins.")

if __name__ == "__main__":
    # Ensure current dir is Jamakkal Prasna root
    sys.path.append(os.path.join(os.getcwd(), 'backend'))
    test_precision()
