import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__)))
from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine
from datetime import datetime

print("=" * 70)
print('CRICKET PREDICTION VERIFICATION — IND vs ZIM (7 PM Chennai, Yesterday)')
print("=" * 70)

je = JamakkalEngine(13.0827, 80.2707, datetime(2026, 2, 26, 19, 0, 0))
jd = je.compute_all()
qt = 'WHO WILL BE WINNING TODAYS CRICKET MATCH BETWEEN INDIA AND ZIMBABWE'
jd['query_text'] = qt
jd['toss_winner'] = 'Zimbabwe'
jd['toss_decision'] = 'field'

se = SynthesisEngine(jd, qt)
cd = se._calculate_cricket_prediction()

print(f'\n1. TOSS WINNER: {cd["toss_winner"]}')
print(f'\n2. BAT FIRST: {cd["bat_first"]}')
print(f'   BAT SECOND: {cd["bat_second"]}')
print(f'\n3. BAT FIRST SCORE: {cd["bat_first_score"]}')
print(f'   Reason: {cd["bat_first_score_reason"].replace("<br/>", "\n")}')
print(f'\n4. BAT SECOND SCORE: {cd["bat_second_score"]}')
print(f'   Reason: {cd["bat_second_score_reason"].replace("<br/>", "\n")}')
print(f'\n5. PREDICTED WINNER: {cd["predicted_winner"]}')
print(f'   Margin: {cd.get("predicted_margin", "")}')
print(f'   Outcome Reason: {cd.get("outcome_reason", "").replace("<br/>", "\n")}')
