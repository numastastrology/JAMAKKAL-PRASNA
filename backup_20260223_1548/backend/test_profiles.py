"""Test that different profiles show SAME astronomical date but DIFFERENT fruition text."""
import sys, datetime as dt, re
sys.path.insert(0, '.')
from engines.jamakkal import JamakkalEngine
from engines.natal import NatalEngine
from engines.prediction import PredictionEngine

qt = dt.datetime.now()
jam = JamakkalEngine(13.0827, 80.2707, qt)
d = jam.compute_all()
d['query_text'] = 'when will I get a job'

profiles = [
    {'name': 'Profile1', 'gender': 'Male', 'birth_date': '1975-10-21', 'birth_time': '01:10:00', 'birth_place': 'Navi Mumbai', 'lat': 19.033, 'lon': 73.029},
    {'name': 'Profile2', 'gender': 'Female', 'birth_date': '1990-05-15', 'birth_time': '14:30:00', 'birth_place': 'Chennai', 'lat': 13.082, 'lon': 80.270},
    {'name': 'Profile3', 'gender': 'Male', 'birth_date': '1985-01-01', 'birth_time': '06:00:00', 'birth_place': 'Delhi', 'lat': 28.613, 'lon': 77.209},
]

for p in profiles:
    ne = NatalEngine(p)
    nd = ne.compute_all()
    pe = PredictionEngine(d, nd)
    r = pe.generate_full_report_data('en')
    
    # Extract the transit date and manifestation date
    rec_points = r.get('recovery_timeline', [])
    rec_text = " ".join(rec_points)
    all_dates = re.findall(r'([A-Z][a-z]+ \d{1,2}, \d{4})', rec_text)
    
    # Extract fruition window
    fruition = pe._get_natal_fruition_window()
    
    lagna = nd.get('Lagna', '?')
    # Phase 3 date comes first in recovery text, then the Shift Factor date
    manifest_date = all_dates[0] if all_dates else '?'
    transit_date = all_dates[1] if len(all_dates) > 1 else '?'
    
    print(f"{p['name']} | Lagna={lagna}")
    print(f"   Transit (Shift) Date: {transit_date}")
    print(f"   Final Manifestation:  {manifest_date}")
    print(f"   Fruition: {fruition}")
    print("-" * 40)
