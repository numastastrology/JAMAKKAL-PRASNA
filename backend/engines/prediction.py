from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine
import ephem, math, datetime as _dt
from typing import Dict, Any, List, Tuple

class PredictionEngine:
    """
    World-Class Interpretation Engine for Jamakkol Prasna.
    Integrates Prashna (Now) with Janma (Birth) potential.
    Implements 80+ pinpoint specific scenarios and targeted Pariharams.
    """
    
    def __init__(self, jamakkal_data: Dict[str, Any], natal_data: Dict[str, Any] = None):
        self.jam = jamakkal_data # Added ref to full jam data for synthesis
        self.jamakkal = jamakkal_data
        self.natal = natal_data or {}
        
        # Core Architecture (The Four Pillars)
        inner = self.jamakkal.get("inner_planets", {})
        self.udayam = inner.get("Udayam", {}).get("rasi_num", 1) if isinstance(inner.get("Udayam"), dict) else inner.get("Udayam", 1)
        self.arudam = inner.get("Arudam", {}).get("rasi_num", 1) if isinstance(inner.get("Arudam"), dict) else inner.get("Arudam", 1)
        self.kavippu = inner.get("Kavippu", {}).get("rasi_num", 1) if isinstance(inner.get("Kavippu"), dict) else inner.get("Kavippu", 1)
        self.ruling_planet = self.jamakkal.get("ruling_planet", "Sun")
        
        # Positions & Transits - Sanitize to ensure ints for logic
        raw_positions = self.jam.get("planet_positions", {})
        self.positions = {k: (v.get("rasi_num", 1) if isinstance(v, dict) else v) for k, v in raw_positions.items()}
        self.transits = self.jam.get("transits", {})
        
        # Natal Data for Synthesis
        self.n_pos = self.natal.get("Positions", {})
        self.n_lords = self.natal.get("HouseLords", {})
        
        # Intent detection
        self.query_text = self.jamakkal.get("query_text", "").lower()
        self.intent = self._detect_intent()
        self.n_states = self.natal.get("PlanetaryStates", {})
        self.n_lagna = self.natal.get("LagnaRasi", 1)
        
        # Initialize Observer for transits
        self.obs = ephem.Observer()
        self.obs.lat = str(self.jamakkal.get("lat", 13.08))
        self.obs.lon = str(self.jamakkal.get("lon", 80.27))
        self.obs.pressure = 0
        q_time_iso = self.jamakkal.get("query_time")
        q_time = _dt.datetime.fromisoformat(q_time_iso) if q_time_iso else _dt.datetime.now()
        self.obs.date = (q_time - _dt.timedelta(hours=5, minutes=30)).strftime('%Y/%m/%d %H:%M:%S')

        self.house_lords = {
            1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon",
            5: "Sun", 6: "Mercury", 7: "Venus", 8: "Mars",
            9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"
        }

    def _detect_intent(self) -> str:
        if self.jamakkal.get("is_strict_competition_mode"):
            return "COMPETITION"
        if any(w in self.query_text for w in ["health", "sick", "disease", "recover", "doctor"]):
            return "HEALTH"
        if any(w in self.query_text for w in ["vs", "score", "win", "toss", "cricket", "football", "sport", "game", "election", "vote", "candidate", "poll", "result", "victory", "seat"]):
            return "COMPETITION"
        if any(w in self.query_text for w in ["marriag", "propos", "wed", "husband", "wife", "alliance", "match"]):
            return "MARRIAGE"
        if "match" in self.query_text:
            return "COMPETITION"
        return "GENERAL"

    def _has_natal(self) -> bool:
        """Returns True if natal birth data is available (Mode 2)."""
        return bool(self.natal and self.natal.get("Lagna"))

    def _get_natal_overlay(self) -> str:
        """Generates native-specific birth chart overlay for the conclusion (Mode 2 only)."""
        if not self._has_natal():
            return ""
        
        br = "<br/>"
        bull = "&#8226;"
        lagna = self.natal.get("Lagna", "")
        nakshatra = self.natal.get("Nakshatra", "")
        lagna_rasi = self.natal.get("LagnaRasi", 0)
        
        # Dasha info
        dasha = self.natal.get("Dasha", "")
        
        # Check natal planet states relevant to the intent
        states = self.natal.get("PlanetaryStates", {})
        
        # Lagna-Prasna alignment
        lagna_alignment = self._rel_house(self.udayam, lagna_rasi) if lagna_rasi else 0
        alignment_text = ""
        if lagna_alignment in [1, 5, 9]:
            alignment_text = "Birth Lagna and Prasna Udayam are in a trine (excellent alignment) — the query is deeply connected to your karmic path."
        elif lagna_alignment in [4, 7, 10]:
            alignment_text = "Birth Lagna and Prasna Udayam form a kendram (angular relationship) — strong action energy is available."
        elif lagna_alignment in [6, 8, 12]:
            alignment_text = "Birth Lagna and Prasna Udayam are in a dusthana relationship — extra effort and remedies are essential for this native."
        else:
            alignment_text = "Birth Lagna and Prasna Udayam have a neutral alignment — steady, measured progress is indicated."
        
        # Intent-specific natal insights
        natal_insight = ""
        if self.intent == "CAREER":
            sat_state = states.get("Saturn", "")
            sun_state = states.get("Sun", "")
            natal_insight = f"{bull} Natal Saturn: {sat_state or 'Normal'} — {'supports disciplined career growth' if 'Friend' in str(sat_state) else 'challenges in authority/structure require patience'}{br}"
            natal_insight += f"{bull} Natal Sun: {sun_state or 'Normal'} — {'leadership potential active in birth chart' if 'Friend' in str(sun_state) else 'native may need to build authority gradually'}{br}"
        elif self.intent == "MARRIAGE":
            ven_state = states.get("Venus", "")
            jup_state = states.get("Jupiter", "")
            natal_insight = f"{bull} Natal Venus: {ven_state or 'Normal'} — {'strong relationship karma' if 'Friend' in str(ven_state) or 'Direct' in str(ven_state) else 'relationship area needs careful nurturing'}{br}"
            natal_insight += f"{bull} Natal Jupiter: {jup_state or 'Normal'} — {'blessings for the union' if 'Friend' in str(jup_state) else 'guidance from elders recommended'}{br}"
        elif self.intent == "HEALTH":
            sun_state = states.get("Sun", "")
            moon_state = states.get("Moon", "")
            natal_insight = f"{bull} Natal Sun: {sun_state or 'Normal'} — {'strong constitution in birth chart' if 'Friend' in str(sun_state) else 'vitality needs periodic boosting'}{br}"
            natal_insight += f"{bull} Natal Moon: {moon_state or 'Normal'} — {'emotional stability supports recovery' if 'Direct' in str(moon_state) else 'mental stress may slow healing'}{br}"
        else:
            rp_state = states.get(self.ruling_planet, "")
            natal_insight = f"{bull} Natal {self.ruling_planet}: {rp_state or 'Normal'} — {'birth chart supports the Prasna ruling planet energy' if rp_state else 'neutral natal influence on the query'}{br}"

        overlay = (
            f"{br}{br}"
            f"<b>Birth Chart Overlay (Native-Specific):</b>{br}"
            f"{bull} Birth Lagna: {lagna} | Birth Nakshatra: {nakshatra}{br}"
            f"{bull} {alignment_text}{br}"
            f"{natal_insight}"
        )
        if dasha:
            overlay += f"{bull} Current Dasha: {dasha} — this period's energy interacts with the Prasna outcome.{br}"
        
        return overlay

    def _rel_house(self, target_sign: int, start_sign: int) -> int:
        return (target_sign - start_sign) % 12 + 1

    def _get_natal_fruition_window(self) -> str:
        """Returns a native-specific fruition window text based on birth chart.
        This describes how quickly the native will experience results AFTER the transit,
        NOT a change to the transit date itself (which is astronomical)."""
        if not self._has_natal():
            return ""
        
        days_min, days_max = self._get_natal_fruition_days()
        n_nak = self.natal.get("Nakshatra", "")
        speed = "rapid" if days_min <= 5 else "moderate" if days_min <= 10 else "gradual" if days_min >= 15 else "steady"
        
        states = self.natal.get("PlanetaryStates", {})
        rp_state = str(states.get(self.ruling_planet, ""))
        
        # Modifier from natal planet state
        if "Friend" in rp_state or "Own" in rp_state:
            modifier = "accelerated by supportive natal energy"
        elif "Enemy" in rp_state:
            modifier = "may require additional remedial effort"
        elif "Retrograde" in rp_state:
            modifier = "initially slow but gains momentum"
        else:
            modifier = "at a natural pace"
        
        return f"For this native ({self.natal.get('Lagna', '')} Lagna, {n_nak}), the effect is expected to manifest within {days_min}-{days_max} days of the transit — {speed} fruition, {modifier}."

    def _get_natal_fruition_days(self) -> Tuple[int, int]:
        """Returns the min and max days for fruition based on native alignment."""
        if not self._has_natal():
            return (10, 15)  # Default
            
        lagna_rasi = self.natal.get("LagnaRasi", 0)
        alignment = self._rel_house(self.udayam, lagna_rasi) if lagna_rasi else 0
        if alignment in [1, 5, 9]:  # Trine — fast fruition
            return (3, 5)
        elif alignment in [4, 7, 10]:  # Kendram — moderate
            return (7, 12)
        elif alignment in [6, 8, 12]:  # Dusthana — slow
            return (15, 25)
        else:
            return (10, 15)

    def _get_transit_date_raw(self) -> _dt.datetime:
        """Helper to get the raw transit datetime."""
        planet_map = {
            "Sun": ephem.Sun, "Moon": ephem.Moon, "Mars": ephem.Mars,
            "Mercury": ephem.Mercury, "Jupiter": ephem.Jupiter,
            "Venus": ephem.Venus, "Saturn": ephem.Saturn
        }
        planet_cls = planet_map.get(self.ruling_planet)
        if not planet_cls:
            return _dt.datetime.now() + _dt.timedelta(days=1)

        try:
            body = planet_cls()
            # Precise natural transit detection
            q_time_iso = self.jamakkal.get("query_time")
            q_time = _dt.datetime.fromisoformat(q_time_iso) if q_time_iso else _dt.datetime.now()
            self.obs.date = (q_time - _dt.timedelta(hours=5, minutes=30)).strftime('%Y/%m/%d %H:%M:%S') # Reset

            body.compute(self.obs)
            curr_rasi = self.positions.get(self.ruling_planet, 1)

            # Precise natural transit detection
            for day_offset in range(1, 400):
                self.obs.date = ephem.Date(self.obs.date + 1)
                body.compute(self.obs)
                ecl = math.degrees(float(ephem.Ecliptic(body).lon)) % 360
                d_dt = ephem.Date(self.obs.date).datetime()
                
                # Use same dynamic ayanamsha formula as JamakkalEngine
                aya = 23.85 + (d_dt.year - 2000) * 0.01388
                sidereal = (ecl - aya) % 360
                new_rasi = int(sidereal // 30) + 1
                
                if new_rasi != curr_rasi:
                    # Found boundary crossing, refine to hourly for precision
                    self.obs.date = ephem.Date(self.obs.date - 1)
                    for hour in range(25):
                        self.obs.date = ephem.Date(self.obs.date + (1/24))
                        body.compute(self.obs)
                        ecl_h = math.degrees(float(ephem.Ecliptic(body).lon)) % 360
                        d_h = ephem.Date(self.obs.date).datetime() + _dt.timedelta(hours=5, minutes=30)
                        aya_h = 23.85 + (d_h.year - 2000) * 0.01388
                        sid_h = (ecl_h - aya_h) % 360
                        if int(sid_h // 30) + 1 != curr_rasi:
                            return d_h
            
            return _dt.datetime.now() + _dt.timedelta(days=41)
        except Exception:
            return _dt.datetime.now() + _dt.timedelta(days=41)

    def _get_planet_data(self, planet_name: str) -> dict:
        """Get transit planet data — reads from 'transits' key (not inner_planets)."""
        return self.jamakkal.get("transits", {}).get(planet_name, {})

    def _get_analysis_for_category(self, category: str) -> Dict[str, List[str]]:
        """
        Returns dynamically generated challenges and remedies per category.
        All points are derived from the actual chart — positions, nakshatras, status, fruition.
        """
        challenges = []
        remedies = []
        rasi_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        def add_pt(clist, pt):
            if pt not in clist: clist.append(pt)

        # Core chart references
        ud_rel = self._rel_house(self.kavippu, self.udayam)
        ar_rel = self._rel_house(self.arudam, self.udayam)
        ud_rasi = rasi_names[(self.udayam - 1) % 12]
        ar_rasi = rasi_names[(self.arudam - 1) % 12]
        kav_rasi = rasi_names[(self.kavippu - 1) % 12]
        
        if category == "Health & Recovery":
            sun = self._get_planet_data("Sun")
            moon = self._get_planet_data("Moon")
            mars = self._get_planet_data("Mars")
            sun_status = sun.get("status", "Neutral Sign")
            sun_nak = sun.get("nakshatra", "")
            sun_rasi = sun.get("rasi", "")
            moon_rasi = moon.get("rasi", "")
            moon_nak = moon.get("nakshatra", "")
            mars_status = mars.get("status", "Neutral Sign")
            fruition = sun.get("fruition", "6 Months")
            
            add_pt(challenges, f"Sun (vitality significator) is in {sun_rasi} ({sun_status}), nakshatra {sun_nak} — {('strong vitality support' if 'Exalted' in sun_status or 'Own' in sun_status or 'Friendly' in sun_status else 'weakened healing energy, recovery needs external support')}.")
            add_pt(challenges, f"Moon (mind/body rhythm) transiting {moon_rasi} in {moon_nak} — {'stable mental health' if 'Friendly' in moon.get('status', '') or 'Own' in moon.get('status', '') else 'emotional stress may slow physical recovery'}.")
            add_pt(challenges, f"Kavippu block in {kav_rasi} ({ud_rel}H from Udayam) creates obstruction to the natural healing cycle.")
            add_pt(challenges, f"Mars ({mars_status}) in {mars.get('rasi', '')} — {'strong surgical/action energy' if 'Exalted' in mars_status else 'inflammation or internal heat imbalance possible'}.")
            add_pt(challenges, f"Arudam in {ar_rasi} ({ar_rel}H) — {'favorable recovery direction' if ar_rel in [1,5,9,11] else 'recovery path requires sustained disciplined effort'}.")
            
            add_pt(remedies, f"Offer water to the Sun at sunrise — Sun currently in {sun_nak}, invoke its healing energy.")
            add_pt(remedies, f"Moon is in {moon_nak}: follow a calming diet and avoid cold foods on Moon's transit days.")
            add_pt(remedies, "Chant 'Aditya Hridayam' or 'Om Suryaya Namaha' 11 times daily.")
            add_pt(remedies, f"Donate wheat or jaggery on Sundays to strengthen Sun's fruition ({fruition}).")
            add_pt(remedies, f"Perform Navagraha pooja to ease the Kavippu in {kav_rasi}.")

        elif category == "Business & Finance":
            merc = self._get_planet_data("Mercury")
            jup = self._get_planet_data("Jupiter")
            ven = self._get_planet_data("Venus")
            merc_status = merc.get("status", "Neutral Sign")
            merc_rasi = merc.get("rasi", "")
            merc_nak = merc.get("nakshatra", "")
            jup_status = jup.get("status", "Neutral Sign")
            jup_rasi = jup.get("rasi", "")
            jup_nak = jup.get("nakshatra", "")
            ven_fruition = ven.get("fruition", "2 Months")
            
            add_pt(challenges, f"Mercury (commerce lord) is in {merc_rasi} ({merc_status}), nakshatra {merc_nak} — {'sharp business acumen active' if 'Own' in merc_status or 'Friendly' in merc_status or 'Exalted' in merc_status else 'cash flow velocity and communication in deals may face friction'}.")
            add_pt(challenges, f"Jupiter (wealth significator) in {jup_rasi} ({jup_status}), nakshatra {jup_nak} — {'wealth accumulation supported' if 'Own' in jup_status or 'Exalted' in jup_status else 'profit margins under pressure, invest conservatively'}.")
            add_pt(challenges, f"Kavippu in {kav_rasi} ({ud_rel}H from Udayam) blocks the financial flow — {'minor delay' if ud_rel in [3,6,11] else 'significant block on new ventures until the energy shifts'}.")
            add_pt(challenges, f"Arudam in {ar_rasi} ({ar_rel}H) — {'supports financial gains and client trust' if ar_rel in [2,5,9,11] else 'hidden expenses or undisclosed liabilities present'}.")
            add_pt(challenges, f"Venus fruition indicator ({ven_fruition}): monetary returns timeline linked to Venus transit through {ven.get('nakshatra', '')}.")
            
            add_pt(remedies, f"Perform financial activities during Mercury Hora — Mercury is in {merc_nak} for optimal timing.")
            add_pt(remedies, f"Offer yellow flowers/turmeric to Jupiter — currently in {jup_nak}, enhancing wealth energy.")
            add_pt(remedies, "Chant 'Om Shreem Mahalakshmiye Namaha' 108 times on Fridays.")
            add_pt(remedies, f"Avoid major financial commitments on Tuesdays until Kavippu in {kav_rasi} eases.")
            add_pt(remedies, "Donate green gram (Moong) to cows/birds on Wednesdays for Mercury's blessing.")

        elif category == "Career & Professional":
            sat = self._get_planet_data("Saturn")
            sun = self._get_planet_data("Sun")
            jup = self._get_planet_data("Jupiter")
            sat_status = sat.get("status", "Neutral Sign")
            sat_rasi = sat.get("rasi", "")
            sat_nak = sat.get("nakshatra", "")
            sun_status = sun.get("status", "Neutral Sign")
            sun_rasi = sun.get("rasi", "")
            fruit_time = sat.get("fruition", "1 Year")
            
            add_pt(challenges, f"Saturn (career lord) in {sat_rasi} ({sat_status}), nakshatra {sat_nak} — {'disciplined effort will yield strong professional results' if 'Own' in sat_status or 'Exalted' in sat_status or 'Friendly' in sat_status else 'heavy workload with delayed recognition'}.")
            add_pt(challenges, f"Sun (authority) in {sun_rasi} ({sun_status}) — {'good rapport with superiors/leadership' if 'Exalted' in sun_status or 'Own' in sun_status or 'Friendly' in sun_status else 'friction with authority figures, proceed diplomatically'}.")
            add_pt(challenges, f"Kavippu in {kav_rasi} ({ud_rel}H from Udayam) creates {'minor' if ud_rel in [3,6,11] else 'significant'} career obstruction — {'office politics' if ud_rel in [6,8,12] else 'timing misalignment in key decisions'}.")
            add_pt(challenges, f"Jupiter (growth) in {jup.get('rasi', '')} ({jup.get('status', '')}) — {'expansion and promotion energy active' if 'Friendly' in jup.get('status', '') or 'Own' in jup.get('status', '') else 'growth pace slower than expected'}.")
            add_pt(challenges, f"Career fruition linked to Saturn's cycle ({fruit_time}): currently in {sat_nak}, patience required until transit completes.")
            
            add_pt(remedies, f"Light a sesame oil lamp on Saturdays — Saturn in {sat_nak} needs appeasement.")
            add_pt(remedies, f"Offer water to the rising Sun daily — Sun in {sun_rasi} strengthens authority energy.")
            add_pt(remedies, "Feed crows with cooked rice/sesame to honor Saturn's servant energy.")
            add_pt(remedies, f"Perform career actions during {self.ruling_planet} Hora for maximum impact.")
            add_pt(remedies, f"Significant career result expected in {fruit_time} — maintain consistent effort.")

        elif category == "Travel & Foreign":
            moon = self._get_planet_data("Moon")
            rah = self._get_planet_data("Rahu")
            sat = self._get_planet_data("Saturn")
            moon_status = moon.get("status", "Neutral Sign")
            moon_rasi = moon.get("rasi", "")
            moon_nak = moon.get("nakshatra", "")
            rah_rasi = rah.get("rasi", "")
            rah_nak = rah.get("nakshatra", "")
            
            add_pt(challenges, f"Moon (travel lord) in {moon_rasi} ({moon_status}), nakshatra {moon_nak} — {'favorable travel energy, plans will materialize' if 'Friendly' in moon_status or 'Own' in moon_status or 'Exalted' in moon_status else 'fluctuating plans, expect last-minute changes'}.")
            add_pt(challenges, f"Rahu (foreign influence) in {rah_rasi}, nakshatra {rah_nak} — {'strong foreign connection energy' if rah_rasi in ['Gemini', 'Virgo', 'Aquarius'] else 'documentation/visa process will face unexpected hurdles'}.")
            add_pt(challenges, f"Kavippu in {kav_rasi} ({ud_rel}H) — {'minor delay in departure' if ud_rel in [3,6,11] else 'significant obstacle creating travel postponement'}.")
            add_pt(challenges, f"Saturn in {sat.get('rasi', '')} ({sat.get('status', '')}) — {'structured travel, well-planned execution' if 'Own' in sat.get('status', '') else 'unexpected expenses or logistical friction during the journey'}.")
            add_pt(challenges, f"Arudam in {ar_rasi} ({ar_rel}H) — {'travel purpose will be fulfilled' if ar_rel in [1,5,9,11] else 'the travel may not fully achieve its primary objective'}.")
            
            add_pt(remedies, f"Offer milk to Shiva Lingam on Mondays — Moon in {moon_nak} needs lunar pacification.")
            add_pt(remedies, f"Carry a silver coin during travel — Moon transiting {moon_rasi} benefits from silver energy.")
            add_pt(remedies, "Chant 'Om Namah Shivaya' 108 times before departure.")
            add_pt(remedies, f"Avoid starting travel during Rahu Kalam — Rahu is in {rah_nak}.")
            add_pt(remedies, "Double-check all documentation; keep digital and physical copies.")

        elif category == "Marriage & Relationship":
            ven = self._get_planet_data("Venus")
            moon = self._get_planet_data("Moon")
            jup = self._get_planet_data("Jupiter")
            ven_status = ven.get("status", "Neutral Sign")
            ven_rasi = ven.get("rasi", "")
            ven_nak = ven.get("nakshatra", "")
            fruition = ven.get("fruition", "15 Days")
            
            add_pt(challenges, f"Venus (relationship lord) in {ven_rasi} ({ven_status}), nakshatra {ven_nak} — {'strong emotional harmony and attraction active' if 'Own' in ven_status or 'Exalted' in ven_status or 'Friendly' in ven_status else 'emotional misalignment creating friction in the relationship'}.")
            add_pt(challenges, f"Moon (mind/emotions) in {moon.get('rasi', '')} ({moon.get('status', '')}) — {'stable emotional foundation' if 'Friendly' in moon.get('status', '') else 'mood swings or overthinking complicating communication'}.")
            add_pt(challenges, f"Kavippu in {kav_rasi} ({ud_rel}H) — {'minor timing delay in alliance' if ud_rel in [3,6,11] else 'family or external pressure creating hesitation in the decision'}.")
            add_pt(challenges, f"Jupiter (blessing/dharma) in {jup.get('rasi', '')} — {'auspicious blessings for the union' if jup.get('rasi_num', 0) in [1,5,7,9] else 'need elder or guru guidance to align family expectations'}.")
            add_pt(challenges, f"Venus fruition period: {fruition} — relationship progress linked to Venus transit through {ven_nak}.")
            
            add_pt(remedies, f"Offer white flowers to Goddess Lakshmi on Fridays — Venus in {ven_nak} needs strengthening.")
            add_pt(remedies, f"Recite 'Om Shukraya Namaha' 108 times daily — Venus currently in {ven_rasi}.")
            add_pt(remedies, "Avoid arguments or ego clashes on Fridays and during Venus Hora.")
            add_pt(remedies, f"Donate sweets/milk products on Fridays to enhance Venus ({fruition} fruition).")
            add_pt(remedies, "Wear white or light-colored clothing on alliance meeting days.")

        elif category == "Disputes & Litigation":
            mars = self._get_planet_data("Mars")
            sat = self._get_planet_data("Saturn")
            rah = self._get_planet_data("Rahu")
            mars_status = mars.get("status", "Neutral Sign")
            mars_rasi = mars.get("rasi", "")
            mars_nak = mars.get("nakshatra", "")
            sat_status = sat.get("status", "Neutral Sign")
            
            add_pt(challenges, f"Mars (conflict lord) in {mars_rasi} ({mars_status}), nakshatra {mars_nak} — {'strong fighting energy, favorable for the native' if 'Exalted' in mars_status or 'Own' in mars_status else 'impulsive actions may weaken the case'}.")
            add_pt(challenges, f"Saturn (delay/justice) in {sat.get('rasi', '')} ({sat_status}) — {'justice process will be slow but fair' if 'Own' in sat_status else 'delays and procedural hurdles expected in the legal matter'}.")
            add_pt(challenges, f"Rahu in {rah.get('rasi', '')} ({rah.get('nakshatra', '')}) — {'hidden strategies by the opponent' if rah.get('rasi_num', 0) in [6,8,12] else 'unexpected twists possible in the dispute'}.")
            add_pt(challenges, f"Kavippu in {kav_rasi} ({ud_rel}H) — {'minor resistance' if ud_rel in [3,6,11] else 'strong opposition energy blocking a quick resolution'}.")
            add_pt(challenges, f"Arudam in {ar_rasi} ({ar_rel}H) — {'ultimately favorable outcome for the native' if ar_rel in [1,5,9,11] else 'the dispute may require compromise rather than outright victory'}.")
            
            add_pt(remedies, f"Recite 'Narasimha Kavacham' for protection — Mars in {mars_nak} needs warrior shielding.")
            add_pt(remedies, f"Light sesame oil lamp on Saturdays — Saturn ({sat_status}) governs the justice timeline.")
            add_pt(remedies, "Avoid confrontation on Tuesdays (Mars day) and Saturdays (Saturn day).")
            add_pt(remedies, "Donate food to the needy on Saturdays to appease Saturn's delay energy.")
            add_pt(remedies, "Seek mediation and out-of-court settlement where possible.")

        elif category == "Education & Knowledge":
            merc = self._get_planet_data("Mercury")
            jup = self._get_planet_data("Jupiter")
            moon = self._get_planet_data("Moon")
            merc_status = merc.get("status", "Neutral Sign")
            merc_rasi = merc.get("rasi", "")
            merc_nak = merc.get("nakshatra", "")
            jup_rasi = jup.get("rasi", "")
            jup_status = jup.get("status", "Neutral Sign")
            
            add_pt(challenges, f"Mercury (intellect lord) in {merc_rasi} ({merc_status}), nakshatra {merc_nak} — {'sharp memory and analytical ability active' if 'Own' in merc_status or 'Exalted' in merc_status or 'Friendly' in merc_status else 'concentration and retention may fluctuate'}.")
            add_pt(challenges, f"Jupiter (wisdom/guru) in {jup_rasi} ({jup_status}) — {'strong learning absorption and teacher support' if 'Own' in jup_status or 'Exalted' in jup_status else 'conceptual clarity needs extra effort'}.")
            add_pt(challenges, f"Moon in {moon.get('rasi', '')} ({moon.get('nakshatra', '')}) — {'stable focus and emotional balance for study' if 'Friendly' in moon.get('status', '') else 'distractions from emotional/personal matters'}.")
            add_pt(challenges, f"Kavippu in {kav_rasi} ({ud_rel}H) — {'minor disruption' if ud_rel in [3,6,11] else 'learning block due to stress or environment'} currently present.")
            add_pt(challenges, f"Arudam in {ar_rasi} ({ar_rel}H) — {'education goals will be achieved' if ar_rel in [1,4,5,9] else 'additional effort needed to reach desired academic outcome'}.")
            
            add_pt(remedies, f"Study facing the direction of Mercury's current energy — Mercury in {merc_nak}; facing East/North is ideal.")
            add_pt(remedies, f"Offer Tulsi leaves to Lord Vishnu on Wednesdays — Mercury in {merc_rasi} benefits from this.")
            add_pt(remedies, "Chant 'Om Aim Saraswatyai Namaha' 21 times before study sessions.")
            add_pt(remedies, f"Start study during Jupiter Hora — Jupiter in {jup_rasi} amplifies learning.")
            add_pt(remedies, "Consume soaked almonds daily; maintain a disciplined study schedule.")

        elif category == "Missing Objects":
            moon = self._get_planet_data("Moon")
            ar_sign = self.arudam
            direction_map = {
                1: "East", 2: "South-East", 3: "South", 4: "South-West",
                5: "North-West", 6: "North", 7: "North-East", 8: "East",
                9: "South-East", 10: "South", 11: "South-West", 12: "North-West"
            }
            direction = direction_map.get(ar_sign, "the direction of the Arudham")
            movable = ar_sign in [1, 4, 7, 10]
            
            add_pt(challenges, f"Arudam in {ar_rasi} ({ar_rel}H) points to the {direction} direction of your location.")
            add_pt(challenges, f"Object is likely {'movable — may have been taken or shifted by someone' if movable else 'stationary — misplaced in an overlooked spot nearby'}.")
            add_pt(challenges, f"Moon in {moon.get('rasi', '')} ({moon.get('nakshatra', '')}) — {'clear recall possible, search systematically' if 'Friendly' in moon.get('status', '') else 'memory gap about the last placement'}.")
            add_pt(challenges, f"Kavippu in {kav_rasi} ({ud_rel}H) — {'the object is recoverable with focused effort' if ud_rel in [3,5,9,11] else 'recovery is uncertain — there may be permanent loss or damage'}.")
            add_pt(challenges, f"Ruling planet {self.ruling_planet} indicates the object is related to {'metal/tools' if self.ruling_planet in ['Mars','Saturn'] else 'documents/paper' if self.ruling_planet in ['Mercury','Jupiter'] else 'jewelry/clothing' if self.ruling_planet in ['Venus','Moon'] else 'valuables'}.")
            
            add_pt(remedies, f"Search intensely in the {direction} sector of your home/office.")
            add_pt(remedies, "Chant 'Karthavirya Arjuna Mantra' — Om Karthaviryaya Namaha — 108 times.")
            add_pt(remedies, f"Check {'lower levels, under furniture, storage boxes' if not movable else 'with family members or visitors who were recently present'}.")
            add_pt(remedies, "Light a ghee lamp and pray to your Kuladevata for guidance.")
            add_pt(remedies, f"Best time to search: during {self.ruling_planet} Hora for heightened intuition.")
            add_pt(remedies, "Light a ghee lamp and pray to your Kuladevata for guidance.")

        elif category == "Competition & Success":
            mars = self._get_planet_data("Mars")
            merc = self._get_planet_data("Mercury")
            sun = self._get_planet_data("Sun")
            sat = self._get_planet_data("Saturn")
            
            add_pt(challenges, f"Mars (offensive energy) in {mars.get('rasi')} ({mars.get('status')}) — {'strong competitive drive' if 'Friend' in str(mars.get('status')) or 'Own' in str(mars.get('status')) else 'strategic caution required to avoid burnout'}.")
            add_pt(challenges, f"Mercury (calculations/toss) in {merc.get('rasi')} ({merc.get('status')}) — {'favorable tactical decisions likely' if 'Friend' in str(merc.get('status')) else 'adversary may use unexpected tactics'}.")
            add_pt(challenges, f"6th House (Opponents) Kavippu relationship: {'opposition is blocked/weakened' if ud_rel == 6 else 'opponents are active and challenging'}.")
            
            # Get 11th Lord position correctly
            h11_lord = self.house_lords.get(f"{(self.udayam+10)%12 or 12}th")
            h11_pos_rasi = self.positions.get(h11_lord, 1)
            add_pt(challenges, f"11th House (Success) Lord {h11_lord} in {rasi_names[(h11_pos_rasi-1)%12]} — indicates the path to victory.")
            
            add_pt(remedies, "Worship Lord Hanuman for strength and mental toughness.")
            add_pt(remedies, f"Execute key strategic moves during {self.ruling_planet} Hora.")
            add_pt(remedies, "Carry a small piece of red cloth or sandalwood for Mars' protection.")
            add_pt(remedies, f"Significant outcome expected around {self.transits.get(self.ruling_planet, {}).get('fruition', '41 days')}.")

        # Dynamic filler points based on chart (not hardcoded)
        transits = self.jamakkal.get("transits", {})
        if len(challenges) < 10:
            add_pt(challenges, f"Ruling planet {self.ruling_planet} in {transits.get(self.ruling_planet, {}).get('rasi', '')} ({transits.get(self.ruling_planet, {}).get('status', '')}) indicates timing adjustments needed.")
            add_pt(challenges, f"Arudam in {ar_rasi} ({ar_rel}H from Udayam) — {'positive intent validation' if ar_rel in [1,5,9,11] else 'hidden variables at play that need careful navigation'}.")
            add_pt(challenges, f"Udayam in {ud_rasi} — the query's energy is {('cardinal — rapid action needed' if self.udayam in [1,4,7,10] else 'fixed — patience required' if self.udayam in [2,5,8,11] else 'dual — flexibility will be key')}.")
            rp_data = transits.get(self.ruling_planet, {})
            add_pt(challenges, f"{self.ruling_planet} in nakshatra {rp_data.get('nakshatra', '')} (star lord: {rp_data.get('star_lord', '')}) — {('supportive star lord' if rp_data.get('star_status', '') in ['Friendly Star', 'Own Star'] else 'challenging star lord, extra effort required')}.")
            add_pt(challenges, f"Kavippu distance from Udayam ({ud_rel}H) shows {'mild' if ud_rel in [3,6,11] else 'moderate' if ud_rel in [2,5] else 'intense'} resistance to the desired outcome.")
            
        if len(remedies) < 10:
            rp = self.ruling_planet
            rp_data = transits.get(rp, {})
            add_pt(remedies, f"Perform key actions during {rp} Hora — {rp} is in {rp_data.get('nakshatra', '')} for optimal timing.")
            add_pt(remedies, f"Light a sesame oil lamp at dusk — Kavippu in {kav_rasi} needs regular pacification.")
            add_pt(remedies, f"Feed crows or stray animals regularly — Saturn ({transits.get('Saturn', {}).get('rasi', '')}) governs karmic debts.")
            add_pt(remedies, f"Recite your Ishta Devata mantra 108 times daily for 41 days — aligned with {rp}'s transit cycle.")
            add_pt(remedies, f"Donate to charitable causes on the day of {rp} to strengthen its fruition ({rp_data.get('fruition', '41 days')}).")

        # Natal-specific points (Mode 2 — Prasna + Birth Data)
        if self._has_natal():
            rasi_names_local = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
            n_lagna = self.natal.get("Lagna", "")
            n_nak = self.natal.get("Nakshatra", "")
            n_states = self.natal.get("PlanetaryStates", {})
            n_naks = self.natal.get("Nakshatras", {})
            n_positions = self.natal.get("Positions", {})
            
            # Lagna alignment with Prasna
            lagna_rasi = self.natal.get("LagnaRasi", 0)
            if lagna_rasi:
                lagna_house = self._rel_house(self.udayam, lagna_rasi)
                if lagna_house in [1, 5, 9]:
                    add_pt(challenges, f"Birth Lagna ({n_lagna}) forms a trine with Prasna Udayam — strong karmic alignment for this query.")
                elif lagna_house in [6, 8, 12]:
                    add_pt(challenges, f"Birth Lagna ({n_lagna}) is in a dusthana from Prasna Udayam — native needs extra persistence for this matter.")
                else:
                    add_pt(challenges, f"Birth Lagna ({n_lagna}) in {lagna_house}H from Prasna Udayam — moderate alignment, steady effort yields results.")
            
            # Category-specific natal points
            if category == "Health & Recovery":
                sun_state = n_states.get("Sun", "Normal")
                moon_nak = n_naks.get("Moon", "")
                add_pt(challenges, f"Native birth nakshatra {n_nak} — health vulnerabilities linked to this star require attention.")
                add_pt(remedies, f"Natal Sun state: {sun_state} — {'maintain current health regimen' if 'Friend' in str(sun_state) else 'strengthen Sun with Surya Namaskar daily'}.")
                add_pt(remedies, f"Natal Moon in {moon_nak} — follow a diet aligned with Moon's nakshatra energy for faster recovery.")
            elif category == "Career & Professional":
                sat_state = n_states.get("Saturn", "Normal")
                mer_state = n_states.get("Mercury", "Normal")
                add_pt(challenges, f"Natal Saturn ({sat_state}) — {'disciplined career growth in birth chart' if 'Friend' in str(sat_state) else 'natal chart shows delayed career rewards, persistence needed'}.")
                add_pt(challenges, f"Birth nakshatra {n_nak} — professional strengths linked to this star should be leveraged.")
                add_pt(remedies, f"Natal Mercury ({mer_state}) — {'communication skills are a native strength' if 'Direct' in str(mer_state) else 'strengthen communication through Mercury remedies'}.")
            elif category == "Marriage & Relationship":
                ven_state = n_states.get("Venus", "Normal")
                jup_state = n_states.get("Jupiter", "Normal")
                add_pt(challenges, f"Natal Venus ({ven_state}) — {'strong relationship karma in birth chart' if 'Friend' in str(ven_state) else 'relationship sector needs nurturing from birth chart perspective'}.")
                add_pt(challenges, f"Birth nakshatra {n_nak} — compatibility analysis should factor this star for best matching.")
                add_pt(remedies, f"Natal Jupiter ({jup_state}) — {'guru blessings support the alliance' if 'Friend' in str(jup_state) else 'seek elder guidance and perform Jupiter remedies'}.")
            elif category == "Finance & Wealth":
                jup_state = n_states.get("Jupiter", "Normal")
                ven_state = n_states.get("Venus", "Normal")
                add_pt(challenges, f"Natal Jupiter ({jup_state}) — {'wealth potential supported in birth chart' if 'Friend' in str(jup_state) else 'financial growth requires strategic planning per birth chart'}.")
                add_pt(remedies, f"Natal Venus ({ven_state}) — {'luxury and comfort supported' if 'Friend' in str(ven_state) else 'strengthen Venus with Friday fasting for material gains'}.")
            else:
                add_pt(challenges, f"Birth nakshatra {n_nak} with Lagna {n_lagna} — native's inherent strengths should be channeled for this matter.")
                rp_n_state = n_states.get(self.ruling_planet, "")
                if rp_n_state:
                    add_pt(remedies, f"Natal {self.ruling_planet} ({rp_n_state}) — {'birth chart supports the ruling planet' if 'Friend' in str(rp_n_state) else 'perform specific remedies for ' + self.ruling_planet + ' to align natal and Prasna energies'}.")

        return {"challenges": challenges[:12], "solutions": remedies[:12]}

    def _generate_deep_points(self) -> Tuple[List[str], List[str], List[str]]:
        """Synthesizes high-depth, unique points for the main dashboard."""
        rasi_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        curr_rasi = self.positions.get(self.ruling_planet, 1)
        next_rasi_num = (curr_rasi % 12) + 1
        next_rasi = rasi_names[next_rasi_num - 1]
        speed = 'Rapid' if self.udayam in [1, 4, 7, 10] else 'Slow-Steady'

        if self.intent == "CAREER":
            diag = [
                f"Architecture: Udayam @ House {self.udayam}, Arudham @ House {self.arudam} — Job Change Configuration.",
                f"Primary Block: Kavippu at House {self._rel_house(self.kavippu, self.udayam)} restricts current employment energy.",
                f"Career Modulator: {self.ruling_planet} governs this professional transition moment.",
                f"Manifestation Speed: {speed} — outcome reflects the effort invested in the transition.",
                f"10th House Energy: Current chart validates the native's desire for professional change."
            ]
            transit_date_raw = self._get_transit_date_raw()
            transit_date_str = f"approximately around {transit_date_raw.strftime('%B %d, %Y')}"
            final_manifest_date = (transit_date_raw + _dt.timedelta(days=41)).strftime('%B %d, %Y')
            
            rec_time = "48-72 hours" if speed == 'Rapid' else "7-10 days"
            rec = [
                f"Initial Clarity: First signs of direction visible within {rec_time}.",
                "Interview / Decision Window: 15-20 days — a key opportunity will emerge.",
                f"Peak Manifestation: Full career outcome expected approximately around {final_manifest_date} (Transit + 41 days).",
                f"Shift Factor: Your ruling planet {self.ruling_planet} moving to {next_rasi} ({transit_date_str}) triggers the job change unlock.",
                "Persistence Note: Continue pursuing; the transition energy is active but requires consistent action."
            ]
            rem = [
                "Worship Lord Murugan or Surya on Sundays for career boost.",
                f"Perform new career-related actions during the {self.ruling_planet} Hora for best results.",
                "Carry a piece of raw turmeric in your pocket during job interviews.",
                "Light camphor at home on the day of submitting applications or attending interviews.",
                "Avoid announcing your job-change plans to colleagues until the offer is confirmed."
            ]

        elif self.intent == "MARRIAGE":
            diag = [
                f"Architecture: Udayam @ House {self.udayam}, Arudham @ House {self.arudam} — Alliance Configuration.",
                f"Primary Block: Kavippu at House {self._rel_house(self.kavippu, self.udayam)} creates hesitation in alliance decision.",
                f"7th House Modulator: {self.ruling_planet} influences the compatibility and timing of the proposal.",
                f"Manifestation Speed: {speed} — relationship energies move with this pattern.",
                "Venus & Moon alignment in the chart validates the emotional sincerity of this query."
            ]
            transit_date_raw = self._get_transit_date_raw()
            transit_date_str = f"approximately around {transit_date_raw.strftime('%B %d, %Y')}"
            final_manifest_date = (transit_date_raw + _dt.timedelta(days=41)).strftime('%B %d, %Y')

            rec_time = "48-72 hours" if speed == 'Rapid' else "7-10 days"
            rec = [
                f"Initial Signs: Family inclination or first response visible within {rec_time}.",
                "Formal Discussion Window: 21-30 days — ideal for formal alliance talks.",
                f"Final Decision: Marriage/Alliance resolution expected approximately around {final_manifest_date} (Transit + 41 days).",
                f"Shift Factor: Your ruling planet {self.ruling_planet} moving to {next_rasi} ({transit_date_str}) opens the alliance gate.",
                "Auspicious Timing: Consult an elder or astrologer before the formal meeting for best results."
            ]
            rem = [
                "Offer white flowers and milk to Goddess Parvati on Fridays.",
                "Recite 'Om Shukraya Namaha' 108 times daily for Venus (relationship) blessings.",
                "Avoid conflict or ego clashes in family settings during this period.",
                "Send a gift or sweet on Friday before the formal proposal meeting.",
                "Wear white or light blue clothing on the day of the alliance discussion."
            ]

        elif self.intent == "HEALTH":
            diag = [
                f"Architecture: Udayam @ House {self.udayam}, Arudham @ House {self.arudam} — Health Query.",
                f"Primary Block: Kavippu at House {self._rel_house(self.kavippu, self.udayam)} affects recovery rhythm.",
                f"Healing Modulator: {self.ruling_planet} governs the body's current recovery energy.",
                f"Manifestation Speed: {speed} — reflects the pace of physical healing.",
                "Sun–Moon balance in the chart determines the vitality level for this period."
            ]
            transit_date_raw = self._get_transit_date_raw()
            transit_date_str = f"approximately around {transit_date_raw.strftime('%B %d, %Y')}"
            final_manifest_date = (transit_date_raw + _dt.timedelta(days=41)).strftime('%B %d, %Y')

            rec_time = "48-72 hours" if speed == 'Rapid' else "7-10 days"
            rec = [
                f"Symptomatic Relief: Expect first improvement within {rec_time}.",
                "Stabilization: Sustained improvement expected within 15-21 days.",
                f"Full Recovery: Complete healing cycle expected approximately around {final_manifest_date} (Transit + 41 days).",
                f"Shift Factor: {self.ruling_planet} entering {next_rasi} ({transit_date_str}) marks the turning point for recovery.",
                "Maintenance: Adhere strictly to prescribed remedies to avoid relapse."
            ]
            rem = [
                "Offer water to the rising Sun at dawn (Surya Arghya) for vitality.",
                "Chant 'Aditya Hridayam' or 'Om Suryaya Namaha' for 21 days.",
                "Maintain a strictly light, sattvic (pure) diet for the first 7 days.",
                "Avoid cold baths or cold food; prefer warm water and fresh cooked meals.",
                "Donate wheat, jaggery, or copper items on the next Sunday."
            ]

        elif self.intent == "COMPETITION":
            diag = [
                f"Architecture: Udayam @ House {self.udayam}, Arudham @ House {self.arudam} — Competition Configuration.",
                f"Conflict Vector: 6th House (Opponents) vs 11th House (Victory) analysis is active.",
                f"Primary Block: Kavippu at House {self._rel_house(self.kavippu, self.udayam)} indicates where the resistance lies.",
                f"Manifestation Speed: {speed} — outcome depends on the quality of strategy.",
                "Mars and Mercury alignment indicates the blend of force and intellect in this event."
            ]
            transit_date_raw = self._get_transit_date_raw()
            transit_date_str = f"approximately around {transit_date_raw.strftime('%B %d, %Y')}"
            final_manifest_date = (transit_date_raw + _dt.timedelta(days=41)).strftime('%B %d, %Y')

            rec_time = "48-72 hours" if speed == 'Rapid' else "7-10 days"
            rec = [
                f"Initial Momentum: Strategy begins to take effect within {rec_time}.",
                "Critical Event Window: Significant developments or the event itself within the transit cycle.",
                f"Final Result: Success/Victory resolution expected approximately around {final_manifest_date} (Transit + 41 days).",
                f"Shift Factor: {self.ruling_planet} entering {next_rasi} ({transit_date_str}) marks the victory gate opening.",
                "Tactical Advice: Maintain composure and adapt to changing conditions during the event."
            ]
            rem = [
                "Recite 'Hanuman Chalisa' or 'Kanda Sashti Kavasam' for victory.",
                f"Perform key competitive moves during {self.ruling_planet} or Mars Hora.",
                "Donate food or donate to a sports/community cause on a Tuesday.",
                "Keep a small piece of raw turmeric or red sandalwood for protection.",
                "Maintain absolute focus; avoid sharing strategy with outsiders."
            ]

        else:  # GENERAL
            diag = [
                f"Architecture: Udayam @ House {self.udayam}, Arudham @ House {self.arudam}.",
                f"Primary Block: Kavippu at House {self._rel_house(self.kavippu, self.udayam)} influences the query outcome.",
                f"Ruling Modulator: {self.ruling_planet} governs the quality and speed of manifestation.",
                f"Manifestation Speed: {speed} — the result will follow this energy pattern.",
                "Natal alignment with the current Prasna confirms the query's karmic relevance."
            ]
            transit_date_raw = self._get_transit_date_raw()
            transit_date_str = f"approximately around {transit_date_raw.strftime('%B %d, %Y')}"
            final_manifest_date = (transit_date_raw + _dt.timedelta(days=41)).strftime('%B %d, %Y')

            rec_time = "48-72 hours" if speed == 'Rapid' else "7-10 days"
            rec = [
                f"Phase 1: First indicators of change visible within {rec_time}.",
                "Phase 2: Tangible progress expected within 21-30 days.",
                f"Phase 3: Complete resolution expected approximately around {final_manifest_date} (Transit + 41 days).",
                f"Shift Factor: {self.ruling_planet} moving to {next_rasi} ({transit_date_str}) is the key transition trigger.",
                "Consistency: Performing the recommended remedies without interruption ensures lasting results."
            ]
            rem = [
                "Light a sesame oil lamp at dusk in the prayer room daily.",
                f"Perform your key activities during the {self.ruling_planet} Hora for best results.",
                "Donate food or essential items to those in need on an auspicious day.",
                "Maintain mental peace; avoid arguments or major decisions when agitated.",
                "Recite your chosen deity's mantra 108 times daily for 41 days."
            ]

        # Natal-specific deep points (Mode 2 — Prasna + Birth Data)
        if self._has_natal():
            n_lagna = self.natal.get("Lagna", "")
            n_nak = self.natal.get("Nakshatra", "")
            n_states = self.natal.get("PlanetaryStates", {})
            n_naks = self.natal.get("Nakshatras", {})
            lagna_rasi = self.natal.get("LagnaRasi", 0)

            # Add native-specific diagnostic point
            if lagna_rasi:
                lagna_house = self._rel_house(self.udayam, lagna_rasi)
                alignment = "trine (excellent)" if lagna_house in [1,5,9] else "kendram (strong action)" if lagna_house in [4,7,10] else "dusthana (challenging)" if lagna_house in [6,8,12] else "neutral"
                diag.append(f"Birth Chart Alignment: Lagna ({n_lagna}) is in {lagna_house}H from Prasna Udayam — {alignment} alignment for this query.")
            
            # Add native-specific recovery/timeline point
            rp_natal_state = n_states.get(self.ruling_planet, "")
            if rp_natal_state:
                rec.append(f"Natal Factor: Birth chart {self.ruling_planet} is {rp_natal_state} — {'accelerates' if 'Friend' in str(rp_natal_state) else 'modulates'} the Prasna timeline.")
            rec.append(f"Native Nakshatra: {n_nak} — the birth star energy {'supports' if n_nak else 'influences'} the recovery rhythm.")
            
            # Add native-specific fruition window
            fruition_window = self._get_natal_fruition_window()
            if fruition_window:
                rec.append(f"Timeline Milestone: {fruition_window}")

            # Add native-specific remedy point
            moon_nak = n_naks.get("Moon", "")
            if self.intent == "CAREER":
                sat_state = n_states.get("Saturn", "Normal")
                rem.append(f"Birth Saturn ({sat_state}): {'maintain discipline and consistency' if 'Friend' in str(sat_state) else 'perform Saturn remedies — donate black items on Saturdays'}.")
            elif self.intent == "MARRIAGE":
                ven_state = n_states.get("Venus", "Normal")
                rem.append(f"Birth Venus ({ven_state}): {'relationship energy is strong in birth chart' if 'Friend' in str(ven_state) or 'Direct' in str(ven_state) else 'strengthen Venus — offer white flowers on Fridays'}.")
            elif self.intent == "HEALTH":
                sun_state = n_states.get("Sun", "Normal")
                rem.append(f"Birth Sun ({sun_state}): {'constitutional vitality is supported' if 'Friend' in str(sun_state) else 'boost vitality with Surya Namaskar and copper vessel water'}.")
            else:
                rem.append(f"Birth Nakshatra {n_nak}: align remedies with your janma star for enhanced results.")

        return diag, rec, rem

    def _calculate_holistic_score(self, category: str, base_score: float) -> float:
        """Calculates a deep, sensitive score by weighing Prasna and Natal synergy."""
        score = base_score
        if not self._has_natal():
            return min(max(score, 1.0), 10.0)

        # 1. Birth Lagna Alignment (+1.5, +0.75, -1.0)
        n_lagna_rasi = self.natal.get("LagnaRasi", 0)
        if n_lagna_rasi:
            rel = self._rel_house(self.udayam, n_lagna_rasi)
            if rel in [1, 5, 9]:
                score += 1.5
            elif rel in [4, 7, 10]:
                score += 0.75
            elif rel in [6, 8, 12]:
                score -= 1.0

        # Category Significators for Natal Check
        cat_map = {
            "Health & Recovery": "Sun",
            "Business & Finance": "Jupiter",
            "Career & Professional": "Saturn",
            "Travel & Foreign": "Moon",
            "Marriage & Relationship": "Venus",
            "Disputes & Litigation": "Mars",
            "Education & Knowledge": "Mercury",
            "Missing Objects": "Mercury"
        }
        
        sig = cat_map.get(category)
        if sig:
            # 2. Significator Natal Strength
            n_state = str(self.natal.get("PlanetaryStates", {}).get(sig, ""))
            if "Friend" in n_state or "Own" in n_state or "Exalted" in n_state:
                score += 1.25
            elif "Enemy" in n_state or "Debilitated" in n_state:
                score -= 1.25
            elif "Retrograde" in n_state:
                score -= 0.5
            
            # 3. Ruling Planet vs Natal Lord Synergy
            # Mapping category to house number (approximate)
            house_map = {
                "Health & Recovery": 1,
                "Business & Finance": 2,
                "Career & Professional": 10,
                "Travel & Foreign": 9,
                "Marriage & Relationship": 7,
                "Disputes & Litigation": 6,
                "Education & Knowledge": 5,
                "Missing Objects": 4
            }
            h_num = house_map.get(category)
            if h_num:
                n_lord = self.natal.get("HouseLords", {}).get(f"{h_num}th")
                if n_lord == self.ruling_planet:
                    score += 1.0
                
        # 4. Final smoothing and range capping
        return min(max(round(score, 1), 1.0), 10.0)

    def _get_category_data(self, lang: str = "en") -> Dict[str, Dict[str, Any]]:
        categories = ["Health & Recovery", "Business & Finance", "Career & Professional", "Travel & Foreign", 
                      "Marriage & Relationship", "Disputes & Litigation", "Education & Knowledge", "Missing Objects", "Competition & Success"]
        
        results = {}
        for cat in categories:
            data = self._get_analysis_for_category(cat)
            
            # Base logic: Jamakkol Kavippu distance
            ud_to_kav = self._rel_house(self.kavippu, self.udayam)
            base_score = 7.5 if ud_to_kav in [5, 9, 11] else 3.5 if ud_to_kav in [1, 6, 8, 12] else 5.5
            
            # Calculate deep score (Mode 2 aware)
            score = self._calculate_holistic_score(cat, base_score)
            
            status = "Excellent" if score >= 8 else "Strong" if score >= 6 else "Moderate" if score >= 4 else "Challenging"
            
            results[cat] = {
                "score": score,
                "status": status,
                "challenges": data["challenges"],
                "solutions": data["solutions"]
            }
        return results

    def _calculate_remedial_timing(self) -> Dict[str, Any]:
        """Calculates the Shanti Jama (Ideal 90-min Interval) and Ideal Day."""
        # 1. Shanti Jama logic
        best_jama_planet = None
        for p_name in ["Jupiter", "Venus", "Mercury"]:
            pos = self.positions.get(f"Jama {p_name}")
            if pos and pos != self.kavippu:
                rel = self._rel_house(pos, self.udayam)
                if rel in [1, 5, 9, 11]:
                    best_jama_planet = p_name
                    break
        
        # 2. Ideal Day logic from Natal
        janma_star = self.natal.get("Nakshatra", "Your Birth Star")
        sadhana_star = self.natal.get("SadhanaStar", "6th Star")
        
        timing_advice = [
            f"Ideal Day: Start remedies on {janma_star} or {sadhana_star} day.",
            f"Shanti Jama: Best performed during the {best_jama_planet or 'Jupiter'} Jamam.",
            "Avoid: Do not start during Chandrashtama or while under Kavippu.",
            f"Phase: The {self.jamakkal.get('panchanga', {}).get('Tithi', 'Waxing')} phase is highly supportive."
        ]
        
        return {
            "best_jama_planet": best_jama_planet,
            "ideal_janma_star": janma_star,
            "ideal_sadhana_star": sadhana_star,
            "timing_advice": timing_advice
        }

    def generate_full_report_data(self, lang: str = "en"):
        diag, rec, rem = self._generate_deep_points()
        all_cat_data = self._get_category_data(lang)
        timing_data = self._calculate_remedial_timing()
        
        summary = f"Synthesized Analysis: Udayam @ {self.udayam}, Arudham @ {self.arudam}, Kavippu @ {self.kavippu}."
        
        # Intent-specific Final Conclusion — Query-Aware, Elaborative with HTML formatting
        rasi_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        # Run Synthesis Engine early to use findings in conclusions
        s_engine = SynthesisEngine(self.jam, self.jam.get('query_text', ''), self.natal)
        s_result = s_engine.generate_synthesis()
        transit_date_raw, next_rasi = s_engine._get_kavippu_lift_date_raw()
        transit_date = f"approximately around {transit_date_raw.strftime('%B %d, %Y')}"
        # Calculate Fruition Window Dates
        f_min, f_max = self._get_natal_fruition_days()
        fruition_start = (transit_date_raw + _dt.timedelta(days=f_min)).strftime('%B %d, %Y')
        fruition_end = (transit_date_raw + _dt.timedelta(days=f_max)).strftime('%B %d, %Y')
        fruition_window_str = f"{fruition_start} to {fruition_end}"
        
        # Calculate synchronized secondary dates
        # Point 2 (Initial Clarity): shortly after or during fruition start
        clarity_days = max(2, f_min)
        clarity_date = (transit_date_raw + _dt.timedelta(days=clarity_days)).strftime('%B %d, %Y')
        
        # Point 3 (Concrete Opportunity): f_max + buffer
        opp_days_min = f_max + 2
        opp_days_max = f_max + 10
        
        final_manifest_date = (transit_date_raw + _dt.timedelta(days=41)).strftime('%B %d, %Y')
        br = "<br/>"
        bull = "&#8226;"

        # Build query-specific context
        raw_query = self.jam.get('query_text', '').strip()
        query_ctx = raw_query if raw_query else "the queried matter"
        kav_rel = self._rel_house(self.kavippu, self.udayam)
        prefix = ""
        findings = s_result.get('findings', {})
        diag_injection = ""
        if self.intent == "HEALTH":
            d = findings.get('diagnosis', 'vulnerable areas')
            b = findings.get('block', 'energy centers')
            diag_injection = f" Specifically, the chart points to the **{d}** as the primary affected region, with a temporary energy block in the **{b}**."

        if self.intent == "CAREER":
            favour = "favourably aligned" if kav_rel in [5, 9, 11] else "challenging but manageable"
            final = (
                f'{prefix}Based on the Jamakkal Prasna analysis regarding "{query_ctx}", '
                f"the configuration is {favour}.{diag_injection} "
                f"The ruling planet {self.ruling_planet} is the key driver - once it transits into {next_rasi} ({transit_date}), "
                f"the native will see a clear opening for the desired professional outcome."
                f"{br}{br}"
                f"<b>Outcome Forecast:</b>{br}"
                f"{bull} <b>FRUITION WINDOW: {fruition_window_str}</b> — key results manifest post-transit.{br}"
                f"{bull} Initial clarity and signs of direction will emerge around {clarity_date}.{br}"
                f"{bull} A concrete opportunity (interview, offer, or lead) is expected between {opp_days_min}-{opp_days_max} days post-transit.{br}"
                f"{bull} Full professional manifestation expected approximately around {final_manifest_date} (Transit + 41 days).{br}"
                f"{bull} The Kavippu block in {kav_rel}H will naturally dissolve with the shift."
                f"{br}{br}"
                f"<b>Essential Actions to Accelerate Results:</b>{br}"
                f"{bull} Perform all career-related activities during {self.ruling_planet} Hora for maximum benefit{br}"
                f"{bull} Light camphor and pray to your Ishta Devata before important meetings{br}"
                f"{bull} Follow the prescribed Pariharams without interruption for the full 41-day cycle{br}"
                f"{bull} Maintain positive intent and avoid sharing plans with others until confirmed"
            )
        elif self.intent == "MARRIAGE":
            favour = "positive with steady progress" if kav_rel in [5, 9, 11] else "requiring patience"
            final = (
                f'The Jamakkal Prasna analysis regarding "{query_ctx}" indicates the outcome is {favour}.{diag_injection} '
                f"{self.ruling_planet}'s transit to {next_rasi} ({transit_date}) marks the auspicious window for the alliance to progress."
                f"{br}{br}"
                f"<b>Outcome Forecast:</b>{br}"
                f"{bull} <b>FRUITION WINDOW: {fruition_window_str}</b> — alliance gate opens and manifests here.{br}"
                f"{bull} Family discussions and initial alignment will gain momentum around {clarity_date}.{br}"
                f"{bull} A formal proposal or decisive meeting is likely between {opp_days_min}-{opp_days_max} days post-transit.{br}"
                f"{bull} Final commitment expected approximately around {final_manifest_date} (Transit + 41 days).{br}"
                f"{bull} The karmic delays indicated by Kavippu in {kav_rel}H will ease with the shift."
                f"{br}{br}"
                f"<b>Essential Actions to Accelerate Results:</b>{br}"
                f"{bull} Offer white flowers to Goddess Parvati/Lakshmi on Fridays{br}"
                f"{bull} Recite 'Om Shukraya Namaha' 108 times daily for relationship harmony{br}"
                f"{bull} Maintain patience and avoid pressuring the other party during the waiting period{br}"
                f"{bull} Follow all prescribed Pariharams consistently for the full 41-day cycle"
            )
        elif self.intent == "HEALTH":
            favour = "recovery is well-supported" if kav_rel in [5, 9, 11] else "recovery needs sustained effort"
            final = (
                f'The Jamakkal Prasna analysis regarding "{query_ctx}" indicates that {favour}.{diag_injection} '
                f"The planetary ruler {self.ruling_planet} shifting to {next_rasi} ({transit_date}) will mark the point of significant improvement."
                f"{br}{br}"
                f"<b>Recovery Forecast:</b>{br}"
                f"{bull} <b>FRUITION WINDOW: {fruition_window_str}</b> — significant relief and healing manifest.{br}"
                f"{bull} Initial symptomatic improvement expected around {clarity_date}.{br}"
                f"{bull} Sustained stabilization and noticeble health gains between {opp_days_min}-{opp_days_max} days post-transit.{br}"
                f"{bull} Full recovery expected approximately around {final_manifest_date} (Transit + 41 days).{br}"
                f"{bull} The health blockage from Kavippu in {kav_rel}H will release with the transition."
                f"{br}{br}"
                f"<b>Essential Actions to Accelerate Recovery:</b>{br}"
                f"{bull} Strictly adhere to medical advice and prescribed medications{br}"
                f"{bull} Offer water to the rising Sun daily (Surya Arghya) for vitality{br}"
                f"{bull} Maintain a light, sattvic diet and adequate rest{br}"
                f"{bull} Follow all prescribed spiritual remedies consistently for the full recovery cycle"
            )
        elif self.intent == "COMPETITION":
            favour = "positive with strong winning potential" if kav_rel in [5, 9, 11] else "requiring strategic persistence"
            final = (
                f'The Jamakkal Prasna analysis regarding "{query_ctx}" indicates the outcome is {favour}.{diag_injection} '
                f"The ruling planet {self.ruling_planet} shifting to {next_rasi} ({transit_date}) marks the key moment for the win."
                f"{br}{br}"
                f"<b>Outcome Forecast:</b>{br}"
                f"{bull} <b>FRUITION WINDOW: {fruition_window_str}</b> — competitive edge and victory manifest here.{br}"
                f"{bull} Initial strategy and tactical alignment will show results around {clarity_date}.{br}"
                f"{bull} A significant breakthrough or clear advantage is likely between {opp_days_min}-{opp_days_max} days post-transit.{br}"
                f"{bull} Final victory/goal fulfillment expected approximately around {final_manifest_date} (Transit + 41 days).{br}"
                f"{bull} The competitive hurdles indicated by Kavippu in {kav_rel}H will ease with the shift."
                f"{br}{br}"
                f"<b>Essential Actions to Accelerate Results:</b>{br}"
                f"{bull} Worship Lord Hanuman for strength and obstacle removal{br}"
                f"{bull} Perform key event-related activities during {self.ruling_planet} Hora{br}"
                f"{bull} Maintain mental discipline and avoid reactive decisions{br}"
                f"{bull} Follow all prescribed Pariharams consistently for the full cycle"
            )
        else:
            favour = "positive" if kav_rel in [5, 9, 11] else "requiring disciplined effort"
            final = (
                f'The Jamakkal Prasna analysis regarding "{query_ctx}" indicates the configuration is {favour}.{diag_injection} '
                f"The key planetary transition of {self.ruling_planet} into {next_rasi} ({transit_date}) will be the defining shift point."
                f"{br}{br}"
                f"<b>Outcome Forecast:</b><br/>"
                f"{bull} <b>FRUITION WINDOW: {fruition_window_str}</b> — desired outcome starts to manifest.{br}"
                f"{bull} First signs of positive movement expected around {clarity_date}.{br}"
                f"{bull} Tangible progress and visible results between {opp_days_min}-{opp_days_max} days post-transit.{br}"
                f"{bull} Complete resolution/desired outcome expected approximately around {final_manifest_date} (Transit + 41 days).{br}"
                f"{bull} The Kavippu block in {kav_rel}H will naturally dissolve with the planetary shift."
                f"{br}{br}"
                f"<b>Essential Actions to Accelerate Results:</b>{br}"
                f"{bull} Perform key activities during {self.ruling_planet} Hora for best timing{br}"
                f"{bull} Light a sesame oil lamp at dusk daily during the 41-day Prasna window{br}"
                f"{bull} Recite your Ishta Devata mantra 108 times daily{br}"
                f"{bull} Follow all prescribed Pariharams without interruption for the full cycle"
            )

        # Append natal overlay for Mode 2 (Prasna + Birth Data)
        natal_overlay = self._get_natal_overlay()
        if natal_overlay:
            final += natal_overlay

        # Advanced Synthesis Breakdown
        # Move s_result call earlier as done above

        res = {
            "summary": summary,
            "analysis_points": diag,
            "diagnostic_analysis": diag,
            "recovery_timeline": rec,
            "remedies": rem,
            "remedy_timing": timing_data,
            "synthesis_points": s_result["points"],
            "synthesis_conclusion": s_result["conclusion"],
            "final_conclusion": final,
            "balance_categories": all_cat_data,
            "location": self.jam.get('location') or "Chennai",
            "birth_place": self.jam.get('birth_place'),
            "lat": self.jam.get('lat'),
            "lon": self.jam.get('lon'),
            "ruling_planet": self.ruling_planet,
            "block": self.jamakkal.get("block"),
            "is_day": self.jamakkal.get("is_day"),
            "positions": self.positions,
            "panchanga": self.jamakkal.get("panchanga"),
            "transits": self.jamakkal.get("transits"),
            "jama_grahas": self.jamakkal.get("jama_grahas"),
            "inner_planets": self.jamakkal.get("inner_planets"),
            "sunrise_str": self.jamakkal.get("sunrise"),
            "sunset_str": self.jamakkal.get("sunset"),
            "query_time_str": self.jamakkal.get("query_time"),
            "natal": self.natal
        }
        
        if hasattr(s_engine, 'cricket_data'):
            res['cricket_data'] = s_engine.cricket_data
            
        return res
