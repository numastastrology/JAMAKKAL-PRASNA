
import os
import sys
import datetime
from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine

def reproduce():
    print("--- Reproducing Missing Toss Winner Issue ---")
    
    # 1. Setup Data
    lat, lon = 13.0827, 80.2707
    query_time = datetime.datetime.now()
    
    jam_engine = JamakkalEngine(lat, lon, query_time)
    jam_data = jam_engine.compute_all()
    
    # Simulate the data as prepared in main.py for a match
    jam_data['query_text'] = "TEAM A : India (Suryakumar Yadav)\nTEAM B : England (Harry Brook)"
    jam_data['is_strict_competition_mode'] = True
    
    # Case 1: toss_winner is None (Should use calculated)
    jam_data['toss_winner'] = None
    engine1 = SynthesisEngine(jam_data, jam_data['query_text'])
    res1 = engine1._calculate_cricket_prediction()
    print(f"Case 1 (toss_winner=None): {res1['toss_winner']}")
    
    # Case 2: toss_winner is empty string (Likely issue)
    jam_data['toss_winner'] = ""
    engine2 = SynthesisEngine(jam_data, jam_data['query_text'])
    res2 = engine2._calculate_cricket_prediction()
    print(f"Case 2 (toss_winner=''): '{res2['toss_winner']}'")
    
    if res2['toss_winner'] == "":
        print("[FAIL] Reproduction successful: empty string preserved as toss winner.")
    else:
        print("[OK] Reproduction failed: empty string replaced by default.")

if __name__ == "__main__":
    reproduce()
