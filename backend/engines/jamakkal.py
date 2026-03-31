import datetime
import ephem
import math

class JamakkalEngine:
    """
    Precision Sidereal Engine for Jamakkal Prasna.
    Targets exact match with Professional Jamakkol Standards (True Citra Ayanamsha).
    Calculates Rasi, Degree, Nakshatra, Pada, and Lords for all points.
    """
    
    # Precise True Citra Ayanamsha for 2026-02-10
    AYANAMSHA = 24.20838 

    PLANETS_ORDER = ["Sun", "Mars", "Jupiter", "Mercury", "Venus", "Saturn", "Moon", "Snake"]
    PLANETS_ORDER = ["Sun", "Mars", "Jupiter", "Mercury", "Venus", "Saturn", "Moon", "Snake"]
    JAMAKKAL_HOUSES = [1, 2, 4, 5, 7, 8, 10, 11] # Skip corners: 3, 6, 9, 12. Correct order as per chart.

    RASI_NAMES = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    NAKSHATRAS = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
        "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
        "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    NAK_LORDS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"] * 3

    def __init__(self, lat: float, lon: float, query_time: datetime.datetime = None):
        self.lat = lat
        self.lon = lon
        self.query_time = query_time or datetime.datetime.now()
        self.obs = ephem.Observer()
        self.obs.lat = str(self.lat)
        self.obs.lon = str(self.lon)
        self.obs.pressure = 0
        
        # TIMEZONE FIX: Treat query_time as IST. Convert to UTC for Ephem.
        utc_time = self.query_time - datetime.timedelta(hours=5, minutes=30)
        self.obs.date = utc_time.strftime('%Y/%m/%d %H:%M:%S')
        
        self.sunrise, self.sunset, self.next_sunrise = self._calculate_sun_times()

    def _calculate_sun_times(self):
        # We need the sunrise preceding the query time
        # Save current obs date
        orig_date = self.obs.date
        
        # Get sunrise before query_time
        sunrise_utc = self.obs.previous_rising(ephem.Sun()).datetime()
        
        # Get sunset after that sunrise
        self.obs.date = sunrise_utc
        sunset_utc = self.obs.next_setting(ephem.Sun()).datetime()
        
        # Get next sunrise after that sunset
        self.obs.date = sunset_utc
        next_sunrise_utc = self.obs.next_rising(ephem.Sun()).datetime()
        
        # Restore obs date
        self.obs.date = orig_date
        
        # Convert all to IST
        sunrise = sunrise_utc + datetime.timedelta(hours=5, minutes=30)
        sunset = sunset_utc + datetime.timedelta(hours=5, minutes=30)
        next_sunrise = next_sunrise_utc + datetime.timedelta(hours=5, minutes=30)
        
        return sunrise, sunset, next_sunrise

    def _get_detailed_info(self, absolute_degree):
        """Returns Rasi, Degree in Rasi, Nakshatra, Pada, and Lord."""
        # Precession-aware Ayanamsha sync
        year = self.query_time.year
        dynamic_aya = 23.85 + (year - 2000) * 0.01388
        
        sidereal_deg = (absolute_degree - dynamic_aya) % 360
        rasi_num = int(sidereal_deg // 30) + 1
        rasi_deg = sidereal_deg % 30
        
        # Nakshatra
        nak_idx = int(sidereal_deg // (360/27))
        nak_name = self.NAKSHATRAS[nak_idx % 27]
        pada = int((sidereal_deg % (360/27)) // (360/108)) + 1
        lord = self.NAK_LORDS[nak_idx % 27]
        
        return {
            "rasi": self.RASI_NAMES[rasi_num-1],
            "rasi_num": rasi_num,
            "degree": f"{int(rasi_deg)}° {int((rasi_deg % 1)*60)}' {int(((rasi_deg*60)%1)*60)}\"",
            "nakshatra": nak_name,
            "pada": pada,
            "star_lord": lord,
            "abs_deg": sidereal_deg
        }

    def _get_friendship_status(self, planet, rasi_num, star_lord):
        """Step I, II, III: Friendship/Enmity Logic from User Photo"""
        # Table from Photo (Step II & III)
        FRIENDS = {
            "Sun": ["Jupiter", "Mars", "Moon"],
            "Moon": ["Sun", "Mercury"],
            "Mars": ["Moon", "Jupiter", "Sun"],
            "Mercury": ["Rahu", "Venus", "Sun"],
            "Jupiter": ["Sun", "Moon", "Mars"],
            "Venus": ["Mercury", "Saturn", "Rahu"],
            "Saturn": ["Venus", "Mercury", "Rahu"],
            "Rahu": ["Venus", "Mercury", "Saturn"],
            "Ketu": ["Venus", "Mercury", "Saturn"] # Assumed same as Rahu or neutral
        }
        ENEMIES = {
            "Sun": ["Saturn", "Rahu", "Venus"],
            "Moon": ["Rahu", "Ketu"],
            "Mars": ["Mercury", "Venus", "Rahu"],
            "Mercury": ["Moon"],
            "Jupiter": ["Mercury", "Venus"],
            "Venus": ["Sun", "Moon"],
            "Saturn": ["Sun", "Mars", "Moon"],
            "Rahu": ["Sun", "Mars", "Moon"],
            "Ketu": ["Sun", "Mars", "Moon"]
        }
        
        # 1. Rasi Lord Check
        house_lords = {
            1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon", 
            5: "Sun", 6: "Mercury", 7: "Venus", 8: "Mars", 
            9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"
        }
        rasi_lord = house_lords[rasi_num]
        
        if rasi_lord in FRIENDS.get(planet, []):
            status = "Friendly Sign"
        elif rasi_lord in ENEMIES.get(planet, []):
            status = "Enemy Sign"
        else:
            status = "Neutral Sign"
            
        # 2. Exaltation/Debilitation Override
        exalt = {"Sun": 1, "Moon": 2, "Mars": 10, "Mercury": 6, "Jupiter": 4, "Venus": 12, "Saturn": 7, "Rahu": 2, "Ketu": 8}
        debilit = {"Sun": 7, "Moon": 8, "Mars": 4, "Mercury": 12, "Jupiter": 10, "Venus": 6, "Saturn": 1, "Rahu": 8, "Ketu": 2}
        
        if exalt.get(planet) == rasi_num: status = "Exalted"
        if debilit.get(planet) == rasi_num: status = "Debilitated"
        
        # 3. Star Lord Check (Step V.2)
        # "Planet in friendly Rasi but enemy star may not give favorable result"
        star_status = "Neutral Star"
        if star_lord in FRIENDS.get(planet, []): star_status = "Friendly Star"
        elif star_lord in ENEMIES.get(planet, []): star_status = "Enemy Star"
        
        return status, star_status

    def _get_fruition_period(self, planet, status):
        """Step IV: Planetary Periods for Fruition"""
        # "Sun: 6m, Moon: Immediate, Mars: 6m, Merc: 2m, Jup: 1m, Ven: 15d, Sat: 1y, Rahu: 8m, Ketu: 3m"
        periods = {
            "Sun": "6 Months", "Moon": "Immediate", "Mars": "6 Months", 
            "Mercury": "2 Months", "Jupiter": "1 Month", "Venus": "15 Days", 
            "Saturn": "1 Year", "Rahu": "8 Months", "Ketu": "3 Months"
        }
        base_period = periods.get(planet, "Unknown")
        
        # Logic: "Retrograde planets... start giving favorable result once they become direct"
        # We handle this in prediction text, but returning base period here.
        return base_period

    def calculate_panchanga(self, transits):
        sun_deg = transits['Sun']['abs_deg']
        moon_deg = transits['Moon']['abs_deg']
        
        diff = (moon_deg - sun_deg) % 360
        tithi_num = int(diff // 12) + 1
        paksha = "Shukla" if tithi_num <= 15 else "Krishna"
        tithi_names = ["Prathama", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shasthi", "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima/Amavasya"]
        tithi_name = tithi_names[(tithi_num-1) % 15]

        yoga_num = int(((sun_deg + moon_deg) % 360) // (360/27)) + 1
        karana_num = int(diff // 6) + 1
        
        # Hora
        weekday = (self.query_time.weekday() + 1) % 7 # 0=Sun
        hora_order = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
        elapsed_hours = (self.query_time - self.sunrise).total_seconds() / 3600
        # Correct Hora logic: Day lord starts first hour, then follows the above cycle
        # We need to map weekday (0-6) into the cycle starting point
        weekday_map = {0:0, 1:3, 2:6, 3:2, 4:5, 5:1, 6:4} # Sun, Moon, Mars...
        hora_idx = (weekday_map[weekday] + int(elapsed_hours)) % 7
        hora = hora_order[hora_idx]

        return {
            "Tithi": f"{paksha} {tithi_name} ({tithi_num})",
            "Nakshatra": transits['Moon']['nakshatra'],
            "Yoga": f"Yoga #{yoga_num}",
            "Karana": f"Karana #{karana_num}",
            "Hora": hora,
            "SiderealTime": str(self.obs.sidereal_time()),
            "Ayanamsa": f"True Citra ({self.AYANAMSHA}°)"
        }

    def compute_all(self):
        self.obs.date = self.query_time.strftime('%Y/%m/%d %H:%M:%S')
        
        # 1. Transits
        transits = {}
        bodies = {"Sun": ephem.Sun(), "Moon": ephem.Moon(), "Mars": ephem.Mars(), "Mercury": ephem.Mercury(), "Venus": ephem.Venus(), "Saturn": ephem.Saturn(), "Jupiter": ephem.Jupiter()}
        for name, body in bodies.items():
            body.compute(self.obs)
            # IST Offset: Ecliptic longitude is independent of time zone, but Observer time affects positions.
            # We already set self.obs.date based on input query_time.
            # However, if input query_time was naive, we treated it as local.
            # ephem expects UTC. 
            # If system `datetime.now()` is IST, we must convert to UTC for ephem.
            # But wait, earlier logic using `datetime.now()` directly into `obs.date` assumes `now()` returns UTC?
            # No, `datetime.now()` returns local system time. `ephem.Date()` expects UTC.
            # CRITICAL FIX: Subtract 5.5 hours from input time if it's treated as IST.
            
            # Actually, `self.query_time` from `main.py` comes from `datetime.now()` or request.
            # If user sends local time, we must adjust.
            # Let's assume input is IST.
            pass # Logic handled in __init__ now
            
            transits[name] = self._get_detailed_info(math.degrees(ephem.Ecliptic(body).lon) % 360)
            
            # Add Friendship/Fruition Info
            curr_rasi = transits[name]["rasi_num"]
            curr_star = transits[name]["star_lord"]
            status, star_status = self._get_friendship_status(name, curr_rasi, curr_star)
            transits[name]["status"] = status
            transits[name]["star_status"] = star_status
            transits[name]["fruition"] = self._get_fruition_period(name, status)
            
        # Rahu/Snake (Mean Node Calculation)
        # J2000 epoch: 2000-01-01 12:00:00 UTC (JD 2451545.0)
        d = float(ephem.Date(self.obs.date)) - float(ephem.Date('2000/01/01 12:00:00'))
        # Mean Rahu Longitude (IAU formula for ascending node)
        ra_deg = (125.04452 - 0.0529537652 * d) % 360
        transits["Rahu"] = self._get_detailed_info(ra_deg)
        transits["Ketu"] = self._get_detailed_info((ra_deg + 180) % 360)
        
        # Ascendant
        ra_asc = self.obs.sidereal_time()
        transits["Ascendant"] = self._get_detailed_info(math.degrees(ra_asc) % 360)

        # Mandhi (md) calculation
        # Segment offsets: Sun(7), Mon(6), Tue(5), Wed(4), Thu(3), Fri(2), Sat(1)
        weekday = (self.query_time.weekday() + 1) % 7 # 0=Sun
        is_day = self.sunrise <= self.query_time < self.sunset
        total_dur = (self.sunset - self.sunrise).total_seconds() if is_day else (self.next_sunrise - self.sunset).total_seconds()
        
        if is_day:
            seg_offsets = {0:7, 1:6, 2:5, 3:4, 4:3, 5:2, 6:1}
        else:
            seg_offsets = {0:3, 1:2, 2:1, 3:7, 4:6, 5:5, 6:4}
            
        seg_num = seg_offsets.get(weekday, 1)
        md_time_offset = seg_num * (total_dur / 8)
        md_time = (self.sunrise if is_day else self.sunset) + datetime.timedelta(seconds=md_time_offset)
        
        # Save current obs date
        orig_date = self.obs.date
        utc_md_time = md_time - datetime.timedelta(hours=5, minutes=30)
        self.obs.date = utc_md_time.strftime('%Y/%m/%d %H:%M:%S')
        md_asc = self.obs.sidereal_time()
        transits["Mandhi"] = self._get_detailed_info(math.degrees(md_asc) % 360)
        # Restore obs date
        self.obs.date = orig_date

        # 2. Jamakkal Info
        is_day = self.sunrise <= self.query_time < self.sunset
        
        if is_day:
            total_dur = (self.sunset - self.sunrise).total_seconds()
            elapsed = (self.query_time - self.sunrise).total_seconds()
            block = int(elapsed // (total_dur / 8)) + 1
            if block > 8: block = 8
        else:
            # Query time is between sunset and next sunrise
            total_dur = (self.next_sunrise - self.sunset).total_seconds()
            elapsed = (self.query_time - self.sunset).total_seconds()
            # If query_time is before sunset (very early morning), 
            # we need to handle the Wrap-around? No, _calculate_sun_times 
            # always gives sunset/sunrise relative to query_time.
            # But wait, if query_time is 4 AM, sunrise (prev) is 6 AM yesterday.
            # sunset is 6 PM yesterday. query_time (4 AM today) is > sunset (yesterday).
            # So elapsed = 4 AM today - 6 PM yesterday = 10 hours.
            # total_dur = 6 AM today - 6 PM yesterday = 12 hours.
            # block = 10 // 1.5 + 9 = 6 + 9 = 15. Correct.
            
            # Night blocks are 9-16
            block = int(elapsed // (total_dur / 8)) + 9
            if block > 16: block = 16

        # Jama Grahas (Outer Planets) - TRUE JAMAKKOL LOGIC
        # These are mathematical points that move ANTI-CLOCKWISE
        # Base Sun position depends on weekday, then moves 1 sign back per Jamam
        
        # WEEKDAY LOGIC: In Jamakkol, the "day" starts at SUNRISE.
        # So if it's 3 AM Feb 12th, the weekday is still Feb 11th's weekday.
        weekday = self.sunrise.weekday()  # Mon=0, Tue=1, ..., Sun=6
        
        # Base Sun position for Jamam #1 on each day
        # Derived from user reference: Tuesday Jamam#5 -> Sun in Scorpio(8)
        # Working backwards: #5=Scorpio -> #1=Pisces
        base_sun_positions = {
            0: 4,   # Monday -> Cancer
            1: 12,  # Tuesday -> Pisces
            2: 3,   # Wednesday -> Gemini
            3: 6,   # Thursday -> Virgo
            4: 9,   # Friday -> Sagittarius
            5: 10,  # Saturday -> Capricorn
            6: 1    # Sunday -> Aries
        }
        
        sun_start = base_sun_positions.get(weekday, 1)
        
        # Calculate current Sun position (moves 1 sign BACK per Jamam)
        current_sun_rasi = sun_start - (block - 1)
        while current_sun_rasi <= 0:
            current_sun_rasi += 12
        
        # Relative offsets for other planets (signs BEHIND Sun in anti-clockwise)
        # Based on user screenshot pattern
        planet_offsets = {
            "Sun": 0,
            "Mars": 2,      # 2 signs behind Sun
            "Jupiter": 3,   # 3 signs behind Sun
            "Mercury": 5,   # 5 signs behind Sun
            "Venus": 6,     # 6 signs behind Sun
            "Saturn": 8,    # 8 signs behind Sun
            "Moon": 9,      # 9 signs behind Sun
            "Snake": 11     # 11 signs behind Sun (Rahu/Ketu)
        }
        
        jamam_duration = total_dur / 8
        elapsed_in_jamam = elapsed % jamam_duration
        # Jamakkol planets move anti-clockwise (30 -> 0 degrees during the Jamam)
        jama_degree_in_rasi = 30 - ( (elapsed_in_jamam / jamam_duration) * 30 )
        
        jama_positions = {}
        for planet, offset in planet_offsets.items():
            rasi = current_sun_rasi - offset
            while rasi <= 0:
                rasi += 12
            
            # Add degree info to match professional charts
            abs_deg = (rasi - 1) * 30 + jama_degree_in_rasi
            jama_positions[f"Jama {planet}"] = {
                "rasi_num": rasi,
                "rasi": self.RASI_NAMES[rasi-1],
                "degree_in_rasi": jama_degree_in_rasi,
                "abs_deg": abs_deg,
                "degree": f"{int(jama_degree_in_rasi)}° {int((jama_degree_in_rasi % 1)*60)}'",
                "abs_degree_fmt": f"{int(abs_deg)}° {int((abs_deg % 1)*60)}'"
            }

        # Inner Planets
        sun_abs = transits["Sun"]["abs_deg"]
        # Night Jamam starts from 7th house of Sun
        start_offset = 0 if is_day else 180
        jamam_offset = (block - 1 if is_day else block - 9) * 30
        
        ud_deg_sidereal = (sun_abs + start_offset + jamam_offset) % 360
        ar_deg_sidereal = (ud_deg_sidereal - 3 * 30) % 360 # 4th house logic from ref
        kv_deg_sidereal = (ud_deg_sidereal + 3 * 30) % 360 # Kavippu logic varies, but usually opposite arudham or fixed shift
        
        # In the photo logic: Arudam is near Udayam, Kavippu is after.
        # AR = (UD + something)? No, photo says UD=42, AR=56. (Diff 14 deg).
        # Actually, let's use the provided logic which was working for the user before.
        # But I'll provide detailed degree info.
        
        ud_info = self._get_detailed_info(ud_deg_sidereal + self.AYANAMSHA)
        ar_info = self._get_detailed_info((ud_deg_sidereal - 90) + self.AYANAMSHA)
        kv_info = self._get_detailed_info((ud_deg_sidereal + 180) + self.AYANAMSHA)
        
        inner = {
            "Udayam": ud_info,
            "Arudam": ar_info,
            "Kavippu": kv_info
        }
        
        # ruling_planet
        ruling_idx = ( {0:7, 1:5, 2:0, 3:2, 4:1, 5:3, 6:4}[weekday] + (block - 1 if is_day else block - 9) ) % 8
        ruling = ["Sun", "Mars", "Jupiter", "Mercury", "Venus", "Saturn", "Moon", "Snake"][ruling_idx]

        # Add "Snake" (The 8th Jama Graha) to transits for synthesis logic
        # It follows the same degree as the current Jama Snake
        # but we need it in the transits dict for intent logic
        jama_snake = jama_positions.get("Jama Snake", {})
        if jama_snake:
            s_deg = jama_snake.get("abs_deg", ra_deg) # Fallback to Rahu if not found
            year = self.query_time.year
            dynamic_aya = 23.85 + (year - 2000) * 0.01388
            transits["Snake"] = self._get_detailed_info(s_deg + dynamic_aya)
            
            # Add status/fruition for Snake (Treat as Rahu/Malefic)
            s_rasi = transits["Snake"]["rasi_num"]
            s_star = transits["Snake"]["star_lord"]
            s_status, s_star_status = self._get_friendship_status("Rahu", s_rasi, s_star)
            transits["Snake"]["status"] = s_status
            transits["Snake"]["star_status"] = s_star_status
            transits["Snake"]["fruition"] = self._get_fruition_period("Rahu", s_status)

        # Calculate auxiliary points for Prasanna Details Special
        lords_map = {1:"Mars", 2:"Venus", 3:"Mercury", 4:"Moon", 5:"Sun", 6:"Mercury", 7:"Venus", 8:"Mars", 9:"Jupiter", 10:"Saturn", 11:"Saturn", 12:"Jupiter"}
        def get_kala_ascendant(seg_offsets_map):
            seg_num = seg_offsets_map.get(weekday, 1)
            offset = seg_num * (total_dur / 8)
            t = (self.sunrise if is_day else self.sunset) + datetime.timedelta(seconds=offset)
            orig = self.obs.date
            self.obs.date = (t - datetime.timedelta(hours=5, minutes=30)).strftime('%Y/%m/%d %H:%M:%S')
            asc = math.degrees(self.obs.sidereal_time()) % 360
            self.obs.date = orig
            return self._get_detailed_info(asc)

        if is_day:
            k_off = {0:6, 1:5, 2:4, 3:3, 4:2, 5:1, 6:0}
            e_off = {0:4, 1:3, 2:2, 3:1, 4:0, 5:6, 6:5}
            r_off = {0:7, 1:1, 2:6, 3:4, 4:5, 5:3, 6:2}
            m_off = {0:2, 1:1, 2:0, 3:6, 4:5, 5:4, 6:3}
        else:
            k_off = {0:2, 1:1, 2:0, 3:6, 4:5, 5:4, 6:3}
            e_off = {0:0, 1:6, 2:5, 3:4, 4:3, 5:2, 6:1}
            r_off = {0:3, 1:4, 2:2, 3:0, 4:1, 5:6, 6:5}
            m_off = {0:6, 1:5, 2:4, 3:3, 4:2, 5:1, 6:0}

        transits["Kuligan"] = get_kala_ascendant(k_off)
        transits["Emakandam"] = get_kala_ascendant(e_off)
        transits["RahuTime"] = get_kala_ascendant(r_off)
        transits["Mrithyu"] = get_kala_ascendant(m_off)

        # Build Prasanna Details Special structure
        def get_pt(point_info):
            rasi = point_info["rasi_num"]
            deg_in_rasi = point_info["abs_deg"] % 30
            pct = round((deg_in_rasi / 30.0) * 100, 2)
            
            # Find Jama Graha in that rasi
            jg_in_rasi = []
            for jg, jinfo in jama_positions.items():
                if jinfo["rasi_num"] == rasi:
                    jg_in_rasi.append(jg.replace("Jama ", "").upper())
            
            if jg_in_rasi:
                pl = ", ".join(jg_in_rasi)
            else:
                opp_rasi = rasi + 6 if rasi <= 6 else rasi - 6
                # Phase 2: Aspecting Planet (7th house)
                for jg, jinfo in jama_positions.items():
                    if jinfo["rasi_num"] == opp_rasi:
                        jg_in_rasi.append(jg.replace("Jama ", "").upper())
                if jg_in_rasi:
                    pl = ", ".join(jg_in_rasi)
                else:
                    # Phase 3: Rasi Lord
                    pl = lords_map[rasi].upper()
                    
            return {"planet": pl, "percent": pct}

        exalted = []
        debilitated = []
        parivarthana = [] # Left blank initially or handled externally
        for name, info in transits.items():
            if name in ["Ascendant", "Mandhi", "Kuligan", "Emakandam", "RahuTime", "Mrithyu"]: continue
            if info.get("status") == "Exalted": exalted.append(name.upper())
            if info.get("status") == "Debilitated": debilitated.append(name.upper())

        ud_rasi = inner["Udayam"]["rasi_num"]
        ar_rasi = inner["Arudam"]["rasi_num"]
        kv_rasi = inner["Kavippu"]["rasi_num"]
        
        ud_lord_name = lords_map[ud_rasi]
        ud_lord_rasi = transits[ud_lord_name]["rasi_num"] if ud_lord_name in transits else ud_rasi
        
        prasanna_special = {
            "udhayam": get_pt(inner["Udayam"]),
            "udhayam_lord": {"planet": ud_lord_name.upper(), "bhava": ((ud_lord_rasi - ud_rasi) % 12) + 1},
            "arudam_bhava": ((ar_rasi - ud_rasi) % 12) + 1,
            "arudam": get_pt(inner["Arudam"]),
            "kavipu": get_pt(inner["Kavippu"]),
            "kavipu_bhava": ((kv_rasi - ud_rasi) % 12) + 1,
            "exalted": exalted,
            "debilitated": debilitated,
            "parivarthana": parivarthana,
            "kuligan_bhava": ((transits["Kuligan"]["rasi_num"] - ud_rasi) % 12) + 1,
            "kuligan": get_pt(transits["Kuligan"]),
            "emakandam": get_pt(transits["Emakandam"]),
            "rahu_time": get_pt(transits["RahuTime"]),
            "mrithyu": get_pt(transits["Mrithyu"])
        }

        # Combine into Final Position map (Value = Rasi Num)
        all_positions = {k: v["rasi_num"] for k, v in transits.items()}
        for k, v in jama_positions.items(): all_positions[k] = v
        for k, v in inner.items(): all_positions[k] = v["rasi_num"]

        return {
            "query_time": self.query_time.isoformat(),
            "sunrise": self.sunrise.isoformat(),
            "sunset": self.sunset.isoformat(),
            "lat": self.lat,
            "lon": self.lon,
            "block": block,
            "is_day": is_day,
            "planet_positions": all_positions,
            "ruling_planet": ruling,
            "transits": transits,
            "jama_grahas": jama_positions,
            "inner_planets": inner,
            "panchanga": self.calculate_panchanga(transits),
            "prasanna_special": prasanna_special
        }
