import sys, os
from datetime import datetime
# Ensure backend is in path
current_dir = os.getcwd()
backend_path = os.path.join(current_dir, 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

from engines.jamakkal import JamakkalEngine
from engines.prediction import PredictionEngine
from engines.synthesis import SynthesisEngine
from utils.pdf_generator import PremiumPDFGenerator

def generate_corrected_report():
    # Ahmedabad Coordinates
    lat=23.0225; lon=72.5714
    # Match Date: March 8, 2026, 7:00 PM IST
    dt = datetime(2026, 3, 8, 19, 0, 0)
    
    # 1. Compute Jamakkal Data
    je = JamakkalEngine(lat, lon, dt)
    jam_data = je.compute_all()
    
    # 2. Add required metadata for Synthesis/PDF
    jam_data['lat'] = lat
    jam_data['lon'] = lon
    jam_data['location'] = "Ahmedabad, India"
    jam_data['query_text'] = "India vs New Zealand"
    jam_data['is_strict_competition_mode'] = True
    jam_data['query_time_str'] = dt.strftime("%Y-%m-%d %H:%M:%S")
    
    # 3. Generate Prediction/Synthesis
    # PredictionEngine needs jam_data and optional natal_data
    pred_engine = PredictionEngine(jam_data)
    # This triggers SynthesisEngine internally for competition mode
    full_data = pred_engine.generate_full_report_data("en")
    
    # Merge additional data needed for PDF
    full_data['lat'] = lat
    full_data['lon'] = lon
    full_data['location'] = jam_data['location']
    full_data['query_text'] = jam_data['query_text']
    full_data['is_strict_competition_mode'] = True
    full_data['query_time_str'] = jam_data['query_time_str']
    full_data['block'] = jam_data['block']
    full_data['sunrise_str'] = jam_data['sunrise'] 
    
    # 4. Generate PDF
    output_path = os.path.join(current_dir, "Ind_vs_NZ_Corrected_Prediction.pdf")
    gen = PremiumPDFGenerator(full_data, output_path)
    gen.generate()
    
    print(f"Corrected PDF generated at: {output_path}")

if __name__ == "__main__":
    generate_corrected_report()
