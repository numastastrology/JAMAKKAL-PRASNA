import sys, os
from datetime import datetime
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine

# Coordinates for PCA New Cricket Stadium, Tira (Mohali/Chandigarh)
lat = 30.7833 # Approximate for Mullanpur/Tira
lon = 76.7667

dt = datetime(2026, 3, 31, 19, 30, 0)
team_a = "PBKS"
team_b = "GT"

print(f"\n{'='*60}\nIPL MATCH PREDICTION: {team_a} vs {team_b} \n{'='*60}")
je = JamakkalEngine(lat, lon, dt)
jd = je.compute_all()

# Force strict competition
jd['is_strict_competition_mode'] = True

query = f"TEAM A : {team_a}\nTEAM B : {team_b}"
se = SynthesisEngine(jd, query)

try:
    se.generate_synthesis()
    cd = getattr(se, 'cricket_data', {})
    print(f"Udayam Rasi: {se.udayam} | Arudam: {se.arudam} | Kavippu: {se.kavippu}\n")
    print(f"1. WHO WILL WIN THE TOSS: {cd.get('toss_winner', 'Unknown')}")
    print(f"2. WHO WILL BAT FIRST: {cd.get('bat_first', 'Unknown')}")
    print(f"3. BATTING FIRST SCORE: {cd.get('bat_first_score')} runs")
    print(f"4. BATTING SECOND SCORE: {cd.get('bat_second_score')} runs")
    print(f"5. WHO WILL WIN: {cd.get('predicted_winner')} ({cd.get('predicted_margin')})")
    print()
    print("Detailed Outcome Reason:")
    print(cd.get('outcome_reason', '').replace('<br/>', '\n').replace('&bull;', '-').replace('<b>', '').replace('</b>', ''))
except Exception as e:
    print(f"Error: {e}")
