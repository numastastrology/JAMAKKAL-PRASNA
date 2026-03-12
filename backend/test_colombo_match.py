import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__)))
from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine
from datetime import datetime

print("=" * 70)
print("CRICKET PREDICTION VERIFICATION — NZ vs ENG (7PM Colombo)")
print("=" * 70)

# Colombo Lat/Lon
lat = 6.9271
lon = 79.8612
dt = datetime(2026, 2, 27, 19, 0, 0)

je = JamakkalEngine(lat, lon, dt)
jd = je.compute_all()
qt = 'WHO WILL WIN THE MATCH BETWEEN NEW ZEALAND AND ENGLAND AT COLOMBO'
jd['query_text'] = qt

se = SynthesisEngine(jd, qt)
result = se.generate_synthesis()
cd = getattr(se, 'cricket_data', None)

if cd:
    print(f"\nUdayam={se.udayam}")
    print(f"7th House={ (se.udayam + 6) % 12 or 12 }")
    print(f"Team A: {cd['team_a']}")
    print(f"Team B: {cd['team_b']}")
    print(f"\n1. TOSS WINNER: {cd.get('toss_winner')}")
    print(f"\n2. BAT FIRST: {cd.get('bat_first')}")
    print(f"   BAT SECOND: {cd.get('bat_second')}")
    
    print(f"\n3. BAT FIRST SCORE (with rays): {cd.get('bat_first_score')}")
    raw_reason = cd.get('bat_first_score_reason', '').replace('&bull;', '•').replace('<br/>', '\n')
    print(f"   Reason: {raw_reason}")
    print(f"\n   BAT FIRST SCORE (no rays): {cd.get('bat_first_score_noray')}")
    
    print(f"\n4. BAT SECOND SCORE (with rays): {cd.get('bat_second_score')}")
    raw_reason2 = cd.get('bat_second_score_reason', '').replace('&bull;', '•').replace('<br/>', '\n')
    print(f"   Reason: {raw_reason2}")
    
    print(f"\n5. PREDICTED WINNER: {cd.get('predicted_winner')}")
else:
    print("\n[ERROR] No cricket_data generated!")
