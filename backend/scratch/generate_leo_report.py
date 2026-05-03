import sys
import os
import json
from datetime import datetime

# Add the backend directory to sys.path
sys.path.append(os.path.abspath("c:/Users/kanna/JAMAKKAL PRASNA/backend"))

from engines.jamakkal import JamakkalEngine
from engines.prediction import PredictionEngine
from utils.pdf_generator import PremiumPDFGenerator

def generate_report():
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
    jam_data = je.compute_all()
    jam_data['query_text'] = query
    
    pe = PredictionEngine(jam_data, natal_data)
    report_data = pe.generate_full_report_data()
    
    # Merge jam_data into report_data for the PDF generator
    # The PDF generator expects a combined dictionary
    final_data = {**jam_data, **report_data}
    final_data['natal'] = natal_data
    
    filename = "c:/Users/kanna/JAMAKKAL PRASNA/backend/Verification_Report_Leo.pdf"
    pdf_gen = PremiumPDFGenerator(final_data, filename)
    pdf_gen.generate()
    
    print(f"Report generated: {filename}")

if __name__ == "__main__":
    generate_report()
