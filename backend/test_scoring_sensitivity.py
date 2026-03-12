import os
import sys
import datetime
import json
from engines.jamakkal import JamakkalEngine
from engines.prediction import PredictionEngine

def test_scoring_sensitivity():
    print("--- Verifying Scoring Sensitivity ---")
    
    lat, lon = 12.9716, 77.5946 # Bengaluru
    query_time = datetime.datetime(2026, 2, 20, 17, 14, 0)
    
    jam_engine = JamakkalEngine(lat, lon, query_time)
    jam_data = jam_engine.compute_all()
    
    # Profile 1: Favorable (Trine Lagna + Strong Saturn for Career)
    natal_favorable = {
        "Lagna": "Virgo",
        "LagnaRasi": 6, # Trine to Udayam (approximate, if Udayam is in Taurus/Capricorn)
        "PlanetaryStates": {
            "Saturn": "Direct (Friend)",
            "Sun": "Direct (Friend)",
            "Venus": "Direct (Friend)"
        },
        "HouseLords": {
            "10th": "Mercury",
            "7th": "Jupiter"
        }
    }
    
    # Profile 2: Unfavorable (Dusthana Lagna + Weak Saturn for Career)
    natal_unfavorable = {
        "Lagna": "Scorpio",
        "LagnaRasi": 8, # Dusthana to Udayam
        "PlanetaryStates": {
            "Saturn": "Direct (Enemy)",
            "Sun": "Direct (Enemy)",
            "Venus": "Direct (Enemy)"
        },
        "HouseLords": {
            "10th": "Sun",
            "7th": "Mars"
        }
    }

    # Profile 3: No Natal (Should give base Jamakkol score)
    natal_none = {}

    engines = [
        ("Favorable Profile", PredictionEngine(jam_data, natal_favorable)),
        ("Unfavorable Profile", PredictionEngine(jam_data, natal_unfavorable)),
        ("No Natal Profile", PredictionEngine(jam_data, natal_none))
    ]

    udayam_rasi = jam_data['inner_planets']['Udayam']['rasi_num']
    print(f"\nUdayam is in Rasi: {udayam_rasi}")
    
    for label, engine in engines:
        print(f"\nResults for {label}:")
        report_data = engine.generate_full_report_data()
        
        # In PredictionEngine.generate_full_report_data, all_cat_data is returned in the dict?
        # Let's check the keys
        # print(f"Keys: {report_data.keys()}") 
        
        # Based on PredictionEngine return: "balance_categories": all_cat_data
        categories = report_data.get("balance_categories", {})
        
        for cat_name in ["Career & Professional", "Health & Recovery", "Marriage & Relationship"]:
            cat_data = categories.get(cat_name, {})
            score = cat_data.get("score", "N/A")
            status = cat_data.get("status", "N/A")
            print(f"  - {cat_name}: Score = {score}, Status = {status}")

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    test_scoring_sensitivity()
