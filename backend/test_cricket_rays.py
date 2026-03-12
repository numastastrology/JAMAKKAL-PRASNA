import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__)))
from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine
from datetime import datetime

print("=" * 70)
print("CRICKET PREDICTION VERIFICATION — SA vs WI (3PM Ahmedabad)")
print("Actual: SA won toss, elected to field. WI batted first 176/8.")
print("        SA chased 177/1. SA WON easily.")
print("=" * 70)

# Exact match details from user query
je = JamakkalEngine(23.0225, 72.5714, datetime(2026, 2, 26, 15, 0, 0))
jd = je.compute_all()
qt = 'WHO WILL BE WINNING TODAYS CRICKET MATCH BETWEEN SOUTH AFRICA AND WEST INDIES AND WHO WILL WIN TOSS, BAT FIRST AND SCORE HOW MANY RUNS AND BATTING SECOND HOW MUCH THEY SCORE AND WHO IS THE WINNER'
jd['query_text'] = qt
# "toss_winner" not explicitly provided in the simple test, so let the system decide or we force it if needed
# The photo has "South Africa Batting Second"
se = SynthesisEngine(jd, qt)

result = se.generate_synthesis()
cd = getattr(se, 'cricket_data', None)

if cd:
    print(f"\nUdayam={se.udayam}")
    print(f"7th House={ (se.udayam + 6) % 12 or 12 }")
    print(f"Team A: {cd['team_a']}")
    print(f"Team B: {cd['team_b']}")
    print(f"\n1. TOSS WINNER: {cd['toss_winner']}")
    print(f"\n2. BAT FIRST: {cd['bat_first']}")
    print(f"   BAT SECOND: {cd['bat_second']}")
    
    print(f"\n3. BAT FIRST SCORE (with rays): {cd['bat_first_score']}")
    raw_reason = cd.get('bat_first_score_reason', '').replace('&bull;', '•').replace('<br/>', '\n')
    print(f"   Reason: {raw_reason}")
    print(f"\n   BAT FIRST SCORE (no rays): {cd['bat_first_score_noray']}")
    
    print(f"\n4. BAT SECOND SCORE (with rays): {cd['bat_second_score']}")
    raw_reason2 = cd.get('bat_second_score_reason', '').replace('&bull;', '•').replace('<br/>', '\n')
    print(f"   Reason: {raw_reason2}")
    
    print(f"\n5. PREDICTED WINNER: {cd['predicted_winner']}")
else:
    print("\n[ERROR] No cricket_data generated!")
