import os
import sys
import datetime
from engines.jamakkal import JamakkalEngine
from engines.natal import NatalEngine
from engines.prediction import PredictionEngine
from utils.pdf_generator import PremiumPDFGenerator

def verify_final_fixes():
    print("--- Verifying Final Fixes & Elaboration ---")
    
    lat, lon = 13.0827, 80.2707
    query_time = datetime.datetime.now()
    
    jam_engine = JamakkalEngine(lat, lon, query_time)
    jam_data = jam_engine.compute_all()
    # Simulate user query from photo 1
    jam_data['query_text'] = "The native is found very stressed in his job and want to change his job. Whether it is favourable for the native to change the job."
    
    natal_data = {
        "name": "M MANIVANNAN",
        "birth_date": "1985-06-15",
        "birth_time": "10:30:00",
        "birth_place": "Devakottai, Tamil Nadu",
        "lat": 9.9442,
        "lon": 78.8258
    }
    natal_engine = NatalEngine(natal_data)
    n_data = natal_engine.compute_all()
    
    pred_engine = PredictionEngine(jam_data, n_data)
    report = pred_engine.generate_full_report_data()
    report['query_text'] = jam_data['query_text']
    report['name'] = natal_data['name']
    
    print("\n[SYNTHESIS POINTS]")
    for pt in report.get('synthesis_points', []):
        print(f"  {pt}")
        
    print("\n[PREDICTION CHALLENGES (Checking for Elaboration)]")
    # Check Career challenges
    career_challenges = report['balance_categories'].get('Career & Professional', {}).get('challenges', [])
    for c in career_challenges:
        if "Arudham position" in c or "Check for environmental" in c:
            print(f"  [OK] Found elaborative point: {c}")
        else:
            print(f"  {c}")

    print("\n[CHECKING NATAL DATA KEYS for PDF]")
    natal = report.get('natal', {})
    expected_keys = ["Positions", "Degrees", "Nakshatras", "PlanetaryStates"]
    for k in expected_keys:
        if k in natal:
            print(f"  [OK] Key '{k}' found in natal data.")
        else:
            print(f"  [FAIL] Key '{k}' NOT found in natal data!")

    # Generate PDF
    pdf_gen = PremiumPDFGenerator(report, "Final_Verification_Report.pdf")
    filename = pdf_gen.generate()
    print(f"\nPDF Generated: {filename}")

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    verify_final_fixes()
