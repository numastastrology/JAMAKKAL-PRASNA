
import datetime
import sys
import os

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from engines.jamakkal import JamakkalEngine

def analyze_date(date_str, label, lat=13.08, lon=80.27):
    try:
        dt = datetime.datetime.fromisoformat(date_str)
    except ValueError:
        # Handle simple date without time
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        
    engine = JamakkalEngine(lat, lon, dt)
    data = engine.compute_all()
    
    print(f"\n--- {label} ({date_str}) ---")
    print(f"Udayam: {data['inner_planets']['Udayam']['rasi']} | Arudam: {data['inner_planets']['Arudam']['rasi']} | Kavippu: {data['inner_planets']['Kavippu']['rasi']}")
    
    # Relevant planets for competition: Mars, Saturn, Jupiter, Mercury
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    for p in planets:
        pos = data['transits'][p]
        print(f"  {p:10}: {pos['rasi']:12} @ {pos['degree']:8} | Star: {pos['nakshatra']}")

# --- TAMIL NADU ---
print("\n" + "="*50 + "\nTAMIL NADU ANALYSIS\n" + "="*50)
analyze_date("2024-02-02T12:00:00", "TVK Formation Date")
analyze_date("2026-04-06T12:00:00", "TN Poll Date")
analyze_date("2026-05-04T12:00:00", "TN Counting Date")

# --- WEST BENGAL ---
print("\n" + "="*50 + "\nWEST BENGAL ANALYSIS\n" + "="*50)
analyze_date("1998-01-01T12:00:00", "TMC Formation Date", lat=22.57, lon=88.36) # Kolkata
analyze_date("1980-04-06T12:00:00", "BJP Formation Date", lat=28.61, lon=77.20) # New Delhi
analyze_date("2026-04-23T12:00:00", "WB Poll Phase (April 23)", lat=22.57, lon=88.36)
analyze_date("2026-05-04T12:00:00", "WB Counting Date", lat=22.57, lon=88.36)

# --- KERALA ---
print("\n" + "="*50 + "\nKERALA ANALYSIS\n" + "="*50)
analyze_date("1964-11-07T12:00:00", "CPI(M) Formation Date", lat=22.57, lon=88.36) # Formed in Calcutta
analyze_date("2026-04-06T12:00:00", "Kerala Poll Date", lat=8.52, lon=76.93) # Trivandrum
analyze_date("2026-05-04T12:00:00", "Kerala Counting Date", lat=8.52, lon=76.93)
