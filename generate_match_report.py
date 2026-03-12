import os
import sys
import json
from datetime import datetime

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from engines.jamakkal import JamakkalEngine
from engines.prediction import PredictionEngine
from utils.pdf_generator import PremiumPDFGenerator

def generate_match_report():
    # Query details
    query_text = "WHO WILL BE WINNING TODAYS CRICKET MATCH BETWEEN SOUTH AFRICA AND WEST INDIES AND WHO WILL WIN TOSS, BAT FIRST AND SCORE HOW MANY RUNS AND BATTING SECOND HOW MUCH THEY SCORE AND WHO IS THE WINNER"
    
    # 3 PM today is the match time, but using CURRENT Prasna time as requested
    now = datetime.now()
    query_time = now # Use current exact time for Prasna chart
    
    # Ahmedabad location
    lat = 23.0225
    lon = 72.5714
    
    print(f"Generating report for: {query_text}")
    print(f"Prasna Time: {query_time}")
    
    # 1. Run Jamakkal Engine
    jam_engine = JamakkalEngine(lat, lon, query_time)
    jam_data = jam_engine.compute_all()
    jam_data['query_text'] = query_text
    jam_data['location'] = "Ahmedabad"
    jam_data['birth_place'] = "N/A"
    
    print("Jamakkal calculated. Udayam:", jam_data['inner_planets']['Udayam']['rasi'])
    
    # 2. Run Prediction Engine
    pred_engine = PredictionEngine(jam_data, {})
    full_data = pred_engine.generate_full_report_data("en")
    
    # Add required top-level fields for PDF generator
    full_data['query_text'] = query_text
    full_data['name'] = "Sports Oracle"
    full_data['gender'] = "N/A"
    full_data['natal'] = {}
    full_data['query_time_str'] = query_time.strftime("%Y-%m-%d %H:%M:%S")
    full_data['analysis_mode'] = "prasna_only"
    
    # 3. Generate PDF
    filename = f"SA_vs_WI_Match_Report_{now.strftime('%H%M%S')}.pdf"
    output_path = os.path.join(os.getcwd(), filename)
    
    gen = PremiumPDFGenerator(full_data, output_path)
    gen.generate()
    
    print(f"\nReport successfully generated: {output_path}")

if __name__ == "__main__":
    generate_match_report()
