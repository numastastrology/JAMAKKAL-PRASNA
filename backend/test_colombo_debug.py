import sys, os
from datetime import datetime
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine

lat=6.9271; lon=79.8612; dt=datetime(2026, 2, 27, 19, 0, 0)
je = JamakkalEngine(lat, lon, dt)
jd = je.compute_all()

print(f"Udayam: {jd.get('udayam')} ({je.RASI_NAMES[jd.get('udayam')]})")
print(f"Arudam: {jd.get('arudam')} ({je.RASI_NAMES[jd.get('arudam')]})")
print(f"Kavippu: {jd.get('kavippu')} ({je.RASI_NAMES[jd.get('kavippu')]})")

qt = 'WHO WILL WIN THE MATCH BETWEEN NEW ZEALAND AND ENGLAND AT COLOMBO'
jd['query_text'] = qt
se = SynthesisEngine(jd, qt)
res = se.generate_synthesis()
cd = getattr(se, 'cricket_data', {})

print('Team A (L1):', cd.get('team_a'), 'Strength:', se._get_planet_strength_score(se.house_lords[se.udayam]))
print('Team B (L7):', cd.get('team_b'), 'Strength:', se._get_planet_strength_score(se.house_lords[(se.udayam+6)%12 or 12]))
