import sys, os
from datetime import datetime
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine

matches = [
    {
        "name": "RCB vs SRH",
        "lat": 17.3850,
        "lon": 78.4867, # Hyderabad/Telangana approx coords
        "dt": datetime(2026, 3, 28, 14, 34, 44),
        "team_a": "RCB",
        "team_b": "SRH",
        "toss_winner": "RCB",
        "toss_decision": "field"
    },
    {
        "name": "RR vs CSK",
        "lat": 17.3850,
        "lon": 78.4867,
        "dt": datetime(2026, 3, 30, 18, 7, 57),
        "team_a": "CSK",
        "team_b": "RR",
        "toss_winner": "RR",
        "toss_decision": "field"
    }
]

for m in matches:
    print(f"\n{'='*60}\nIPL MATCH PREDICTION: {m['name']} \n{'='*60}")
    je = JamakkalEngine(m['lat'], m['lon'], m['dt'])
    jd = je.compute_all()
    # Force strict competition
    jd['is_strict_competition_mode'] = True
    jd['toss_winner'] = m['toss_winner']
    jd['toss_decision'] = m['toss_decision']
    
    query = f"TEAM A : {m['team_a']}\nTEAM B : {m['team_b']}"
    se = SynthesisEngine(jd, query)
    
    try:
        se.generate_synthesis()
        cd = getattr(se, 'cricket_data', {})
        print(f"Udayam Rasi: {se.udayam} | Arudam: {se.arudam} | Kavippu: {se.kavippu}\n")
        print(f"1. WHO WILL WIN THE TOSS: {cd.get('toss_winner', 'Unknown')}")
        print(f"2. WHO WILL BAT FIRST: {cd.get('bat_first', 'Unknown')}")
        print(f"3. BATTING FIRST ({cd.get('bat_first')}): {cd.get('bat_first_score')} runs")
        print(f"4. BATTING SECOND ({cd.get('bat_second')}): {cd.get('bat_second_score')} runs")
        print(f"5. WHO WILL WIN: {cd.get('predicted_winner')} ({cd.get('predicted_margin')})")
        print()
        print("Detailed Outcome Reason:")
        print(cd.get('outcome_reason', '').replace('<br/>', '\n').replace('&bull;', '-'))
    except Exception as e:
        print(f"Error: {e}")
