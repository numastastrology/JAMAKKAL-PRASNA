
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
    "query_text": "placeholder"
}

print("--- VERIFYING COMPETITION CATEGORY ---")

def test_query(text):
    print(f"\nQUERY: {text}")
    jam_data['query_text'] = text
    se = SynthesisEngine(jam_data, text)
    print(f"Detected Intent: {se.intent}")
    conclusion = se._generate_conclusion()
    print("Conclusion Preview (first 200 chars):")
    print(conclusion[:200] + "...")
    return se.intent

q1 = "WHAT WILL THE OUTCOME OF TODAY INDIA VS ZIMBABWE CRICKET MATCH PLAYED IN CHENNAI. WHAT SCORE WILL EACH SCORE AND WHO WILL WIN TOSS AND WHO WILL WIN MATCH."
intent1 = test_query(q1)

q2 = "Who will win the upcoming election results for our candidate?"
intent2 = test_query(q2)

if intent1 == "COMPETITION" and intent2 == "COMPETITION":
    print("\n[SUCCESS] Both queries correctly classified as COMPETITION.")
else:
    print("\n[FAILURE] Intent detection mismatch.")
