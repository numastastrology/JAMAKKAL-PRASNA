
import os
import sys
import datetime
from engines.jamakkal import JamakkalEngine
from engines.prediction import PredictionEngine
from utils.pdf_generator import PremiumPDFGenerator

def verify_competition():
    print("--- Verifying Competition PDF Report ---")
    
    # 1. Setup Engines
    lat, lon = 13.0827, 80.2707 # Chennai
    query_time = datetime.datetime.now()
    
    jam_engine = JamakkalEngine(lat, lon, query_time)
    jam_data = jam_engine.compute_all()
    
    # Force competition mode
    jam_data['query_text'] = "TEAM A : India (Suryakumar Yadav)\nTEAM B : England (Harry Brook)"
    jam_data['is_strict_competition_mode'] = True
    jam_data['toss_winner'] = "" # Test empty string fallback
    jam_data['location'] = "Chennai"
    
    pred_engine = PredictionEngine(jam_data, {})
    report_data = pred_engine.generate_full_report_data()
    
    # Verify toss data in report_data
    cd = report_data.get('cricket_data', {})
    print(f"Toss Winner: {cd.get('toss_winner')}")
    print(f"Toss Reason: {cd.get('toss_reason')}")
    
    # 2. Generate PDF
    pdf_gen = PremiumPDFGenerator(report_data, "Test_Toss_Report.pdf")
    filename = pdf_gen.generate()
    
    if os.path.exists(filename):
        print(f"[SUCCESS] PDF Generated: {filename} (Size: {os.path.getsize(filename)} bytes)")
    else:
        print("[FAIL] PDF file not found.")

if __name__ == "__main__":
    verify_competition()
