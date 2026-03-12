"""
Generate cricket PDF for India vs NZ match (Ahmedabad, Mar 8 2026, 7PM IST).
This is intended to verify that the updated synthesis.py correctly generates
scores in the 248-263 (India) and 165-180 (NZ) ranges.
"""
import os
import sys
from datetime import datetime, timezone, timedelta

sys.path.append(os.path.join(os.getcwd(), 'backend'))

from engines.jamakkal import JamakkalEngine
from engines.prediction import PredictionEngine
from utils.pdf_generator import PremiumPDFGenerator

def generate_report():
    query_text = "cricket match between India (Suryakumar Yadav) vs New Zealand (Mitchell Santner) at Ahmedabad. New Zealand won toss and elected to field."

    # Match time: Mar 8, 2026 7PM IST (naive, since JamakkalEngine expects naive)
    match_time = datetime(2026, 3, 8, 19, 0, 0)

    # Ahmedabad coordinates
    lat = 23.0225
    lon = 72.5714

    print(f"Generating report for: {query_text}")
    print(f"Match Time: {match_time}")

    # 1. Run Jamakkal Engine
    jam_engine = JamakkalEngine(lat, lon, match_time)
    jam_data = jam_engine.compute_all()
    jam_data['query_text'] = query_text
    jam_data['query_time'] = match_time.isoformat()
    jam_data['location'] = "Ahmedabad"
    jam_data['latitude'] = lat
    jam_data['longitude'] = lon
    jam_data['birth_place'] = "N/A"
    jam_data['toss_winner'] = "New Zealand"
    jam_data['toss_decision'] = "field"
    jam_data['is_strict_competition_mode'] = True

    print("Jamakkal calculated. Udayam:", jam_data['inner_planets']['Udayam']['rasi'])

    # 2. Run Prediction Engine
    pred_engine = PredictionEngine(jam_data, {})
    full_data = pred_engine.generate_full_report_data("en")

    # Add required top-level fields for PDF generator
    full_data['query_text'] = query_text
    full_data['name'] = "Sports Oracle"
    full_data['gender'] = "N/A"
    full_data['natal'] = {}
    full_data['query_time_str'] = match_time.strftime("%Y-%m-%d %H:%M:%S")
    full_data['analysis_mode'] = "prasna_only"
    full_data['is_strict_competition_mode'] = True

    # 3. Print verification
    cd = full_data.get('cricket_data', {})
    print(f"\n=== SCORE VERIFICATION ===")
    print(f"Bat First: {cd.get('bat_first')}, Score: {cd.get('bat_first_score')}")
    print(f"Bat Second: {cd.get('bat_second')}, Score: {cd.get('bat_second_score')}")
    print(f"Winner: {cd.get('predicted_winner')}")
    
    # 4. Generate PDF
    filename = f"Ind_vs_NZ_Ahmedabad_Report.pdf"
    output_path = os.path.join(os.getcwd(), filename)
    gen = PremiumPDFGenerator(full_data, output_path)
    gen.generate()
    print(f"\nPDF saved: {output_path}")

if __name__ == "__main__":
    generate_report()
