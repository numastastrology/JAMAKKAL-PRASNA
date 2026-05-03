import sys
import os
import json
from datetime import datetime

# Add the backend directory to sys.path
sys.path.append(os.path.abspath("c:/Users/kanna/JAMAKKAL PRASNA/backend"))

from engines.jamakkal import JamakkalEngine
from engines.prediction import PredictionEngine

def check_now():
    # IST time
    now_dt = datetime.fromisoformat("2026-04-26T21:18:18")
    query = "When promotion is expected and job change shifting is possible from chennai to Bangalore"
    
    # Correct Birth Data: Leo Lagna
    natal_data = {
        "Lagna": "Leo",
        "LagnaRasi": 5,
        "Nakshatra": "Punarvasu",
        "NakshatraRasi": 3,
        "PlanetaryStates": {
            "Sun": "Friend",
            "Moon": "Friend",
            "Mars": "Direct",
            "Mercury": "Direct",
            "Jupiter": "Enemy",
            "Venus": "Retrograde",
            "Saturn": "Retrograde"
        }
    }
    
    lat, lon = 13.08, 80.27 # Chennai
    
    je = JamakkalEngine(lat, lon, now_dt)
    jam_data = je.compute_all() # The method is compute_all(), not calculate()
    jam_data['query_text'] = query
    
    pe = PredictionEngine(jam_data, natal_data)
    report = pe.generate_full_report_data()
    
    print(json.dumps({
        "final_conclusion": report['final_conclusion'],
        "synthesis_conclusion": report['synthesis_conclusion'],
        "ruling_planet": pe.ruling_planet,
        "udayam": pe.udayam,
        "arudam": pe.arudam,
        "kavippu": pe.kavippu
    }, indent=2))

if __name__ == "__main__":
    check_now()
