import os
import sys
import datetime
from engines.jamakkal import JamakkalEngine
from engines.natal import NatalEngine
from engines.prediction import PredictionEngine
from utils.pdf_generator import PremiumPDFGenerator

def test_elaborative_synthesis():
    sys.path.append(os.getcwd())
    print("--- Verifying Elaborative Synthesis & PDF Fixes ---")
    
    lat, lon = 13.0827, 80.2707 # Chennai
    query_time = datetime.datetime.now()
    
    # CASE 1: Career/Job Change
    print("\n[TEST CASE 1] Query: 'Whether job change for the native is favourable'")
    jam_engine = JamakkalEngine(lat, lon, query_time)
    jam_data = jam_engine.compute_all()
    jam_data['query_text'] = "Whether job change for the native is favourable"
    
    natal_engine = NatalEngine({
        "name": "M Manivannan",
        "birth_date": "1985-06-15",
        "birth_time": "10:30:00",
        "birth_place": "Devakottai, Tamil Nadu",
        "lat": 9.9442,
        "lon": 78.8258
    })
    natal_data = natal_engine.compute_all()
    
    pred_engine = PredictionEngine(jam_data, natal_data)
    report_data = pred_engine.generate_full_report_data()
    report_data['query_text'] = jam_data['query_text']
    
    print(f"Points generated: {len(report_data['synthesis_points'])}")
    for pt in report_data['synthesis_points']:
        print(f"  {pt}")
    print(f"Conclusion: {report_data['synthesis_conclusion']}")

    # Generate PDF for this case
    pdf_gen = PremiumPDFGenerator(report_data, "Verification_Report_Job.pdf")
    filename = pdf_gen.generate()
    print(f"PDF Generated: {filename}")

    # CASE 2: Marriage
    print("\n[TEST CASE 2] Query: 'Marriage proposal for daughter'")
    jam_data['query_text'] = "Marriage proposal for daughter"
    pred_engine = PredictionEngine(jam_data, natal_data)
    report_data = pred_engine.generate_full_report_data()
    report_data['query_text'] = jam_data['query_text']
    
    print(f"Points generated: {len(report_data['synthesis_points'])}")
    for pt in report_data['synthesis_points']:
        print(f"  {pt}")

    pdf_gen = PremiumPDFGenerator(report_data, "Verification_Report_Marriage.pdf")
    filename = pdf_gen.generate()
    print(f"PDF Generated: {filename}")

if __name__ == "__main__":
    test_elaborative_synthesis()
