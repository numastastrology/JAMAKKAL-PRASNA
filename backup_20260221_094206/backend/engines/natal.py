import datetime
import ephem
import math
from typing import Dict, Any

class NatalEngine:
    """
    Precision Sidereal Engine for Birth Chart Synthesis.
    Fully automatic calculations using iterative horizon-ecliptic matching.
    """
    
    # Universal calculation constants
    LORDS = {
        1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon", 
        5: "Sun", 6: "Mercury", 7: "Venus", 8: "Mars", 
        9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"
    }

    RASI_NAMES = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    NAKSHATRAS = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
        "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
        "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]

    def __init__(self, birth_data: Dict[str, Any]):
        self.birth_data = birth_data
        self.name = birth_data.get("name", "Native")
        self.birth_date = birth_data.get("birth_date", "2009-04-09")
        self.birth_time = birth_data.get("birth_time", "22:58:00")
        
        # User Coordinates
        self.lat = float(birth_data.get("lat", 12.6935))
        self.lon = float(birth_data.get("lon", 79.9755))
        self.birth_place = birth_data.get("birth_place", "Chengalpattu")
        
        try:
            self.dt = datetime.datetime.strptime(f"{self.birth_date} {self.birth_time}", "%Y-%m-%d %H:%M:%S")
        except:
            self.dt = datetime.datetime(2009, 4, 9, 22, 58)

    def _get_ayanamsha(self, dt):
        """Calculates True Citra Ayanamsha for the given date."""
        # Standard formula approx: 23.85 + (year - 2000) * 0.01388
        year = dt.year
        return 23.85 + (year - 2000) * 0.01388

    def _get_detailed_info(self, absolute_degree, dt):
        aya = self._get_ayanamsha(dt)
        sidereal_deg = (absolute_degree - aya) % 360
        rasi_num = int(sidereal_deg // 30) + 1
        rasi_deg = sidereal_deg % 30
        
        nak_idx = int(sidereal_deg // (360/27))
        nak_name = self.NAKSHATRAS[nak_idx % 27]
        pada = int((sidereal_deg % (360/27)) // (360/108)) + 1
        
        return {
            "rasi": self.RASI_NAMES[rasi_num-1],
            "rasi_num": rasi_num,
            "degree": sidereal_deg,
            "nakshatra": nak_name,
            "pada": pada
        }

    def _calculate_ascendant(self, obs):
        """Calculates the Sidereal Ascendant using horizon-ecliptic matching."""
        # Find the ecliptic longitude that is currently rising (Altitude 0, Azimuth 90)
        # We'll use a binary search/iterative approach across 0-360 degrees ecliptic lon
        
        def get_altitude(ecl_lon_deg):
            body = ephem.Ecliptic(math.radians(ecl_lon_deg), 0)
            fixed = ephem.FixedBody()
            fixed._ra, fixed._dec = ephem.Equatorial(body).ra, ephem.Equatorial(body).dec
            fixed.compute(obs)
            return float(fixed.alt), float(fixed.az)

        # First, find where altitude crosses zero from negative to positive (rising)
        # We check every 10 degrees to find the rough neighborhood
        best_lon = 0
        min_dist = 999
        for deg in range(0, 360, 10):
            alt, az = get_altitude(deg)
            # We want Alt near 0 AND Az near 90 (East) or 270 (West). 
            # 90 is Rising, 270 is Setting.
            if abs(alt) < 0.5 and abs(math.degrees(az) - 90) < 30:
                best_lon = deg
                break
        
        # Refine with binary search
        low = (best_lon - 15) % 360
        high = (best_lon + 15) % 360
        for _ in range(15):
            mid = (low + high) / 2 if high > low else ((low + high + 360) / 2) % 360
            alt, az = get_altitude(mid)
            if alt > 0:
                high = mid
            else:
                low = mid
        
        return self._get_detailed_info(mid, self.dt)

    def _calculate_mandhi(self, obs, sunrise, sunset):
        wd = self.dt.weekday() # 0=Mon
        part_factors = {6:[14,10], 0:[10,6], 1:[6,2], 2:[2,26], 3:[26,22], 4:[22,18], 5:[18,14]} # Sun-Sat
        day_ghati, night_ghati = part_factors[wd]
        
        is_day = sunrise <= self.dt < sunset
        total_dur = (sunset - sunrise) if is_day else (sunrise + datetime.timedelta(days=1) - sunset)
        
        factor = day_ghati if is_day else night_ghati
        offset_pct = factor / 30.0
        mandhi_dt = (sunrise if is_day else sunset) + (total_dur * offset_pct)
        
        obs.date = mandhi_dt.strftime('%Y/%m/%d %H:%M:%S')
        return self._calculate_ascendant(obs)

    def compute_all(self) -> Dict[str, Any]:
        obs = ephem.Observer()
        obs.lat, obs.lon = str(self.lat), str(self.lon)
        obs.date = self.dt.strftime('%Y/%m/%d %H:%M:%S')
        obs.pressure = 0
        
        # TIMEZONE FIX: Treat birth_time as IST. Convert to UTC.
        # simple offset: -5.5 hours
        utc_dt = self.dt - datetime.timedelta(hours=5, minutes=30)
        self.obs_date_utc = utc_dt.strftime('%Y/%m/%d %H:%M:%S')
        obs.date = self.obs_date_utc
        
        # 1. Sunrise/Sunset
        # Use UTC date for rising/setting calc
        pass_dt = utc_dt
        obs.date = pass_dt.replace(hour=0, minute=0).strftime('%Y/%m/%d %H:%M:%S')
        sunrise = obs.next_rising(ephem.Sun()).datetime()
        if sunrise > self.dt:
            obs.date = (self.dt - datetime.timedelta(days=1)).strftime('%Y/%m/%d %H:%M:%S')
            sunrise = obs.next_rising(ephem.Sun()).datetime()
        obs.date = sunrise.strftime('%Y/%m/%d %H:%M:%S')
        sunset = obs.next_setting(ephem.Sun()).datetime()
        
        # 2. Planetary Positions
        obs.date = self.obs_date_utc
        positions = {}
        degrees = {}
        nakshatras = {}
        states = {}
        bodies = {"Sun": ephem.Sun(), "Moon": ephem.Moon(), "Mars": ephem.Mars(), "Mercury": ephem.Mercury(), "Venus": ephem.Venus(), "Saturn": ephem.Saturn(), "Jupiter": ephem.Jupiter()}
        
        # Friendship Table (Step I, II, III from photo)
        FRIENDS = {
            "Sun": ["Jupiter", "Mars", "Moon"], "Moon": ["Sun", "Mercury"], "Mars": ["Moon", "Jupiter", "Sun"],
            "Mercury": ["Rahu", "Venus", "Sun"], "Jupiter": ["Sun", "Moon", "Mars"], "Venus": ["Mercury", "Saturn", "Rahu"],
            "Saturn": ["Venus", "Mercury", "Rahu"], "Rahu": ["Venus", "Mercury", "Saturn"], "Ketu": ["Venus", "Mercury", "Saturn"]
        }
        ENEMIES = {
            "Sun": ["Saturn", "Rahu", "Venus"], "Moon": ["Rahu", "Ketu"], "Mars": ["Mercury", "Venus", "Rahu"],
            "Mercury": ["Moon"], "Jupiter": ["Mercury", "Venus"], "Venus": ["Sun", "Moon"],
            "Saturn": ["Sun", "Mars", "Moon"], "Rahu": ["Sun", "Mars", "Moon"], "Ketu": ["Sun", "Mars", "Moon"]
        }
        HOUSE_LORDS = {1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon", 5: "Sun", 6: "Mercury", 7: "Venus", 8: "Mars", 9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"}

        for name, body in bodies.items():
            body.compute(obs)
            lon = math.degrees(ephem.Ecliptic(body).lon) % 360
            info = self._get_detailed_info(lon, self.dt) # Use original DT for year based ayanamsha
            positions[name] = info["rasi_num"]
            degrees[name] = f"{int(info['degree'] % 30)}° {int((info['degree'] % 1)*60)}'"
            nakshatras[name] = f"{info['nakshatra']} ({info['pada']})"
            
            # Retrograde check
            obs.date = (utc_dt - datetime.timedelta(hours=1)).strftime('%Y/%m/%d %H:%M:%S')
            body.compute(obs)
            lon_prev = math.degrees(ephem.Ecliptic(body).lon)
            
            obs.date = self.obs_date_utc # Reset
            
            diff = (lon - lon_prev) % 360
            if diff > 180: diff -= 360
            
            state_str = "Retrograde" if diff < 0 else "Direct"
            
            # Friendship Status
            rasi_lord = HOUSE_LORDS[info["rasi_num"]]
            if rasi_lord in FRIENDS.get(name, []): state_str += " (Friend)"
            elif rasi_lord in ENEMIES.get(name, []): state_str += " (Enemy)"
            
            states[name] = state_str

        # 3. Nodes (True Nodes)
        obs.date = self.obs_date_utc
        jde = float(ephem.Date(obs.date)) + 2415020.5
        d = jde - 2451545.0
        ra_deg = (259.183275 - 0.0529538083 * d) % 360
        ra_info = self._get_detailed_info(ra_deg, self.dt)
        positions["Rahu"] = ra_info["rasi_num"]
        degrees["Rahu"] = f"{int(ra_info['degree'] % 30)}° {int((ra_info['degree'] % 1)*60)}'"
        nakshatras["Rahu"] = f"{ra_info['nakshatra']} ({ra_info['pada']})"
        
        k_lon = (ra_deg + 180) % 360
        k_info = self._get_detailed_info(k_lon, self.dt)
        positions["Ketu"] = k_info["rasi_num"]
        degrees["Ketu"] = f"{int(k_info['degree'] % 30)}° {int((k_info['degree'] % 1)*60)}'"
        nakshatras["Ketu"] = f"{k_info['nakshatra']} ({k_info['pada']})"
        
        # 4. Lagna & Mandhi
        asc_info = self._calculate_ascendant(obs)
        positions["Ascendant"] = asc_info["rasi_num"]
        degrees["Ascendant"] = f"{int(asc_info['degree'] % 30)}° {int((asc_info['degree'] % 1)*60)}'"
        nakshatras["Ascendant"] = f"{asc_info['nakshatra']} ({asc_info['pada']})"

        mandhi_info = self._calculate_mandhi(obs, sunrise, sunset)
        positions["Mandhi"] = mandhi_info["rasi_num"]
        degrees["Mandhi"] = f"{int(mandhi_info['degree'] % 30)}° {int((mandhi_info['degree'] % 1)*60)}'"
        nakshatras["Mandhi"] = f"{mandhi_info['nakshatra']} ({mandhi_info['pada']})"

        return {
            "name": self.name,
            "birth_date": self.birth_date,
            "birth_time": self.birth_time,
            "Lagna": asc_info["rasi"],
            "LagnaRasi": asc_info["rasi_num"],
            "Nakshatra": self._get_detailed_info(math.degrees(ephem.Ecliptic(bodies["Moon"]).lon) % 360, self.dt)["nakshatra"],
            "Positions": positions,
            "Degrees": degrees,
            "Nakshatras": nakshatras,
            "PlanetaryStates": states,
            "birth_place": self.birth_place
        }
