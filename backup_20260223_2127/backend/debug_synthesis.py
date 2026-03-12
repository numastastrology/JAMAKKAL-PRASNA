
import datetime as _dt
import sys
import os

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from engines.synthesis import SynthesisEngine

# Simulate user query from photo (Venus block in 7H)
now = _dt.datetime.now()
jam_data = {
    "lat": 13.08,
    "lon": 80.27,
    "planet_positions": {"Venus": 11, "Saturn": 12}, # Venus in Aquarius
    "ruling_planet": "Venus",
    "transits": {
        "Venus": {"rasi": "Aquarius", "degree": "22", "abs_deg": 322, "status": "Neutral"}
    },
    "inner_planets": {
        "Udayam": {"rasi_num": 5}, # Leo Lagna
        "Arudam": {"rasi_num": 10}, # Taurus (10H from UDM)
        "Kavippu": {"rasi_num": 11} # Aquarius (7H from UDM) - Matches screenshot!
    },
    "query_time": now.isoformat(),
    "query_text": "the native is jobless from march 2025 and when employment could happen"
}

print("--- EXAMINING SYNTHESIS ENGINE OUTPUT ---")
se = SynthesisEngine(jam_data, jam_data['query_text'])

lift_date = se._get_kavippu_lift_date_raw()
print(f"DEBUG: lift_date = {lift_date}")

final_manifest_date = (lift_date + _dt.timedelta(days=41)).strftime('%B %d, %Y')
print(f"DEBUG: final_manifest_date (lift + 41d) = {final_manifest_date}")

conclusion = se._generate_conclusion()
print("\n--- CONCLUSION START ---")
print(conclusion)
print("--- CONCLUSION END ---")

if "[V-20260223-CORE-FIXED]" in conclusion:
    print("\n[SUCCESS] Found new version tag!")
else:
    print("\n[ERROR] Version tag MISSING.")

if "March" in conclusion and "April" in conclusion:
    print("[SUCCESS] Found March (Transit) and April (Phase 3) in conclusion.")
else:
    print("[ERROR] Date logic still seems off in text.")
