import os
import sys
import datetime
from engines.jamakkal import JamakkalEngine
from engines.natal import NatalEngine
from engines.prediction import PredictionEngine
from utils.pdf_generator import PremiumPDFGenerator

def test_synthesis():
    print("--- Verifying Synthesis Feature ---")
    
    lat, lon = 12.9716, 77.5946 # Bengaluru (from photo)
    # 2026-02-20 17:14:00 (from photo)
    query_time = datetime.datetime(2026, 2, 20, 17, 14, 0)
    
    jam_engine = JamakkalEngine(lat, lon, query_time)
    jam_data = jam_engine.compute_all()
    print(f"[OK] Jamakkal compute done. Block: {jam_data['block']}")
    
    natal_data = {} # Assuming no natal for initial test
    
    pred_engine = PredictionEngine(jam_data, natal_data)
    report_data = pred_engine.generate_full_report_data()
    print("[OK] Prediction report generation done.")
    
    if "synthesis_points" in report_data:
        print(f"[OK] Synthesis points found: {len(report_data['synthesis_points'])}")
        for pt in report_data['synthesis_points']:
            print(f"  - {pt}")
    else:
        print("[FAIL] No synthesis_points in report_data.")
        
    if "synthesis_conclusion" in report_data:
        print(f"[OK] Synthesis conclusion: {report_data['synthesis_conclusion']}")
    else:
        print("[FAIL] No synthesis_conclusion in report_data.")

    # Generate PDF
    pdf_gen = PremiumPDFGenerator(report_data, "Test_Synthesis_Report.pdf")
    filename = pdf_gen.generate()
    if os.path.exists(filename):
        print(f"\n[SUCCESS] PDF Generated at {filename}")
    else:
        print("[FAIL] PDF generation failed.")

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    test_synthesis()
