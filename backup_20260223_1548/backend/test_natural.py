
import ephem
import math
import datetime

def test_natural_transit(planet_name, start_date_ist):
    print(f"--- Testing Natural Transit for {planet_name} ---")
    
    # IST to UTC
    start_date_utc = start_date_ist - datetime.timedelta(hours=5, minutes=30)
    
    obs = ephem.Observer()
    obs.lat, obs.lon = '0', '0'
    obs.date = start_date_utc.strftime('%Y/%m/%d %H:%M:%S')
    
    planet_map = {
        "Sun": ephem.Sun, "Moon": ephem.Moon, "Mars": ephem.Mars,
        "Mercury": ephem.Mercury, "Jupiter": ephem.Jupiter,
        "Venus": ephem.Venus, "Saturn": ephem.Saturn
    }
    
    body = planet_map[planet_name]()
    
    # Get initial rasi
    body.compute(obs)
    ecl_deg = math.degrees(float(ephem.Ecliptic(body).lon)) % 360
    # More precise Ayanamsha (Lahiri approx: 23.85 at J2000, 50.29" precession)
    # Using 1.397e-2 as deg/year
    d_now = start_date_ist
    years_since_j2000 = (d_now - datetime.datetime(2000, 1, 1)).total_seconds() / (365.25 * 24 * 3600)
    aya_start = 23.85 + years_since_j2000 * 0.01397
    sidereal_lon_start = (ecl_deg - aya_start) % 360
    curr_rasi = int(sidereal_lon_start // 30) + 1
    
    print(f"Start Date: {start_date_ist}")
    print(f"Initial Sidereal Rasi: {curr_rasi}")
    print(f"Initial Sidereal Lon: {sidereal_lon_start:.4f}")
    
    found_date = None
    for day in range(1, 400):
        obs.date = ephem.Date(obs.date + 1)
        body.compute(obs)
        ecl = math.degrees(float(ephem.Ecliptic(body).lon)) % 360
        d_dt = ephem.Date(obs.date).datetime()
        # IST
        d_ist = d_dt + datetime.timedelta(hours=5, minutes=30)
        years = (d_ist - datetime.datetime(2000, 1, 1)).total_seconds() / (365.25 * 24 * 3600)
        aya = 23.85 + years * 0.01397
        sidereal = (ecl - aya) % 360
        new_rasi = int(sidereal // 30) + 1
        
        if new_rasi != curr_rasi:
            # Refine to hourly
            obs.date = ephem.Date(obs.date - 1)
            for hour in range(25):
                obs.date = ephem.Date(obs.date + (1/24))
                body.compute(obs)
                ecl_h = math.degrees(float(ephem.Ecliptic(body).lon)) % 360
                d_h_ist = ephem.Date(obs.date).datetime() + datetime.timedelta(hours=5, minutes=30)
                y_h = (d_h_ist - datetime.datetime(2000, 1, 1)).total_seconds() / (365.25 * 24 * 3600)
                aya_h = 23.85 + y_h * 0.01397
                sid_h = (ecl_h - aya_h) % 360
                if int(sid_h // 30) + 1 != curr_rasi:
                    found_date = d_h_ist
                    break
            if found_date: break

    if found_date:
        print(f"Transit Found: {found_date.strftime('%Y-%m-%d %H:%M:%S')} (IST)")
    else:
        print("Transit NOT found in 400 days.")

# Run test
test_natural_transit("Venus", datetime.datetime(2026, 2, 23, 15, 0))
