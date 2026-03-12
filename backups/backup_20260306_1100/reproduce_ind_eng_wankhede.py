
import os
import sys
import datetime
from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine

def reproduce():
    print("--- Verifying India vs England Fix (Wankhede, 7 PM, Eng elected to Field) ---")
    
    # Wankhede, Mumbai coordinates
    lat, lon = 18.9389, 72.8258
    # 18:56:00 matches the Venus-Mars significator transition in the user's report
    query_time = datetime.datetime(2026, 3, 5, 18, 56, 0)
    
    jam_engine = JamakkalEngine(lat, lon, query_time)
    jam_data = jam_engine.compute_all()
    
    # Simulate captured fields from the screenshot
    # Include Wankhede/Mumbai to trigger venue bonus
    jam_data['query_text'] = "TEAM A : India (Suryakumar Yadav)\nTEAM B : England (Harry Brook)\nVenue: Wankhede, Mumbai"
    jam_data['is_strict_competition_mode'] = True
    jam_data['toss_winner'] = "England"
    jam_data['toss_decision'] = "Elects to Bowl / Field"
    
    engine = SynthesisEngine(jam_data, jam_data['query_text'])
    res = engine._calculate_cricket_prediction()
    
    print(f"Time: {query_time.isoformat()}")
    print(f"Captured Toss: {jam_data['toss_winner']} elected to {jam_data['toss_decision']}")
    
    print(f"\nReport Output:")
    print(f"1. TOSS WINNER: {res['toss_winner']}")
    print(f"2. BAT FIRST: {res['bat_first']}")
    print(f"3. BAT SECOND: {res['bat_second']}")
    print(f"4. BAT FIRST SCORE ({res['bat_first']}): {res['bat_first_score']}")
    print(f"5. BAT SECOND SCORE ({res['bat_second']}): {res['bat_second_score']}")
    print(f"6. PREDICTED WINNER: {res['predicted_winner']}")
    
    # Validation
    success = True
    if "India" not in res['bat_first']:
        print(f"[FAIL] Expected India to bat first (since England elected to field).")
        success = False
    
    def mid(r): mn, mx = map(int, r.split('-')); return (mn+mx)/2
    
    # Correctly identify scores by team name
    if "India" in res['bat_first']:
        ind_mid = mid(res['bat_first_score'])
        eng_mid = mid(res['bat_second_score'])
    else:
        ind_mid = mid(res['bat_second_score'])
        eng_mid = mid(res['bat_first_score'])
    
    print(f"DEBUG: India Mid={ind_mid}, England Mid={eng_mid}")
    
    if ind_mid > eng_mid and "India" not in res['predicted_winner']:
        print(f"[FAIL] Consistency Error: India has more runs but isn't the winner.")
        success = False
    elif eng_mid > ind_mid and "England" not in res['predicted_winner']:
        print(f"[FAIL] Consistency Error: England has more runs but isn't the winner.")
        success = False
        
    if "close-fought" not in res['predicted_margin'] and abs(ind_mid - eng_mid) < 20:
        print(f"[FAIL] 'Close-fought' not in margin even though gap is small.")
        success = False
        
    if "Lagna Dominance" not in res['outcome_reason'] and "Descendant Resilience" not in res['outcome_reason']:
        print(f"[FAIL] Elaborate reasoning missing from outcome_reason.")
        success = False
        
    print(f"\nDETAILED VERDICT:\n{res['outcome_reason']}")
        
    if success:
        print("\n[SUCCESS] Fix verified! Mapping is stable and batting order respects toss.")

def verify_symmetry():
    print("\n--- Verifying Input Order Symmetry (India vs England vs England vs India) ---")
    lat, lon = 18.9389, 72.8258
    query_time = datetime.datetime(2026, 3, 5, 18, 56, 0)
    
    orders = [
        "TEAM A : India (Suryakumar Yadav)\nTEAM B : England (Harry Brook)",
        "TEAM A : England (Harry Brook)\nTEAM B : India (Suryakumar Yadav)"
    ]
    
    results = []
    for q_text in orders:
        jam_engine = JamakkalEngine(lat, lon, query_time)
        jam_data = jam_engine.compute_all()
        jam_data['query_text'] = q_text + "\nVenue: Wankhede, Mumbai"
        jam_data['is_strict_competition_mode'] = True
        jam_data['toss_winner'] = "England"
        jam_data['toss_decision'] = "Elects to Bowl / Field"
        
        engine = SynthesisEngine(jam_data, jam_data['query_text'])
        res = engine._calculate_cricket_prediction()
        
        # Get score for India
        ind_score = res['bat_first_score'] if "India" in res['bat_first'] else res['bat_second_score']
        results.append((res['predicted_winner'], ind_score))
        print(f"Input Order: {q_text.splitlines()[0]} -> Winner: {res['predicted_winner']}, India Score: {ind_score}")

    if results[0] == results[1]:
        print("[SUCCESS] Symmetry Verified! Input order does not change the result.")
    else:
        print("[FAIL] Symmetry Error: Results differ based on input order.")

if __name__ == "__main__":
    sys.path.append(os.path.join(os.getcwd(), 'backend'))
    reproduce()
    verify_symmetry()
