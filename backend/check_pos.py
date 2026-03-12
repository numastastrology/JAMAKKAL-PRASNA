
import datetime
import sys
import os

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from engines.jamakkal import JamakkalEngine

lat, lon = 13.0827, 80.2707 # Chennai
query_time = datetime.datetime.now() # Feb 23, 2026

engine = JamakkalEngine(lat, lon, query_time)
data = engine.compute_all()
v = data['transits']['Venus']

print(f"Current Date (IST): {query_time}")
print(f"Venus Position: {v['rasi']} @ {v['degree']}")
print(f"Venus Abs Deg (Sidereal): {v['abs_deg']}")
print(f"Venus Nakshatra: {v['nakshatra']}")
print(f"Ayanamsha Used: {data['panchanga']['Ayanamsa']}")
print(f"Is Tropical? No, this is Sidereal.")

# Calculate Tropical
year = query_time.year
aya = 23.85 + (year - 2000) * 0.01388
tropical = (v['abs_deg'] + aya) % 360
print(f"Calculated Tropical Deg: {tropical}")
