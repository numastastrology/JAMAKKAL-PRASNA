import os
import sys
import datetime
from engines.jamakkal import JamakkalEngine
from engines.natal import NatalEngine
from engines.prediction import PredictionEngine
from utils.pdf_generator import PremiumPDFGenerator

def test_chart():
    # Setup sample data
    lat, lon = 12.9716, 77.5946 # Bengaluru
    q_time = datetime.datetime.now()
    
    jam_engine = JamakkalEngine(lat, lon, q_time)
    jam_data = jam_engine.compute_all()
    jam_data['query_text'] = "Will I get a promotion this year?"
    
    # Mock some natal data if needed
    natal_data = {
        "name": "Test User",
        "gender": "Male",
        "Lagna": "Pisces",
        "LagnaRasi": 12,
        "Nakshatra": "Revati"
    }
    
    pred_engine = PredictionEngine(jam_data, natal_data)
    full_data = pred_engine.generate_full_report_data("en")
    full_data['name'] = "Test User"
    full_data['gender'] = "Male"
    full_data['query_text'] = jam_data['query_text']
    full_data['query_time_str'] = q_time.strftime("%Y-%m-%d %H:%M:%S")
    full_data['natal'] = natal_data
    full_data['birth_place'] = "New Tippasandra, Bengaluru, Karnataka, I"
    full_data['lat'] = lat
    full_data['lon'] = lon
    
    output_path = "Test_Premium_Chart.pdf"
    gen = PremiumPDFGenerator(full_data, output_path)
    gen.generate()
    print(f"Generated test PDF: {output_path}")

if __name__ == "__main__":
    # Ensure backend is in path
    sys.path.append(os.path.dirname(__file__))
    test_chart()
