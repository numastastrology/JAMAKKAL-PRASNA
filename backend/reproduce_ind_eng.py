
import os
import sys
import datetime
from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine

def reproduce():
    print("--- Reproducing India vs England Match Prediction (Refined) ---")
    
    lat, lon = 13.0827, 80.2707 # Chennai
    
    # Check every 15 minutes on March 5, 2026
    start_time = datetime.datetime(2026, 3, 5, 6, 0)
    end_time = datetime.datetime(2026, 3, 5, 22, 0)
    
    step = datetime.timedelta(minutes=15)
    current = start_time
    
    match_found = False
    
    while current <= end_time:
        jam_engine = JamakkalEngine(lat, lon, current)
        jam_data = jam_engine.compute_all()
        
        # We need India (L1) = Venus and England (L7) = Mars
        # This occurs when Lagna is Taurus or Libra
        udayam = jam_data['inner_planets']['Udayam']
        if isinstance(udayam, dict): udayam = udayam['rasi_num']
        
        if udayam in [2, 7]: # Taurus or Libra
            # Try both name orders as "TEAM A" / "TEAM B" might have been used
            query_text = "TEAM A : India (Suryakumar Yadav)\nTEAM B : England (Harry Brook)"
            jam_data['query_text'] = query_text
            jam_data['is_strict_competition_mode'] = True
            
            engine = SynthesisEngine(jam_data, query_text)
            res = engine._calculate_cricket_prediction()
            
            # Check for the exact score range from screenshot:
            # India: 249-264
            # England: 268-283
            if res['team_a_score'] == "249-264" and res['team_b_score'] == "268-283":
                print(f"\n>>> EXACT MATCH FOUND! <<<")
                print(f"Time: {current.isoformat()}")
                print(f"Udayam: {udayam} ( {'Taurus' if udayam==2 else 'Libra'} )")
                print(f"Ruling Planet: {jam_data.get('ruling_planet')}")
                print(f"India (L1) Significator: {engine.house_lords[udayam]}")
                print(f"England (L7) Significator: {engine.house_lords[(udayam+6)%12 or 12]}")
                print(f"India Score: {res['team_a_score']} (Noray: {res['team_a_score_noray']})")
                print(f"England Score: {res['team_b_score']} (Noray: {res['team_b_score_noray']})")
                print(f"Predicted Winner: {res['predicted_winner']}")
                match_found = True
                break
            elif "249-264" in str(res) or "268-283" in str(res):
                print(f"Near Match at {current.isoformat()}: Ind {res['team_a_score']}, Eng {res['team_b_score']}")

        current += step

    if not match_found:
        print("\nExact match not found in 15-min intervals. Trying 5-min intervals around 11:34 AM...")
        current = datetime.datetime(2026, 3, 5, 11, 0)
        end = datetime.datetime(2026, 3, 5, 12, 0)
        while current <= end:
            jam_engine = JamakkalEngine(lat, lon, current)
            jam_data = jam_engine.compute_all()
            query_text = "TEAM A : India (Suryakumar Yadav)\nTEAM B : England (Harry Brook)"
            jam_data['query_text'] = query_text
            jam_data['is_strict_competition_mode'] = True
            engine = SynthesisEngine(jam_data, query_text)
            res = engine._calculate_cricket_prediction()
            if res['team_a_score'] == "249-264" and res['team_b_score'] == "268-283":
                print(f"\n>>> EXACT MATCH FOUND! <<<")
                print(f"Time: {current.isoformat()}")
                print(f"Udayam: {jam_data['inner_planets']['Udayam']}")
                print(f"India Score: {res['team_a_score']}")
                print(f"England Score: {res['team_b_score']}")
                match_found = True
                break
            current += datetime.timedelta(minutes=1)

if __name__ == "__main__":
    sys.path.append(os.path.join(os.getcwd(), 'backend'))
    reproduce()
