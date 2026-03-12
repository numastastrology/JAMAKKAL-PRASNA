
import datetime as _dt
import sys
import os
import ephem
import math

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from engines.prediction import PredictionEngine
from engines.synthesis import SynthesisEngine

# Mock data where Venus is ruling planet and in Aquarius
# To ensure it looks for the transit to Pisces
jam_data = {
    "planet_positions": {"Venus": 11, "Saturn": 12, "Sun": 11, "Moon": 2},
    "ruling_planet": "Venus",
    "transits": {
        "Venus": {"rasi": "Aquarius", "degree": "10", "abs_deg": 310, "status": "Neutral"},
        "Saturn": {"rasi": "Pisces", "status": "Neutral"}
    },
    "inner_planets": {
        "Udayam": {"rasi_num": 5},
        "Arudam": {"rasi_num": 2},
        "Kavippu": {"rasi_num": 11}
    },
    "query_text": "job change stress"
}

print("--- Testing Venus Natural Transit & Timeline (No Hardcoding) ---")

# Test PredictionEngine
pred = PredictionEngine(jam_data)
transit_dt = pred._get_transit_date_raw()
print(f"Venus Transit Date: {transit_dt.strftime('%B %d, %Y %H:%M:%S')} (IST approx)")

manifest_dt = transit_dt + _dt.timedelta(days=41)
print(f"Phase 3 Date (Transit + 41): {manifest_dt.strftime('%B %d, %Y')}")

report = pred.generate_full_report_data()
final_conclusion = report.get('final_conclusion', '')
print("\n[Final Conclusion Snippet]")
# Find Phase 3 line
for line in final_conclusion.split('<br/>'):
    if "Phase 3" in line or "Full professional manifestation" in line:
        print(f"  {line}")

# Test SynthesisEngine
synth = SynthesisEngine(jam_data, "job change")
lift_dt = synth._get_kavippu_lift_date_raw()
print(f"\nSynthesis Lift Date: {lift_dt.strftime('%B %d, %Y')}")
synth_report = synth.generate_synthesis()
conclusion = synth_report.get('conclusion', '')
print("\n[Synthesis Conclusion Snippet]")
for line in conclusion.split('<br/>'):
    if "Phase 3" in line:
        print(f"  {line}")
