import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__)))
from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine
from datetime import datetime

print("=" * 70)
print("CRICKET PREDICTION VERIFICATION — IND vs ZIM (7PM Chennai)")
print("Actual: ZIM won toss, elected to field. IND batted first 256/4 in 20 overs.")
print("=" * 70)

# IND vs ZIM at 7PM Chennai (Feb 26 2026)
# Note: From the image, India is Lagna side (score 10.7) and Zimbabwe is 7th side (score 7.3)
je = JamakkalEngine(13.0827, 80.2707, datetime(2026, 2, 26, 19, 0, 0))
jd = je.compute_all()
qt = 'India vs Zimbabwe match in Chennai'
jd['query_text'] = qt
# Assuming ZIM toss decision is field
jd['toss_winner'] = 'Zimbabwe'
jd['toss_decision'] = 'Field'
se = SynthesisEngine(jd, qt)

# Run cricket prediction
result = se.generate_synthesis()
cd = getattr(se, 'cricket_data', None)

if cd:
    print("\n" + "=" * 70)
    print("CRICKET PREDICTION RESULTS (WITH RAYS)")
    print("=" * 70)
    print(f"Team A: {cd['team_a']}")
    print(f"Team B: {cd['team_b']}")
    print(f"\n1. TOSS WINNER: {cd['toss_winner']}")
    print(f"   Reason: {cd.get('toss_reason', '')}")
    print(f"\n2. BAT FIRST: {cd['bat_first']}")
    print(f"   BAT SECOND: {cd['bat_second']}")
    print(f"   Reason: {cd.get('bat_first_reason', '')}")
    print(f"\n3. BAT FIRST SCORE (with rays): {cd['bat_first_score']}")
    raw_reason = cd.get('bat_first_score_reason', '').replace('&bull;', '•').replace('<br/>', '\n')
    print(f"   Reason: {raw_reason}")
    print(f"\n   BAT FIRST SCORE (no rays): {cd['bat_first_score_noray']}")
    
    print(f"\n4. BAT SECOND SCORE (with rays): {cd['bat_second_score']}")
    raw_reason2 = cd.get('bat_second_score_reason', '').replace('&bull;', '•').replace('<br/>', '\n')
    print(f"   Reason: {raw_reason2}")
    print(f"\n   BAT SECOND SCORE (no rays): {cd['bat_second_score_noray']}")
    
    print(f"\n5. PREDICTED WINNER: {cd['predicted_winner']}")
    print(f"   Margin: {cd.get('predicted_margin', '')}")
    print(f"   Reason: {cd.get('outcome_reason', '')}")
else:
    print("\n[ERROR] No cricket_data generated!")
