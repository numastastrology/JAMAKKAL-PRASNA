import sys
import os
import datetime
from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine

def test_health_analysis():
    # Setup test data
    lat, lon = 12.9716, 77.5946
    query_text = "What is the health conditions of the native and which body part is affected. Explain in detailed and when she can get recovered"
    
    jam_engine = JamakkalEngine(lat, lon)
    jam_data = jam_engine.compute_all()
    # Add extra metadata that SynthesisEngine expects from Main
    jam_data['query_time'] = datetime.datetime.now().isoformat()
    jam_data['lat'] = lat
    jam_data['lon'] = lon
    
    synthesis_engine = SynthesisEngine(jam_data, query_text)
    print(f"Detected Intent: {synthesis_engine.intent}")
    
    result = synthesis_engine.generate_synthesis()
    
    print("\n--- Synthesis Points ---")
    for point in result['points']:
        print(f"- {point}")
        
    print("\n--- Conclusion ---")
    print(result['conclusion'])

if __name__ == "__main__":
    sys.path.append(os.path.dirname(__file__))
    test_health_analysis()
