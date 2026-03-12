import datetime
from engines.jamakkal import JamakkalEngine

def test_jama_rotation():
    lat, lon = 13.0827, 80.2707 # Chennai
    
    # Test cases for different times today
    # Assuming today is 2026-02-11
    test_times = [
        "2026-02-11 06:30:00", # Morning (Jama 1)
        "2026-02-11 09:00:00", # Jama 2
        "2026-02-11 12:00:00", # Midday
        "2026-02-11 15:00:00", # Afternoon
        "2026-02-11 18:30:00", # Evening (Likely Night Jama 1/9)
        "2026-02-11 21:00:00", # Night
        "2026-02-12 00:00:00", # Midnight
        "2026-02-12 03:00:00", # Early morning
    ]
    
    for t_str in test_times:
        t = datetime.datetime.strptime(t_str, "%Y-%m-%d %H:%M:%S")
        engine = JamakkalEngine(lat, lon, t)
        data = engine.compute_all()
        
        print(f"Time: {t_str}")
        print(f"  Sunrise: {data['sunrise']}")
        print(f"  Sunset:  {data['sunset']}")
        print(f"  Is Day:  {data['is_day']}")
        print(f"  Block:   {data['block']}")
        print(f"  Ruling:  {data['ruling_planet']}")
        print("-" * 30)

if __name__ == "__main__":
    test_jama_rotation()
