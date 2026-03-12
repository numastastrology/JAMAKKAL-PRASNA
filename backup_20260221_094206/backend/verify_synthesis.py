import os
import sys
import datetime
from engines.jamakkal import JamakkalEngine
from engines.natal import NatalEngine
from engines.prediction import PredictionEngine
from utils.pdf_generator import PremiumPDFGenerator

def verify():
    print("--- Professional Jamakkol Synthesis Verification ---")
    
    # 1. Setup Engines
    lat, lon = 13.0827, 80.2707 # Chennai
    query_time = datetime.datetime.now()
    
    jam_engine = JamakkalEngine(lat, lon, query_time)
    jam_data = jam_engine.compute_all()
    print(f"[OK] JamakkalEngine compute_all() successful. Block: {jam_data['block']}")
    
    natal_engine = NatalEngine({"name": "Test Native", "gender": "Male"})
    natal_data = natal_engine.compute_all()
    print(f"[OK] NatalEngine compute_all() successful. Lagna: {natal_data['Lagna']}")
    
    pred_engine = PredictionEngine(jam_data, natal_data)
    report_data = pred_engine.generate_full_report_data()
    print("[OK] PredictionEngine report generation successful.")
    
    # 2. Verify Data Structures
    categories = report_data.get('balance_categories', {})
    if not categories:
        print("[FAIL] No balance_categories found.")
        return
    
    print(f"\nVerifying Categories ({len(categories)}):")
    for cat, data in categories.items():
        if "challenges" in data and "solutions" in data:
            if len(data["challenges"]) == 10 and len(data["solutions"]) == 10:
                print(f"  [OK] {cat}: 10 Challenges & 10 Solutions present.")
            else:
                print(f"  [FAIL] {cat}: Incorrect point count. ({len(data['challenges'])}/{len(data['solutions'])})")
        else:
            print(f"  [FAIL] {cat}: Missing fields. Data: {data.keys()}")
            
    # 3. Verify Deep Analysis
    for key in ["diagnostic_analysis", "recovery_timeline", "remedies"]:
        points = report_data.get(key, [])
        if len(points) >= 1:
            print(f"[OK] {key} has {len(points)} points.")
        else:
            print(f"[FAIL] {key} is empty.")

    # 4. Verify PDF Generation
    pdf_gen = PremiumPDFGenerator(report_data, "Verification_Report.pdf")
    try:
        filename = pdf_gen.generate()
        if os.path.exists(filename):
            print(f"\n[SUCCESS] PDF Generated: {filename} (Size: {os.path.getsize(filename)} bytes)")
        else:
            print("[FAIL] PDF file not found after generation.")
    except Exception as e:
        print(f"[FAIL] PDF Generation crashed: {e}")

if __name__ == "__main__":
    # Ensure we can import from local directory
    sys.path.append(os.getcwd())
    verify()
