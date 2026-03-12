from typing import Dict, Any, List, Optional
import re
import ephem, math, datetime as _dt

class SynthesisEngine:
    """
    Advanced Synthesis Engine for Jamakkal Prasna.
    Implements Professional Horary Standards with deep elaborative narrative.
    Generates 15 customer-friendly synthesis points with full indications.
    """

    KAVIPPU_EXPLANATION = ("Kavippu (the planetary energy block — an invisible obstruction "
                           "that temporarily slows progress in the indicated area of life)")

    RASI_BODY_PARTS = {
        1: "Head, Face, Cerebrum",
        2: "Neck, Throat, Cervical region",
        3: "Shoulders, Arms, Lungs, Hands",
        4: "Chest, Heart, Stomach",
        5: "Upper Abdomen, Spinal column, Liver",
        6: "Lower Abdomen, Intestines, Digestive system",
        7: "Kidneys, Bladder, Lumbar region",
        8: "Genitals, Reproductive system, Rectum",
        9: "Hips, Thighs, Arterial system",
        10: "Knees, Joints, Bones",
        11: "Calves, Ankles, Circulatory system",
        12: "Feet, Toes, Lymphatic system"
    }

    PLANET_HEALTH_SIGNIFICANCE = {
        "Sun": "Vitality, Heart, Right Eye (Male), Bones",
        "Moon": "Blood, Fluids, Left Eye (Male), Mind/Nerves",
        "Mars": "Muscles, Heat, Surgery, Accidents, Marrow",
        "Mercury": "Nervous system, Skin, Speech, Lungs",
        "Jupiter": "Liver, Fat, Ears, Growth, Arteries",
        "Venus": "Kidneys, Reproductive health, Vision, Hormones",
        "Saturn": "Chronic pain, Joints, Teeth, Spleen, Gastric issues",
        "Rahu": "Unexpected symptoms, Toxins, Phobias, Undiagnosable ailments",
        "Ketu": "Sudden pains, Viral infections, Neurological blocks, Spiritual health"
    }

    def __init__(self, jamakkal_data: Dict[str, Any], query_text: str = "", natal_data: Dict[str, Any] = None):
        self.jam = jamakkal_data
        self.query_text = query_text.lower()
        self.natal = natal_data or {}
        
        # Inner pillars
        inner = self.jam.get("inner_planets", {})
        self.udayam = self._extract_rasi(inner.get("Udayam"))
        self.arudam = self._extract_rasi(inner.get("Arudam"))
        self.kavippu = self._extract_rasi(inner.get("Kavippu"))
        
        # Positions & Transits - Sanitize to ensure ints for logic
        raw_positions = self.jam.get("planet_positions", {})
        self.positions = {k: (v.get("rasi_num", 1) if isinstance(v, dict) else v) for k, v in raw_positions.items()}
        self.transits = self.jam.get("transits", {})
        self.ruling_planet = self.jam.get("ruling_planet", "Sun")
        
        # Initialize Observer for transits
        self.obs = ephem.Observer()
        self.obs.lat = str(self.jam.get("lat", 13.08))
        self.obs.lon = str(self.jam.get("lon", 80.27))
        self.obs.pressure = 0
        q_time = _dt.datetime.fromisoformat(self.jam.get("query_time")) if self.jam.get("query_time") else _dt.datetime.now()
        self.obs.date = (q_time - _dt.timedelta(hours=5, minutes=30)).strftime('%Y/%m/%d %H:%M:%S')
        
        self.house_lords = {
            1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon",
            5: "Sun", 6: "Mercury", 7: "Venus", 8: "Mars",
            9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"
        }
        
        self.intent = self._detect_intent()

    def _extract_rasi(self, data):
        if isinstance(data, dict): return data.get("rasi_num", 1)
        return data if isinstance(data, int) else 1

    def _get_house_num(self, rasi: int, start_rasi: int) -> int:
        return (rasi - start_rasi + 12) % 12 + 1

    def _detect_intent(self) -> str:
        if self.jam.get("is_strict_competition_mode"):
            return "COMPETITION"
        text = self.query_text
        if any(w in text for w in ["health", "sick", "disease", "recover", "doctor", "pain", "hospital", "illness", "body", "physical", "mental"]):
            return "HEALTH"
        if any(w in text for w in ["vs", "score", "win", "toss", "cricket", "football", "sport", "game", "election", "vote", "candidate", "poll", "result", "victory", "seat"]):
            return "COMPETITION"
        if any(w in text for w in ["marriag", "propos", "wed", "husband", "wife", "alliance", "match", "partner", "love"]):
            return "MARRIAGE"
        if "match" in text:
            return "COMPETITION"
        return "GENERAL"

    def _get_planet_details(self, name: str) -> str:
        t = self.transits.get(name, {})
        if not t: return name
        return f"{name} ({t.get('rasi')} @ {t.get('degree')})"

    def _get_house_placement_meaning(self, house_num: int, lord_name: str, context: str = "career") -> str:
        """Returns customer-friendly interpretation of a lord placed in a specific house."""
        career_meanings = {
            1: f"This is a strong position — {lord_name} in the 1st house means the native has direct control over career advancement. Professional growth depends on personal initiative.",
            2: f"{lord_name} in the 2nd house indicates career is closely tied to financial stability. The native may see income growth through the current professional path.",
            3: f"{lord_name} in the 3rd house suggests career progress through communication, short travels, or sibling/peer connections. The native needs to be more proactive.",
            4: f"{lord_name} in the 4th house indicates comfort at current workplace but limited growth. A home-based or familiar environment role may suit better.",
            5: f"{lord_name} in the 5th house is excellent — creativity, intellect, and past merit (Poorva Punya) support the career. Positive outcomes are likely.",
            6: f"{lord_name} in the 6th house brings competition and challenges. The native may face workplace conflicts but can overcome them with persistence.",
            7: f"{lord_name} in the 7th house indicates career growth through partnerships, negotiations, client-facing roles, or business alliances. Collaborative opportunities are key.",
            8: f"{lord_name} in the 8th house suggests sudden changes or hidden obstacles in the career path. There may be a transformation — an old role ending and a new one beginning.",
            9: f"{lord_name} in the 9th house is very auspicious — fortune, blessings from elders/mentors, and long-distance opportunities favor the career.",
            10: f"{lord_name} in the 10th house (own house) is the strongest placement. The native's career is in a powerful position and recognition is imminent.",
            11: f"{lord_name} in the 11th house is excellent for gains. Career efforts will yield tangible financial rewards, networking gains, and fulfilled ambitions.",
            12: f"{lord_name} in the 12th house indicates career opportunities abroad or through foreign connections. There may be some expenses or sacrifices needed."
        }
        marriage_meanings = {
            1: f"{lord_name} in the 1st house indicates the alliance will be driven by the native's own choice and initiative.",
            2: f"{lord_name} in the 2nd house connects the alliance to family wealth and stability. Family involvement is strong.",
            3: f"{lord_name} in the 3rd house suggests the alliance may come through siblings, neighbors, or short-distance connections.",
            4: f"{lord_name} in the 4th house indicates domestic happiness and emotional compatibility in the alliance.",
            5: f"{lord_name} in the 5th house is very positive — love, children, and intellectual compatibility are strong.",
            6: f"{lord_name} in the 6th house brings challenges — disagreements, health issues, or interference from rivals.",
            7: f"{lord_name} in the 7th house (own house) is ideal — the alliance has strong mutual attraction and compatibility.",
            8: f"{lord_name} in the 8th house may bring hidden complications or in-law issues. Patience is needed.",
            9: f"{lord_name} in the 9th house brings blessings — the alliance has strong dharmic support and elder approval.",
            10: f"{lord_name} in the 10th house connects the alliance to professional or social status.",
            11: f"{lord_name} in the 11th house is very favorable — gains, wish fulfillment, and a supportive partner.",
            12: f"{lord_name} in the 12th house suggests a foreign-connected alliance or one requiring some sacrifices."
        }
        if context == "marriage":
            return marriage_meanings.get(house_num, f"{lord_name} in {house_num}H influences the alliance direction.")
        return career_meanings.get(house_num, f"{lord_name} in {house_num}H influences the career direction.")

    def _get_house_distance_meaning(self, distance: int) -> str:
        """Returns interpretation of the distance between the Udayam Lord and the relevant house lord."""
        meanings = {
            1: "very closely aligned — strong personal connection with the outcome.",
            2: "connected through finances — material stability drives the outcome.",
            3: "linked through efforts and communication — initiative is required.",
            4: "connected through comfort zones — stability is a priority.",
            5: "in a harmonious trine — merit and past good deeds support the outcome.",
            6: "in a challenging aspect — obstacles exist but can be overcome with effort.",
            7: "in opposition — there is tension between personal desires and external factors. Compromise is needed.",
            8: "in a stressful aspect — unexpected changes or transformations are possible.",
            9: "in a fortunate trine — divine blessings and guru support favor the outcome.",
            10: "in a strong angular relationship — authority figures and career structures play a key role.",
            11: "in a gain-oriented aspect — the outcome is likely to bring tangible benefits and fulfilled desires.",
            12: "in a detachment aspect — there may be some losses or expenses before the final gain."
        }
        return meanings.get(distance, "indicating a neutral relationship between the energies.")

    def _get_natal_fruition_window(self) -> str:
        """Returns native-specific fruition text — how quickly effect manifests AFTER the transit."""
        if not self.natal or not self.natal.get("Lagna"):
            return ""
        
        lagna_rasi = self.natal.get("LagnaRasi", 0)
        states = self.natal.get("PlanetaryStates", {})
        n_nak = self.natal.get("Nakshatra", "")
        rp_state = str(states.get(self.ruling_planet, ""))
        
        alignment = self._get_house_num(lagna_rasi, self.udayam) if lagna_rasi else 0
        if alignment in [1, 5, 9]:
            window = "within 3-5 days of the transit"
            speed = "rapid"
        elif alignment in [4, 7, 10]:
            window = "within 7-12 days of the transit"
            speed = "moderate"
        elif alignment in [6, 8, 12]:
            window = "within 15-25 days of the transit"
            speed = "gradual"
        else:
            window = "within 10-15 days of the transit"
            speed = "steady"
        
        if "Friend" in rp_state or "Own" in rp_state:
            modifier = "accelerated by supportive natal energy"
        elif "Enemy" in rp_state:
            modifier = "may require additional remedial effort"
        elif "Retrograde" in rp_state:
            modifier = "initially slow but gains momentum"
        else:
            modifier = "at a natural pace"
        
        return f" For this native ({self.natal.get('Lagna', '')} Lagna, {n_nak}), effects manifest {window} — {speed} fruition, {modifier}."

    def _get_kavippu_lift_date_raw(self) -> Tuple[_dt.datetime, str]:
        """Helper to get the raw datetime when Kavippu eases. Supports Retrograde Nodes."""
        try:
            # Precise natural transit detection
            q_time_iso = self.jam.get("query_time")
            q_time = _dt.datetime.fromisoformat(q_time_iso) if q_time_iso else _dt.datetime.now()
            self.obs.date = (q_time - _dt.timedelta(hours=5, minutes=30)).strftime('%Y/%m/%d %H:%M:%S')
            curr_rasi = self.positions.get(self.ruling_planet, 1)

            planet_map = {
                "Sun": ephem.Sun, "Moon": ephem.Moon, "Mars": ephem.Mars,
                "Mercury": ephem.Mercury, "Jupiter": ephem.Jupiter,
                "Venus": ephem.Venus, "Saturn": ephem.Saturn
            }
            rp_cls = planet_map.get(self.ruling_planet)

            for day in range(1, 600): # Increased range for slow planets
                self.obs.date = ephem.Date(self.obs.date + 1)
                
                if rp_cls:
                    body = rp_cls()
                    body.compute(self.obs)
                    ecl = math.degrees(float(ephem.Ecliptic(body).lon)) % 360
                else:
                    # Handle Rahu/Snake/Ketu
                    d = float(self.obs.date) - float(ephem.Date('2000/01/01 12:00:00'))
                    ecl = (125.04452 - 0.0529537652 * d) % 360
                    if self.ruling_planet in ["Ketu", "Dragon's Tail"]:
                        ecl = (ecl + 180) % 360
                
                d_dt = ephem.Date(self.obs.date).datetime()
                aya = 23.85 + (d_dt.year - 2000) * 0.01388
                sidereal = (ecl - aya) % 360
                new_rasi = int(sidereal // 30) + 1
                
                if new_rasi != curr_rasi:
                    # Refine to hourly
                    for hour in range(25):
                        self.obs.date = ephem.Date(self.obs.date - (1/24))
                        if rp_cls:
                            body.compute(self.obs)
                            ecl_h = math.degrees(float(ephem.Ecliptic(body).lon)) % 360
                        else:
                            d_h_raw = float(self.obs.date) - float(ephem.Date('2000/01/01 12:00:00'))
                            ecl_h = (125.04452 - 0.0529537652 * d_h_raw) % 360
                            if self.ruling_planet in ["Ketu", "Dragon's Tail"]:
                                ecl_h = (ecl_h + 180) % 360
                                
                        d_h = ephem.Date(self.obs.date).datetime() + _dt.timedelta(hours=5, minutes=30)
                        aya_h = 23.85 + (d_h.year - 2000) * 0.01388
                        sid_h = (ecl_h - aya_h) % 360
                        new_rasi_h = int(sid_h // 30) + 1
                        if new_rasi_h == curr_rasi:
                            # We stepped back into the current rasi, so step forward 1 hour and return
                            return d_h + _dt.timedelta(hours=1), self._get_sign_name(new_rasi)
            
            return _dt.datetime.now() + _dt.timedelta(days=41), "Unknown"
        except Exception as e:
            return _dt.datetime.now() + _dt.timedelta(days=41), "Unknown"

    def generate_synthesis(self) -> Dict[str, Any]:
        points = []
        num = 1
        self.findings = {}
        
        # ────────────────────────────────────────────────────
        # 1. ARUDAM VALIDATION (The Root)
        # ────────────────────────────────────────────────────
        aru_house = self._get_house_num(self.arudam, self.udayam)
        pt1 = f"{num:02d}. ARUDAM ({self._get_sign_name(self.arudam)}) in {aru_house}H from UDAYAM ({self._get_sign_name(self.udayam)}). "
        if aru_house in [1, 5, 9, 11]:
            pt1 += "This validates the seeker's intense focus and high probability of success for the query."
        elif aru_house in [2, 10]:
            pt1 += "Indicates the query is rooted in material gains and status stability."
        else:
            pt1 += "Suggests the query arises from a period of flux or external pressures."
        points.append(pt1)
        num += 1

        # ────────────────────────────────────────────────────
        # 2-7. INTENT SPECIFIC LOGIC (6 points)
        # ────────────────────────────────────────────────────
        if self.intent == "CAREER":
            pts, num = self._generate_career_points(num)
            points.extend(pts)
        elif self.intent == "MARRIAGE":
            pts, num = self._generate_marriage_points(num)
            points.extend(pts)
        elif self.intent == "HEALTH":
            pts, num, findings = self._generate_health_points(num)
            points.extend(pts)
            self.findings.update(findings)
        elif self.intent == "COMPETITION":
            is_cricket = any(w in self.query_text.lower() for w in ["cricket", "match", "score", "toss", "vs"])
            if is_cricket:
                self.cricket_data = self._calculate_cricket_prediction()
            pts, num = self._generate_competition_points(num)
            points.extend(pts)
        else:
            pts, num = self._generate_general_points(num)
            points.extend(pts)

        # ────────────────────────────────────────────────────
        # 8. KAVIPPU (THE BLOCK) — with full explanation
        # ────────────────────────────────────────────────────
        kav_h = self._get_house_num(self.kavippu, self.udayam)
        pt_kav = f"{num:02d}. {self.KAVIPPU_EXPLANATION} is in {kav_h}H ({self._get_sign_name(self.kavippu)}). "
        if kav_h == 1:
            pt_kav += "This directly blocks the seeker's initiative — expect delays in starting new actions. "
        elif kav_h == 10:
            pt_kav += "This indicates a professional hurdle or hidden enmity at the workplace. "
        elif kav_h == 7:
            pt_kav += "This suggests opposition from partners, clients, or significant delays in agreements and collaborations. "
        elif kav_h == 6:
            pt_kav += "This creates health-related obstacles or workplace competition that slows progress. "
        elif kav_h == 8:
            pt_kav += "This brings hidden fears, sudden setbacks, or karmic delays that test patience. "
        elif kav_h == 12:
            pt_kav += "This causes expenses, sleep disturbance, or foreign-related complications. "
        else:
            pt_kav += f"This impacts the {self._get_sign_significance(kav_h)} area of life currently. "
        
        lift_date, next_sign_name = self._get_kavippu_lift_date_raw()
        lift_time = f"approximately around {lift_date.strftime('%B %d, %Y')}"
        pt_kav += f"The block is expected to ease {lift_time} when the ruling planet shifts to {next_sign_name}."
        
        # Add native-specific fruition window
        fruition_window = self._get_natal_fruition_window()
        if fruition_window:
            pt_kav += f" {fruition_window}"
            
        points.append(pt_kav)
        num += 1

        # ────────────────────────────────────────────────────
        # 9. KAVIPPU REMEDY
        # ────────────────────────────────────────────────────
        kav_remedy = f"{num:02d}. REMEDY FOR KAVIPPU BLOCK: "
        if kav_h in [1, 7, 10]:
            kav_remedy += "Light a sesame oil lamp on Saturdays and donate black sesame seeds. Chant 'Om Namah Shivaya' 108 times to dissolve the obstruction."
        elif kav_h in [6, 8, 12]:
            kav_remedy += "Perform 'Navagraha Pooja' or offer raw turmeric and green gram at a temple. Avoid making impulsive decisions during this period."
        else:
            kav_remedy += "Offer prayers to your Kuladevata (family deity) and feed crows or stray animals. Maintain daily prayer routine for 41 days."
        points.append(kav_remedy)
        num += 1

        mo_pos = self.positions.get("Moon", 1)
        mo_house = self._get_house_num(mo_pos, self.udayam)
        pt_mo = f"{num:02d}. MOON (Mind/Emotions) at {mo_house}H from Udayam ({self._get_sign_name(mo_pos)}). "
        if self.intent == "HEALTH":
            if mo_house in [6, 8, 12]:
                pt_mo += "This transit suggests high mental anxiety or fluid-related imbalances affecting health. Stress management is critical for recovery."
            else:
                pt_mo += "Mental resolve is strong, supporting the physical recovery process. A calm mind will accelerate healing."
        else:
            if mo_house in [1, 5, 9]:
                pt_mo += "The native is strongly resolved and mentally prepared for the outcome. Confidence levels are high."
            elif mo_house in [4, 7, 10]:
                pt_mo += "The native has moderate mental clarity but may experience mood swings or indecisiveness."
            else:
                pt_mo += "There is considerable mental stress and uncertainty about the next steps. Calming remedies are recommended."
        points.append(pt_mo)
        num += 1

        # ────────────────────────────────────────────────────
        jup_pos = self.positions.get("Jupiter", 1)
        jup_house = self._get_house_num(jup_pos, self.udayam)
        pt_jup = f"{num:02d}. JUPITER (Fortune/Blessings) at {jup_house}H from Udayam ({self._get_sign_name(jup_pos)}). "
        if self.intent == "HEALTH":
            if jup_house in [1, 5, 9, 11]:
                pt_jup += "Jupiter's protective energy is active, ensuring the body's natural vitality (Ojas) remains strong against illness."
            else:
                pt_jup += "Jupiter's support is indirect; the native may need to focus on liver/digestive health and follow disciplined medical advice."
        else:
            if jup_house in [1, 5, 9, 11]:
                pt_jup += "Jupiter's blessings are active — divine support, guru guidance, and luck favor the query outcome."
            elif jup_house in [2, 10]:
                pt_jup += "Jupiter supports financial stability and social reputation, but spiritual effort is needed for full blessings."
            else:
                pt_jup += "Jupiter's blessings are not directly aligned. Additional prayers to Lord Guru (Brihaspati) are recommended to attract fortune."
        points.append(pt_jup)
        num += 1

        # ────────────────────────────────────────────────────
        sun_pos = self.positions.get("Sun", 1)
        sun_house = self._get_house_num(sun_pos, self.udayam)
        pt_sun = f"{num:02d}. SUN (Authority/Vitality) at {sun_house}H from Udayam ({self._get_sign_name(sun_pos)}). "
        if self.intent == "HEALTH":
            if sun_house in [6, 8, 12]:
                pt_sun += "Sun in a challenging house indicates lowered immunity or vital energy. Sun prayers and Vitamin D are recommended."
            else:
                pt_sun += "The Sun's position supports a strong constitution and the will to recover quickly."
        else:
            if sun_house in [1, 5, 9, 10]:
                pt_sun += "Authority figures and government processes are supportive. Approvals or recognition are likely in the near term."
            elif sun_house in [6, 8, 12]:
                pt_sun += "Challenges from authority figures or government processes. Avoid confrontations with superiors and maintain documentation."
            else:
                pt_sun += "Neutral influence from authority figures. The native should proactively seek support from mentors or seniors."
        points.append(pt_sun)
        num += 1

        # ────────────────────────────────────────────────────
        # 13. RAHU-KETU AXIS
        # ────────────────────────────────────────────────────
        rahu_pos = self.positions.get("Rahu", 1)
        ketu_pos = self.positions.get("Ketu", 1)
        rahu_house = self._get_house_num(rahu_pos, self.udayam)
        ketu_house = self._get_house_num(ketu_pos, self.udayam)
        pt_rk = f"{num:02d}. RAHU-KETU AXIS: Rahu at {rahu_house}H ({self._get_sign_name(rahu_pos)}) and Ketu at {ketu_house}H ({self._get_sign_name(ketu_pos)}). "
        if rahu_house in [3, 6, 11]:
            pt_rk += "Rahu in an Upachaya house is favorable — unconventional approaches and bold moves will yield results."
        elif rahu_house in [1, 7, 10]:
            pt_rk += "Rahu in a Kendra house creates intense ambition but also confusion. Avoid shortcuts and stay ethical."
        else:
            pt_rk += "Rahu's placement indicates some karmic patterns that may cause unexpected twists. Patience and spiritual remedies are advised."
        points.append(pt_rk)
        num += 1

        # ────────────────────────────────────────────────────
        # 14. MALEFICS IN KENDRAS CHECK
        # ────────────────────────────────────────────────────
        kendras = [1, 4, 7, 10]
        malefics = ["Mars", "Saturn", "Rahu", "Ketu"]
        mal_in_kendra = []
        for m in malefics:
            m_pos = self.positions.get(m, 0)
            if m_pos and self._get_house_num(m_pos, self.udayam) in kendras:
                mal_in_kendra.append(m)
        
        pt_mal = f"{num:02d}. MALEFIC CHECKPOINT: "
        if mal_in_kendra:
            pt_mal += f"{', '.join(mal_in_kendra)} {'is' if len(mal_in_kendra) == 1 else 'are'} in Kendra houses (1/4/7/10). "
            pt_mal += "This indicates active obstacles in the path. Extra effort and remedies are needed to overcome them."
        else:
            pt_mal += "No major malefics in Kendra houses — the path has fewer direct obstacles. Progress will be smoother with consistent effort."
        points.append(pt_mal)
        num += 1

        # ────────────────────────────────────────────────────
        # 15. NATAL OVERLAY (IF AVAILABLE)
        # ────────────────────────────────────────────────────
        if self.natal:
            n_lagna = self.natal.get("LagnaRasi", 1)
            n_house = self._get_house_num(n_lagna, self.udayam)
            pt_nat = f"{num:02d}. JANMA LAGNA (Birth Ascendant) in {n_house}H from Prashna Udayam. "
            if n_house in [1, 5, 9, 11]:
                pt_nat += "The birth potential is currently in synergy with the transit configuration — a highly supportive alignment for success."
            elif n_house in [2, 10]:
                pt_nat += "The birth chart supports material outcomes but needs spiritual alignment for full effect."
            else:
                pt_nat += "Extra remedial effort is needed to align birth karmas with current desires. Follow the prescribed remedies consistently."
            points.append(pt_nat)
        else:
            pt_nat = f"{num:02d}. NATAL DATA: Birth chart data was not provided. For a more accurate and personalized analysis, include the native's birth details."
            points.append(pt_nat)

        # ────────────────────────────────────────────────────
        # CONCLUSION
        # ────────────────────────────────────────────────────
        conclusion = self._generate_conclusion()
        
        # Append natal overlay for Mode 2 (Prasna + Birth Data)
        natal_overlay = self._get_natal_conclusion_overlay()
        if natal_overlay:
            # Also include fruition window in the synthesis conclusion if not already there
            fruition = self._get_natal_fruition_window()
            if fruition:
                natal_overlay += f"<br/><b>Fruition Timeline:</b> {fruition}"
            conclusion += natal_overlay

        # Final Ruling Planet specific summary (The Head of Timing)
        rp_data = self.transits.get(self.ruling_planet, {})
        rp_name = "Snake" if self.ruling_planet == "Snake" else self.ruling_planet
        pt_rp = f"{num:02d}. RULING PLANET {rp_name.upper()} in {rp_data.get('rasi', 'N/A')} at {rp_data.get('degree', 'N/A')}. "
        pt_rp += f"The key to resolution lies in its transit. Star Lord: {rp_data.get('star_lord', 'N/A')}. Nakshatra: {rp_data.get('nakshatra', 'N/A')}."
        points.append(pt_rp)
        num += 1

        return {
            "points": points,
            "conclusion": conclusion,
            "findings": self.findings
        }

    def _generate_career_points(self, num: int):
        """Generates 6 career-specific synthesis points with full indications."""
        pts = []
        h10_rasi = (self.udayam + 9) % 12 or 12
        h10_lord = self.house_lords[h10_rasi]
        h10_pos = self.positions.get(h10_lord, 1)
        h10_house = self._get_house_num(h10_pos, self.udayam)
        
        # Point: 10L Placement — with full indication
        meaning = self._get_house_placement_meaning(h10_house, h10_lord, "career")
        pts.append(f"{num:02d}. Professional Lord (10L) {h10_lord} is placed in {h10_house}H. {meaning}")
        num += 1

        # Point: 10L alignment check with Arudam/Kavippu
        if h10_pos == self.arudam:
            pts.append(f"{num:02d}. 10L ({h10_lord}) is aligned with Arudam — this confirms professional status is the primary driving force right now. The native's ambition is directly channelized towards career outcomes.")
        elif h10_pos == self.kavippu:
            lift_date = self._get_kavippu_lift_date_raw()
            lift_time = f"approximately around {lift_date.strftime('%B %d, %Y')}"
            pts.append(f"{num:02d}. 10L ({h10_lord}) is overshadowed by {self.KAVIPPU_EXPLANATION}. This indicates a temporary professional 'cutoff' or block — the native may feel stuck in the current role. This block is expected to ease {lift_time}. Remedy: Light a sesame oil lamp on Saturdays, chant 'Om Shanaischaraya Namaha' 108 times, and avoid making impulsive career decisions until the block lifts.")
        else:
            h10_to_aru = self._get_house_num(h10_pos, self.arudam)
            pts.append(f"{num:02d}. 10L ({h10_lord}) and Arudam are {h10_to_aru} houses apart — career energy and desire alignment is {'strong' if h10_to_aru in [1, 5, 9] else 'moderate, requiring focused effort'}.")
        num += 1
        
        # Saturn (Natural Career Indicator)
        sat_pos = self.positions.get("Saturn", 1)
        sat_house = self._get_house_num(sat_pos, self.udayam)
        sat_detail = f"{num:02d}. Saturn (Karma-Karaka, the planet of hard work and discipline) sits in {sat_house}H. "
        if sat_house in [3, 6, 10, 11]:
            sat_detail += "Saturn in an Upachaya house supports career growth through sustained effort. Hard work will be recognized and rewarded."
        elif sat_house in [1, 4, 7]:
            sat_detail += "Saturn in a Kendra house brings intense work pressure and responsibility. The native may feel burdened but results will come through persistence."
        else:
            sat_detail += "Saturn's placement suggests delays and patience are required. Avoid shortcuts — the karmic lesson here is perseverance."
        pts.append(sat_detail)
        num += 1
        
        # Stress Check — always include for CAREER
        h6_rasi = (self.udayam + 5) % 12 or 12
        h6_lord = self.house_lords[h6_rasi]
        h6_pos = self.positions.get(h6_lord, 1)
        h6_house = self._get_house_num(h6_pos, self.udayam)
        pt_stress = f"{num:02d}. Service/Competition Lord (6L) {h6_lord} is in {h6_house}H. "
        if h6_house in [6, 8, 12]:
            pt_stress += "Competition is weakened — the native has an advantage over rivals and obstacles."
        elif h6_house in [1, 7, 10]:
            pt_stress += "Competition is strong — workplace rivals or hidden enemies are active. Stay alert and maintain professional conduct."
        else:
            pt_stress += "Moderate competitive pressure exists. The native needs to stay focused and avoid unnecessary workplace conflicts."
        pts.append(pt_stress)
        num += 1

        # Transition Pulse — with house distance meaning
        udayam_lord = self.house_lords[self.udayam]
        distance = self._get_house_num(h10_pos, self.udayam)
        dist_meaning = self._get_house_distance_meaning(distance)
        pts.append(f"{num:02d}. Transition Pulse: {udayam_lord} (Udayam Lord) and 10L ({h10_lord}) are {distance} houses apart — they are {dist_meaning}")
        num += 1

        # Economic Gains
        h11_rasi = (self.udayam + 10) % 12 or 12
        h11_lord = self.house_lords[h11_rasi]
        h11_pos = self.positions.get(h11_lord, 1)
        h11_house = self._get_house_num(h11_pos, self.udayam)
        pt_gains = f"{num:02d}. Economic Gains: 11L ({h11_lord}) is placed in {h11_house}H. "
        if h11_house in [1, 2, 5, 9, 11]:
            pt_gains += "Financial gains from the career change are strongly indicated. The new opportunity will bring better compensation."
        elif h11_house in [6, 8, 12]:
            pt_gains += "Initial financial challenges may arise during the transition, but gains will stabilize after the first few months."
        else:
            pt_gains += "Financial outcomes are moderate. The native should negotiate carefully and not rush into accepting the first offer."
        pts.append(pt_gains)
        num += 1

        # Transit-based career insights
        sat_t = self.transits.get("Saturn", {})
        mer_t = self.transits.get("Mercury", {})
        if sat_t:
            sat_detail_t = f"{num:02d}. TRANSIT SATURN ({sat_t.get('rasi', '')} @ {sat_t.get('degree', '')}, {sat_t.get('nakshatra', '')}, {sat_t.get('status', '')}): "
            if "Friend" in str(sat_t.get('status', '')) or "Own" in str(sat_t.get('status', '')):
                sat_detail_t += "Saturn's transit position supports structured career growth. Discipline and long-term planning will pay off."
            else:
                sat_detail_t += "Saturn's current transit creates work pressure. Avoid shortcuts — sustained effort and patience are essential for career outcomes."
            sat_detail_t += f" Fruition: {sat_t.get('fruition', 'N/A')}."
            pts.append(sat_detail_t)
            num += 1

        # Natal-specific career points (Mode 2 — Birth Data)
        if self.natal and self.natal.get("Lagna"):
            n_lagna = self.natal.get("Lagna", "")
            n_nak = self.natal.get("Nakshatra", "")
            n_states = self.natal.get("PlanetaryStates", {})
            n_sat = n_states.get("Saturn", "Normal")
            n_sun = n_states.get("Sun", "Normal")
            lagna_rasi = self.natal.get("LagnaRasi", 0)
            lagna_house = self._get_house_num(lagna_rasi, self.udayam) if lagna_rasi else 0
            alignment = "trine (excellent)" if lagna_house in [1,5,9] else "kendram (strong)" if lagna_house in [4,7,10] else "dusthana (challenging)" if lagna_house in [6,8,12] else "neutral"
            pts.append(f"{num:02d}. BIRTH CHART OVERLAY: Native Lagna {n_lagna} ({lagna_house}H from Prasna Udayam) — {alignment} alignment. Birth Nakshatra: {n_nak}.")
            num += 1
            pts.append(f"{num:02d}. NATAL SATURN ({n_sat}): {'Birth chart supports disciplined career growth — native has inherent work ethic.' if 'Friend' in str(n_sat) else 'Birth Saturn indicates delayed career rewards — persistence is the karmic lesson for this native.'}")
            num += 1

        return pts, num

    def _generate_marriage_points(self, num: int):
        """Generates 6 marriage-specific synthesis points with full indications."""
        pts = []
        h7_rasi = (self.udayam + 6) % 12 or 12
        h7_lord = self.house_lords[h7_rasi]
        h7_pos = self.positions.get(h7_lord, 1)
        h7_house = self._get_house_num(h7_pos, self.udayam)
        
        # Point: 7L Placement — with full indication
        meaning = self._get_house_placement_meaning(h7_house, h7_lord, "marriage")
        pts.append(f"{num:02d}. Marriage Lord (7L) {h7_lord} is placed in {h7_house}H. {meaning}")
        num += 1

        # 7L alignment check
        if h7_pos == self.udayam:
            pts.append(f"{num:02d}. 7L ({h7_lord}) is aligned with Udayam — the proposal/alliance is approaching quickly. The other party is actively interested.")
        elif h7_pos == self.kavippu:
            lift_date = self._get_kavippu_lift_date_raw()
            lift_time = f"approximately around {lift_date.strftime('%B %d, %Y')}"
            pts.append(f"{num:02d}. 7L ({h7_lord}) is overshadowed by {self.KAVIPPU_EXPLANATION}. A major hidden hurdle or delayed decision from the other side is indicated. This usually eases {lift_time}. Remedy: Offer white flowers at a Devi temple on Fridays.")
        else:
            pts.append(f"{num:02d}. 7L ({h7_lord}) and Udayam are {h7_house} houses apart — the alliance energy is {'strong and flowing' if h7_house in [1, 5, 9, 11] else 'present but requires patient nurturing'}.")
        num += 1
        
        # Family House
        h2_rasi = (self.udayam + 1) % 12 or 12
        h2_lord = self.house_lords[h2_rasi]
        h2_house = self._get_house_num(self.positions.get(h2_lord, 1), self.udayam)
        pt_fam = f"{num:02d}. Family Lord (2L) {h2_lord} in {h2_house}H. "
        if h2_house in [1, 4, 7, 10]:
            pt_fam += "Strong family involvement and support for the alliance. Elders will play a positive role."
        else:
            pt_fam += "Family dynamics may need careful handling. Communication with elders should be gentle and respectful."
        pts.append(pt_fam)
        num += 1

        # Venus (Karaka)
        ven_pos = self.positions.get("Venus", 1)
        ven_house = self._get_house_num(ven_pos, self.udayam)
        pt_ven = f"{num:02d}. Venus (Natural Marriage Karaka) at {ven_house}H ({self._get_sign_name(ven_pos)}). "
        if ven_house in [1, 2, 4, 7, 11]:
            pt_ven += "Venus placement strongly supports love, emotional bonding, and a harmonious alliance."
        else:
            pt_ven += "Venus needs strengthening. Recite 'Om Shukraya Namaha' 108 times daily for relationship blessings."
        pts.append(pt_ven)
        num += 1

        # Domestic Harmony
        h4_rasi = (self.udayam + 3) % 12 or 12
        h4_lord = self.house_lords[h4_rasi]
        h4_house = self._get_house_num(self.positions.get(h4_lord, 1), self.udayam)
        pts.append(f"{num:02d}. Domestic Harmony: 4L ({h4_lord}) in {h4_house}H indicates {'a peaceful and comfortable married life' if h4_house in [1, 4, 7, 9, 11] else 'some adjustment period needed in the early phase of the alliance'}.")
        num += 1

        # Mutual Compatibility
        udm_lord = self.house_lords[self.udayam]
        udm_pos = self.positions.get(udm_lord, 1)
        dist = self._get_house_num(h7_pos, udm_pos)
        dist_meaning = self._get_house_distance_meaning(dist)
        pts.append(f"{num:02d}. Mutual Compatibility: {udm_lord} (Udayam Lord) and 7L ({h7_lord}) are {dist} houses apart — they are {dist_meaning}")
        num += 1

        # Transit-based marriage insights
        ven_t = self.transits.get("Venus", {})
        if ven_t:
            ven_detail_t = f"{num:02d}. TRANSIT VENUS ({ven_t.get('rasi', '')} @ {ven_t.get('degree', '')}, {ven_t.get('nakshatra', '')}, {ven_t.get('status', '')}): "
            if "Friend" in str(ven_t.get('status', '')) or "Own" in str(ven_t.get('status', '')):
                ven_detail_t += "Venus transit supports relationship harmony and alliance success. Auspicious timing for proposals."
            else:
                ven_detail_t += "Venus transit requires careful nurturing of relationships. Avoid ego clashes and maintain patience."
            ven_detail_t += f" Fruition: {ven_t.get('fruition', 'N/A')}."
            pts.append(ven_detail_t)
            num += 1

        # Natal-specific marriage points (Mode 2)
        if self.natal and self.natal.get("Lagna"):
            n_lagna = self.natal.get("Lagna", "")
            n_nak = self.natal.get("Nakshatra", "")
            n_states = self.natal.get("PlanetaryStates", {})
            n_ven = n_states.get("Venus", "Normal")
            lagna_rasi = self.natal.get("LagnaRasi", 0)
            lagna_house = self._get_house_num(lagna_rasi, self.udayam) if lagna_rasi else 0
            alignment = "trine (excellent)" if lagna_house in [1,5,9] else "kendram (strong)" if lagna_house in [4,7,10] else "dusthana (challenging)" if lagna_house in [6,8,12] else "neutral"
            pts.append(f"{num:02d}. BIRTH CHART OVERLAY: Native Lagna {n_lagna} ({lagna_house}H from Prasna Udayam) — {alignment} alignment. Birth Nakshatra: {n_nak}.")
            num += 1
            pts.append(f"{num:02d}. NATAL VENUS ({n_ven}): {'Birth chart strongly supports relationship harmony — native has inherent compatibility energy.' if 'Friend' in str(n_ven) or 'Direct' in str(n_ven) else 'Birth Venus requires extra nurturing for relationship success — perform Venus remedies on Fridays.'}")
            num += 1

        return pts, num

    def _generate_health_points(self, num: int):
        """Generates 6 health-specific synthesis points with anatomical focus."""
        pts = []
        
        # 1. Affected Body Part (Udayam/Arudam)
        affected_parts = self.RASI_BODY_PARTS.get(self.arudam, "General constitution")
        pts.append(f"{num:02d}. PRIMARY DIAGNOSIS: Arudam ({self._get_sign_name(self.arudam)}) indicates the core area of concern is related to the **{affected_parts}**. This matches the seat of the current health complaint.")
        num += 1

        # 2. Nature of Affliction (Kavippu)
        kav_parts = self.RASI_BODY_PARTS.get(self.kavippu, "vitality")
        pts.append(f"{num:02d}. ENERGY BLOCK: Kavippu is obstructing the **{kav_parts}**. This 'block' indicates where the healing energy is temporarily stagnant, causing specific discomfort or functional delays.")
        num += 1

        # 3. Disease Intensity (6th Lord)
        h6_rasi = (self.udayam + 5) % 12 or 12
        h6_lord = self.house_lords[h6_rasi]
        h6_pos = self.positions.get(h6_lord, 1)
        h6_house = self._get_house_num(h6_pos, self.udayam)
        h6_sig = self.PLANET_HEALTH_SIGNIFICANCE.get(h6_lord, "general health")
        
        pt3 = f"{num:02d}. CLINICAL INDICATOR: The 6th Lord ({h6_lord}) is in {h6_house}H. "
        if h6_house in [6, 8, 12]:
            pt3 += f"This suggests a more deep-seated or stubborn condition related to {h6_sig}. Professional medical attention and strict adherence to protocol are essential."
        else:
            pt3 += f"This indicates a manageable condition. The influence of {h6_sig} suggests inflammation or temporary burnout that will respond well to rest and generic treatment."
        pts.append(pt3)
        num += 1

        # 4. Planetary Affliction (Ruling Planet)
        rp_sig = self.PLANET_HEALTH_SIGNIFICANCE.get(self.ruling_planet, "vitality")
        pts.append(f"{num:02d}. SYSTEMIC FOCUS: The Ruling Planet {self.ruling_planet} points to the **{rp_sig}** as the main system needing revitalization for full recovery.")
        num += 1

        # 5. Recovery Potential (Benefics)
        jup_pos = self.positions.get("Jupiter", 0)
        ven_pos = self.positions.get("Venus", 0)
        j_h = self._get_house_num(jup_pos, self.udayam) if jup_pos else 0
        v_h = self._get_house_num(ven_pos, self.udayam) if ven_pos else 0
        
        pt5 = f"{num:02d}. RECOVERY POTENTIAL: "
        if j_h in [1, 5, 9, 11] or v_h in [1, 5, 9, 11]:
            pt5 += "Benefic planets are strongly placed. This indicates a high 'Ojas' (vitality) and a smooth, faster recovery once the current planetary block eases."
        else:
            pt5 += "Recovery may be gradual. The absence of direct benefic support suggests traditional therapies and patience will be required to build back the immune system."
        pts.append(pt5)
        num += 1

        # 6. Outlook Summary
        kav_lift, next_sign_name = self._get_kavippu_lift_date_raw()
        pts.append(f"{num:02d}. TIMELINE EXPECTATION: Significant relief and 'lift' in symptoms are expected after **{kav_lift.strftime('%B %d, %Y')}**, when the planetary block moves away from the affected body region and shifts into {next_sign_name}.")
        num += 1

        return pts, num, {"diagnosis": affected_parts, "block": kav_parts}

    def _generate_general_points(self, num: int):
        """Generates 6 general synthesis points with full indications."""
        pts = []
        
        udm_lord = self.house_lords[self.udayam]
        udm_pos = self.positions.get(udm_lord, 1)
        udm_house = self._get_house_num(udm_pos, self.udayam)
        pts.append(f"{num:02d}. Udayam Lord ({udm_lord}) is in {udm_house}H — {'strong self-driven energy for the query' if udm_house in [1, 5, 9, 11] else 'the native needs to put extra effort to manifest the desired result'}.")
        num += 1

        aru_lord = self.house_lords[self.arudam]
        aru_pos = self.positions.get(aru_lord, 1)
        aru_house = self._get_house_num(aru_pos, self.udayam)
        pts.append(f"{num:02d}. Arudam Lord ({aru_lord}) is in {aru_house}H — {'the desire is well-supported and likely to manifest' if aru_house in [1, 5, 9, 11] else 'the desire needs time and effort to materialize'}.")
        num += 1

        # House of Gains
        h11_rasi = (self.udayam + 10) % 12 or 12
        h11_lord = self.house_lords[h11_rasi]
        h11_house = self._get_house_num(self.positions.get(h11_lord, 1), self.udayam)
        pts.append(f"{num:02d}. House of Gains: 11L ({h11_lord}) in {h11_house}H — {'gains and wish fulfillment are actively supported' if h11_house in [1, 2, 5, 9, 11] else 'gains will come but may require patience and sustained effort'}.")
        num += 1

        # House of Loss
        h12_rasi = (self.udayam + 11) % 12 or 12
        h12_lord = self.house_lords[h12_rasi]
        h12_house = self._get_house_num(self.positions.get(h12_lord, 1), self.udayam)
        pts.append(f"{num:02d}. House of Expenses: 12L ({h12_lord}) in {h12_house}H — {'expenses are controlled, no major financial drain' if h12_house in [3, 6, 11, 12] else 'watch for unnecessary expenses or energy drain during this period'}.")
        num += 1

        # Planetary relationship
        pts.append(f"{num:02d}. UDM-ARU Gap: The distance between Udayam ({self._get_sign_name(self.udayam)}) and Arudam ({self._get_sign_name(self.arudam)}) is {self._get_house_num(self.arudam, self.udayam)} houses — {'desire and reality are closely aligned' if self._get_house_num(self.arudam, self.udayam) in [1, 5, 9] else 'there is a gap between desire and current reality that needs bridging through effort and remedies'}.")
        num += 1

        # Malefics in Kendras
        kendras = [1, 4, 7, 10]
        malefics = ["Mars", "Saturn", "Rahu", "Ketu"]
        mal_count = sum(1 for m in malefics if self._get_house_num(self.positions.get(m, 0), self.udayam) in kendras)
        pts.append(f"{num:02d}. Obstacle Check: {mal_count} malefic(s) in Kendra houses — {'path has significant obstacles requiring dedicated remedies' if mal_count >= 2 else 'manageable level of obstacles, steady effort will suffice' if mal_count == 1 else 'path is relatively clear of major obstacles'}.")
        num += 1

        # Transit-based general insights
        rp_t = self.transits.get(self.ruling_planet, {})
        if rp_t:
            rp_detail = f"{num:02d}. TRANSIT {self.ruling_planet.upper()} ({rp_t.get('rasi', '')} @ {rp_t.get('degree', '')}, {rp_t.get('nakshatra', '')}, {rp_t.get('status', '')}): "
            rp_detail += f"The ruling planet's current transit determines the timing and quality of the outcome. Fruition: {rp_t.get('fruition', 'N/A')}."
            pts.append(rp_detail)
            num += 1

        # Natal-specific general points (Mode 2)
        if self.natal and self.natal.get("Lagna"):
            n_lagna = self.natal.get("Lagna", "")
            n_nak = self.natal.get("Nakshatra", "")
            n_states = self.natal.get("PlanetaryStates", {})
            lagna_rasi = self.natal.get("LagnaRasi", 0)
            lagna_house = self._get_house_num(lagna_rasi, self.udayam) if lagna_rasi else 0
            alignment = "trine (excellent)" if lagna_house in [1,5,9] else "kendram (strong)" if lagna_house in [4,7,10] else "dusthana (challenging)" if lagna_house in [6,8,12] else "neutral"
            pts.append(f"{num:02d}. BIRTH CHART OVERLAY: Native Lagna {n_lagna} ({lagna_house}H from Prasna Udayam) — {alignment} alignment. Birth Nakshatra: {n_nak}.")
            num += 1
            rp_n_state = n_states.get(self.ruling_planet, "")
            if rp_n_state:
                pts.append(f"{num:02d}. NATAL {self.ruling_planet.upper()} ({rp_n_state}): {'Birth chart supports the ruling planet energy — native is aligned with the Prasna outcome.' if 'Friend' in str(rp_n_state) else 'Birth chart shows friction with ruling planet energy — dedicated remedies for ' + self.ruling_planet + ' will bridge the gap.'}")
                num += 1

        return pts, num

        return pts, num

    def _calculate_cricket_prediction(self):
        """Calculates specific cricket predictions based on the worksheet."""
        res = {"team_a": "Team A", "team_b": "Team B"}
        
        # Determine Teams from query
        text = self.query_text.lower()
        import re
        
        # 1. Try to find explicit "Team A" / "Team B" format
        match_a = re.search(r'team a\s*[:\-]?\s*([^\n]+)', text, flags=re.I)
        match_b = re.search(r'team b\s*[:\-]?\s*([^\n]+)', text, flags=re.I)
        
        if match_a and match_b:
            res["team_a"] = match_a.group(1).strip()
            res["team_b"] = match_b.group(1).strip()
        else:
            # 2. Try to find explicit "between X and Y" pattern
            match_between = re.search(r'between\s+(.+?)\s+(?:and|vs\.?)\s+(.+)', text, flags=re.I)
            if match_between:
                res["team_a"] = match_between.group(1).strip()
                res["team_b"] = match_between.group(2).strip()
            else:
                teams = re.findall(r'([a-z\s]+)\svs\.?\s([a-z\s]+)', text)
                if teams:
                    res["team_a"] = teams[0][0].strip()
                    res["team_b"] = teams[0][1].strip()
                else:
                    # Fallback for simpler queries
                    names = re.split(r'\svs\.?\s|\sand\s', text)
                    if len(names) >= 2:
                        res["team_a"] = names[0].strip()
                        res["team_b"] = names[1].strip()

        # Cleanup team names from trailing/leading query noise
        for key in ["team_a", "team_b"]:
            cleaned = res[key]
            
            # Split off trailing conversational follow-up questions
            cleaned = re.split(r'\s(and)?\s*(who|will|what|where|how|bat|score|toss|win)\b', cleaned, flags=re.I)[0].strip()
            
            # Strip leading words like "Who will win the match between"
            prev = ""
            while cleaned != prev:
                prev = cleaned
                cleaned = re.sub(r'^(?:the|who|will|be|winning|win|match|between|is|playing|what|team|which|todays|today\'s|today)\b\s*', '', cleaned, flags=re.I).strip()
            
            # Split off trailing context like "cricket match in Chennai"
            cleaned = re.split(r'\s(cricket|match|in|at|played|prediction|vs|today|tomorrow)\b', cleaned, flags=re.I)[0].strip()
            
            res[key] = cleaned.title()

        # 1. Toss Prediction (Lagna vs 7th Lord)
        l1 = self.house_lords[self.udayam]
        h7_rasi = (self.udayam + 6) % 12 or 12
        l7 = self.house_lords[h7_rasi]
        
        l1_strength = self._get_planet_strength_score(l1)
        l7_strength = self._get_planet_strength_score(l7)
        
        # Apply additional competition factors (3rd, 6th, 11th houses)
        h3 = (self.udayam + 2) % 12 or 12
        h6 = (self.udayam + 5) % 12 or 12
        h11 = (self.udayam + 10) % 12 or 12
        
        b_h3 = (h7_rasi + 2) % 12 or 12
        b_h6 = (h7_rasi + 5) % 12 or 12
        b_h11 = (h7_rasi + 10) % 12 or 12
        
        a_bonus = sum([self._get_planet_strength_score(self.house_lords[r]) for r in [h3, h6, h11]]) / 3.0
        b_bonus = sum([self._get_planet_strength_score(self.house_lords[r]) for r in [b_h3, b_h6, b_h11]]) / 3.0
        
        l1_strength += a_bonus
        l7_strength += b_bonus
        
        # Jamakkol Syllable Check (Time-based vibration proxy using Arudam and RP)
        # Syllables favoring Lagna (1st half of zodiac from Udayam) vs 7th
        aru_h = self._get_house_num(self.arudam, self.udayam)
        rp_pos = self.positions.get(self.ruling_planet, 1)
        rp_h = self._get_house_num(rp_pos, self.udayam)
        
        syllable_favors_lagna = aru_h in [1, 2, 3, 4, 5, 11] or rp_h in [1, 2, 3]
        syllable_side = res["team_a"] if syllable_favors_lagna else res["team_b"]
        
        # Decide Toss Winner based on structured logic
        strength_diff = l1_strength - l7_strength
        if self.jam.get("toss_winner"):
            res["toss_winner"] = self.jam.get("toss_winner")
            res["toss_reason"] = "&bull; Confirmed pre-match condition."
        else:
            if strength_diff >= 3:
                res["toss_winner"] = res["team_a"]
                res["toss_reason"] = f"&bull; Lagna Lord ({l1}) strongly dominates 7th Lord."
            elif strength_diff <= -3:
                res["toss_winner"] = res["team_b"]
                res["toss_reason"] = f"&bull; 7th Lord ({l7}) strongly dominates Lagna Lord."
            else:
                # Strengths are within override range
                if syllable_favors_lagna:
                    res["toss_winner"] = res["team_a"]
                    reason = "&bull; Jamakkol syllable favors Lagna side."
                    if strength_diff < 0:
                        reason = f"&bull; Jamakkol syllable favors Lagna ({res['team_a']}) despite weaker lord, acting as a powerful override."
                    res["toss_reason"] = reason
                else:
                    res["toss_winner"] = res["team_b"]
                    reason = "&bull; Jamakkol syllable favors 7th side."
                    if strength_diff > 0:
                        reason = f"&bull; Jamakkol syllable favors 7th ({res['team_b']}) despite weaker lord, acting as a powerful override."
                    res["toss_reason"] = reason

        # 2. Score Prediction via Graha Kirana (Planetary Rays)
        # Rays Adjustments mapped from User Table
        ray_adjustments = {
            "Jupiter": (30, 40, "Jupiter Rays (Guru kirana): Expansion, partnerships, accumulation"),
            "Venus": (20, 30, "Venus Rays (Shukra kirana): Smooth flow, attractive batting, boundaries"),
            "Mercury": (15, 25, "Mercury Rays (Budha kirana): Quick singles, sharp calculation"),
            "Saturn": (-30, -20, "Saturn Rays (Shani kirana): Restriction, slow pace, dot balls"),
            "Mars": (-25, -15, "Mars Rays (Kuja kirana): Aggression but instability, wickets fall quickly"),
            "Rahu": (-35, -25, "Rahu/Ketu Rays: Confusion, misjudgment, sudden collapses"),
            "Ketu": (-35, -25, "Rahu/Ketu Rays: Confusion, misjudgment, sudden collapses"),
            "Snake": (-35, -25, "Rahu/Ketu Rays: Confusion, misjudgment, sudden collapses"),
            "Sun": (10, 20, "Sun Rays: Steady authority, solid partnerships"),
            "Moon": (10, 20, "Moon Rays: Rhythm and momentum")
        }
        
        def get_score_range(lord, is_lagna, strength, h2_mal, h10_ben, moon_aff):
            side = "Lagna side" if is_lagna else "7th house side"
            reason_parts = []
            reason_noray_parts = []
            
            # 1. Baseline Score Range
            if strength >= 7:
                base_min = 150
                txt = f"Strong {side} base (score: {strength:.1f}) sets baseline to 150-170."
            elif strength <= 4:
                base_min = 120
                txt = f"Weak {side} base (score: {strength:.1f}) limits baseline to 120-140."
            else:
                base_min = 140
                txt = f"Moderate {side} base (score: {strength:.1f}) sets baseline to 140-160."
                
            base_max = base_min + 20
            reason_parts.append(txt)
            reason_noray_parts.append(txt)
            
            # 2. House Modifier
            if h2_mal: 
                base_min -= 15; base_max -= 15
                txt = "-15 runs (Malefic on 2nd H restrictions)."
                reason_parts.append(txt)
                reason_noray_parts.append(txt)
            if h10_ben: 
                base_min += 20; base_max += 20
                txt = "+20 runs (Benefic on 10th H expansion)."
                reason_parts.append(txt)
                reason_noray_parts.append(txt)
            
            # Save the pre-rays score bounds
            base_noray_min = base_min
            base_noray_max = base_max

            # 3. Planetary Rays Adjustment (Dominant Lord)
            if lord in ray_adjustments:
                ray_min, ray_max, ray_interp = ray_adjustments[lord]
                # Average out the ray adj for simplified addition
                ray_mid = (ray_min + ray_max) // 2
                base_min += ray_mid; base_max += ray_mid
                sign = "+" if ray_mid > 0 else ""
                reason_parts.append(f"{sign}{ray_mid} runs from {ray_interp}.")
            
            # 4. Moon Rays (Rhythm)
            if moon_aff: 
                base_min -= 25; base_max -= 25
                reason_parts.append("-25 runs from Afflicted Moon Rays (Chandra kirana): Broken rhythm, sudden collapses.")
            else: 
                base_min += 15; base_max += 15
                reason_parts.append("+15 runs from Strong Moon Rays (Chandra kirana): Rhythm, stability, partnerships hold.")

            # Formulate final boundary for BOTH scenarios
            
            # --- Scenario 1: WITHOUT RAYS ---
            noray_min = max(70, int(base_noray_min))
            noray_max = max(noray_min + 20, int(base_noray_max))
            reason_noray = "&bull; " + "<br/>&bull; ".join(reason_noray_parts)
            range_str_noray = f"{noray_min}-{noray_max}"
            
            # --- Scenario 2: WITH RAYS ---
            base_min = max(70, int(base_min))
            base_max = max(base_min + 20, int(base_max))
            reason = "&bull; " + "<br/>&bull; ".join(reason_parts)
            range_str = f"{base_min}-{base_max}"
            
            if base_min <= 110: interp = "Collapse/Restricted"
            elif base_min <= 130: interp = "Below Average/Low"
            elif base_min <= 150: interp = "Average/Par"
            elif base_min <= 170: interp = "Competitive/Above average"
            elif base_min <= 190: interp = "Solid/High"
            else: interp = "Huge/Explosive"
            
            return range_str, interp, reason, range_str_noray, reason_noray

        # Check House 2 (Accumulation)
        h2_rasi = (self.udayam + 1) % 12 or 12
        h2_malefic = self.positions.get("Saturn") == h2_rasi or self.positions.get("Mars") == h2_rasi or self.positions.get("Snake") == h2_rasi
        
        # Check House 10 (Achievement)
        h10_rasi = (self.udayam + 9) % 12 or 12
        h10_benefic = self.positions.get("Jupiter") == h10_rasi or self.positions.get("Venus") == h10_rasi or self.positions.get("Mercury") == h10_rasi

        moon_pos = self.positions.get("Moon", 1)
        
        def is_moon_afflicted(base_rasi):
            m_h = self._get_house_num(moon_pos, base_rasi)
            return m_h in [6, 8, 12] or self.positions.get("Snake") == moon_pos

        a_moon_aff = is_moon_afflicted(self.udayam)
        res["team_a_score"], res["team_a_interp"], res["team_a_score_reason"], res["team_a_score_noray"], res["team_a_score_reason_noray"] = get_score_range(l1, True, l1_strength, h2_malefic, h10_benefic, a_moon_aff)
        
        # Team B (7th side) - Use 7th as temporary Lagna for its own 2nd/10th
        h7_2 = (h7_rasi + 1) % 12 or 12
        h7_10 = (h7_rasi + 9) % 12 or 12
        b_h2_mal = self.positions.get("Saturn") == h7_2 or self.positions.get("Mars") == h7_2 or self.positions.get("Snake") == h7_2
        b_h10_ben = self.positions.get("Jupiter") == h7_10 or self.positions.get("Venus") == h7_10 or self.positions.get("Mercury") == h7_10
        b_moon_aff = is_moon_afflicted(h7_rasi)
        
        res["team_b_score"], res["team_b_interp"], res["team_b_score_reason"], res["team_b_score_noray"], res["team_b_score_reason_noray"] = get_score_range(l7, False, l7_strength, b_h2_mal, b_h10_ben, b_moon_aff)

        # 3. Predict Bat First
        if self.jam.get("toss_decision"):
            decision = self.jam.get("toss_decision").lower()
            if decision == "bat":
                res["bat_first"] = res["toss_winner"]
                res["bat_first_reason"] = "&bull; Confirmed pre-match condition (Elected to Bat)."
            elif decision in ["bowl", "field"]:
                res["bat_first"] = res["team_b"] if res["toss_winner"] == res["team_a"] else res["team_a"]
                res["bat_first_reason"] = "&bull; Confirmed pre-match condition (Elected to Bowl)."
        else:
            # If toss winner's 10H (Achievement/Batting) is stronger than their 4H (Comfort/Fielding), they bat.
            # Simplification: If 10H has benefic or is stronger, they bat. Otherwise bowl.
            toss_winner_is_a = res["toss_winner"] == res["team_a"]
            toss_10h_ben = h10_benefic if toss_winner_is_a else b_h10_ben
            # If it's a T20/ODI they mostly prefer to bat or bowl depending on dew, but astrologically:
            if toss_10h_ben or (l1_strength > 5 if toss_winner_is_a else l7_strength > 5):
                res["bat_first"] = res["toss_winner"]
                res["bat_first_reason"] = "&bull; Strong planetary inclination for taking initiative (good 10th house strength) encourages batting first."
            else:
                res["bat_first"] = res["team_b"] if toss_winner_is_a else res["team_a"]
                res["bat_first_reason"] = "&bull; Weaker 10th house or strong 4th house (comfort/defense) encourages fielding first."

        res["bat_second"] = res["team_b"] if res["bat_first"] == res["team_a"] else res["team_a"]

        # Assign scores to batting order
        # Calculate raw scores first
        if res["bat_first"] == res["team_a"]:
            bf_score_raw, bf_interp, bf_reason = res["team_a_score"], res["team_a_interp"], res["team_a_score_reason"]
            bs_score_raw, bs_interp, bs_reason = res["team_b_score"], res["team_b_interp"], res["team_b_score_reason"]
            bf_noray, bf_noray_r = res["team_a_score_noray"], res["team_a_score_reason_noray"]
            bs_noray, bs_noray_r = res["team_b_score_noray"], res["team_b_score_reason_noray"]
            a_is_bf = True
        else:
            bf_score_raw, bf_interp, bf_reason = res["team_b_score"], res["team_b_interp"], res["team_b_score_reason"]
            bs_score_raw, bs_interp, bs_reason = res["team_a_score"], res["team_a_interp"], res["team_a_score_reason"]
            bf_noray, bf_noray_r = res["team_b_score_noray"], res["team_b_score_reason_noray"]
            bs_noray, bs_noray_r = res["team_a_score_noray"], res["team_a_score_reason_noray"]
            a_is_bf = False

        res["bat_first_score"] = bf_score_raw
        res["bat_first_score_reason"] = bf_reason
        res["bat_first_score_noray"] = bf_noray
        res["bat_first_score_reason_noray"] = bf_noray_r

        # Cap second innings score based on first innings target
        bf_min, bf_max = map(int, bf_score_raw.split('-'))
        bs_min, bs_max = map(int, bs_score_raw.split('-'))
        target = bf_max + 1
        
        if bs_max >= target:
            bs_max = target + 5
            bs_min = target - 10
            bs_reason += "<br/>&bull; Score naturally capped as chase target is achieved comfortably."
        
        # Similar logic for NO-RAYS
        bf_n_min, bf_n_max = map(int, bf_noray.split('-'))
        bs_n_min, bs_n_max = map(int, bs_noray.split('-'))
        target_n = bf_n_max + 1
        if bs_n_max >= target_n:
            bs_n_max = target_n + 5
            bs_n_min = target_n - 10
            bs_noray_r += "<br/>&bull; Score naturally capped as chase target is achieved comfortably."

        res["bat_second_score"] = f"{bs_min}-{bs_max}"
        res["bat_second_score_reason"] = bs_reason
        res["bat_second_score_noray"] = f"{bs_n_min}-{bs_n_max}"
        res["bat_second_score_reason_noray"] = bs_noray_r

        # Reflect this back into team_a/team_b
        if a_is_bf:
            res["team_a_score"] = res["bat_first_score"]
            res["team_b_score"] = res["bat_second_score"]
            res["team_a_score_reason"] = res["bat_first_score_reason"]
            res["team_b_score_reason"] = res["bat_second_score_reason"]
        else:
            res["team_b_score"] = res["bat_first_score"]
            res["team_a_score"] = res["bat_second_score"]
            res["team_b_score_reason"] = res["bat_first_score_reason"]
            res["team_a_score_reason"] = res["bat_second_score_reason"]

        # 4. Outcome & Margin
        a_mid = sum(int(x) for x in res["team_a_score"].split('-')) / 2 if '-' in res["team_a_score"] else 200
        b_mid = sum(int(x) for x in res["team_b_score"].split('-')) / 2 if '-' in res["team_b_score"] else 200
        
        diff = a_mid - b_mid
        reason = ""
        if abs(diff) < 5:
            # Tie breaker
            if l1_strength > l7_strength:
                res["predicted_winner"] = res["team_a"]
                reason = f"&bull; Scores are effectively tied, but {res['team_a']} holds a slight planetary edge ({l1_strength:.1f} vs {l7_strength:.1f})."
            elif l7_strength > l1_strength:
                res["predicted_winner"] = res["team_b"]
                reason = f"&bull; Scores are effectively tied, but {res['team_b']} holds a slight planetary edge ({l7_strength:.1f} vs {l1_strength:.1f})."
            else:
                res["predicted_winner"] = res["toss_winner"]
                reason = "&bull; Scores and strengths are matched; the outcome aligns with the toss winner's minor advantage."
            res["predicted_margin"] = "Tense Finish / Edge (Very narrow margin / last over finish)"
        elif diff > 0:
            res["predicted_winner"] = res["team_a"]
            res["predicted_margin"] = "By a margin of ~30-40 runs" if diff >= 30 else "Moderate/Comfortable victory" if diff >= 20 else "Narrow victory"
            reason = f"&bull; {res['team_a']} has significantly higher predicted scoring momentum."
        else:
            res["predicted_winner"] = res["team_b"]
            res["predicted_margin"] = "By a margin of ~30-40 runs" if abs(diff) >= 30 else "Moderate/Comfortable victory" if abs(diff) >= 20 else "Narrow victory"
            reason = f"&bull; {res['team_b']} has significantly higher predicted scoring momentum."
        
        # Override winner if one side has significantly higher lord strength
        if l1_strength >= l7_strength + 3:
            res["predicted_winner"] = res["team_a"]
            res["predicted_margin"] = "Strong planetary support ensures victory."
            reason = f"&bull; {res['team_a']} receives overwhelmingly strong overall planetary support ({l1_strength:.1f} vs {l7_strength:.1f}), overriding the scoring variance."
        elif l7_strength >= l1_strength + 3:
            res["predicted_winner"] = res["team_b"]
            res["predicted_margin"] = "Strong planetary support ensures victory."
            reason = f"&bull; {res['team_b']} receives overwhelmingly strong overall planetary support ({l7_strength:.1f} vs {l1_strength:.1f}), overriding the scoring variance."
        
        res["outcome_reason"] = reason
        return res

    def _get_planet_strength_score(self, planet):
        """Utility for quantitative comparison (1-10 scale)."""
        pos = self.positions.get(planet, 1)
        house = self._get_house_num(pos, self.udayam)
        score = 5 # Neutral base
        if house in [1, 4, 7, 10]: score += 2 # Kendra
        if house in [5, 9]: score += 2 # Trikona
        if house in [6, 8, 12]: score -= 3 # Dusthana
        
        # Status from transits
        t_data = self.transits.get(planet, {})
        status = t_data.get("status", "")
        if "Exalted" in status or "Own" in status: score += 3
        if "Friendly" in status: score += 1
        if "Debilitated" in status or "Enemy" in status: score -= 2
        
        return max(1, min(10, score))

    def _generate_competition_points(self, num: int):
        """Generates 6 competition-specific synthesis points for sports/elections."""
        pts = []
        
        # 6th House: Opponents and Competition
        h6_rasi = (self.udayam + 5) % 12 or 12
        h6_lord = self.house_lords[h6_rasi]
        h6_pos = self.positions.get(h6_lord, 1)
        h6_house = self._get_house_num(h6_pos, self.udayam)
        pts.append(f"{num:02d}. Competition Lord (6L) {h6_lord} is in {h6_house}H. {'The opposition/rival side is in a weakened position.' if h6_house in [6, 8, 12] else 'The opposition side is strong and determined.' if h6_house in [1, 7, 10] else 'Normal competitive pressure is indicated.'}")
        num += 1

        # 11th House: Victory and Success
        h11_rasi = (self.udayam + 10) % 12 or 12
        h11_lord = self.house_lords[h11_rasi]
        h11_house = self._get_house_num(self.positions.get(h11_lord, 1), self.udayam)
        pts.append(f"{num:02d}. Victory Lord (11L) {h11_lord} in {h11_house}H. {'A high probability of victory and goal fulfillment is indicated.' if h11_house in [1, 5, 9, 11] else 'Success will require significant effort and negotiation.' if h11_house in [2, 10] else 'Outcome depends on external factors and timing.'}")
        num += 1

        # 3rd House: Valour and Effort
        h3_rasi = (self.udayam + 2) % 12 or 12
        h3_lord = self.house_lords[h3_rasi]
        h3_house = self._get_house_num(self.positions.get(h3_lord, 1), self.udayam)
        pts.append(f"{num:02d}. Effort/Valour Lord (3L) {h3_lord} in {h3_house}H. {'The native/team will show great courage and strategic brilliance.' if h3_house in [1, 3, 11] else 'Persistence is key; success comes through steady execution.'}")
        num += 1

        # Mars (Natural significator for Competition/Sports)
        mars_pos = self.positions.get("Mars", 1)
        mars_house = self._get_house_num(mars_pos, self.udayam)
        pts.append(f"{num:02d}. Mars (Planet of Action/War) sits in {mars_house} house. {'Strong offensive/competitive energy is active.' if mars_house in [3, 6, 11] else 'Strategic caution and defensive tactics are more important right now.'}")
        num += 1

        # Mercury (Significator for Decisions/Calculation - for TOSS/VOTE)
        mer_pos = self.positions.get("Mercury", 1)
        mer_house = self._get_house_num(mer_pos, self.udayam)
        pts.append(f"{num:02d}. Mercury (Significator for Calculations/Toss) in {mer_house}H. {'A favorable toss or tactical decision is highly likely.' if mer_house in [1, 5, 9, 11] else 'Tactical moves will be surprising and require quick thinking.'}")
        num += 1

        # Transit based insight
        udm_lord = self.house_lords[self.udayam]
        udm_pos = self.positions.get(udm_lord, 1)
        dist = self._get_house_num(h11_pos, udm_pos) if 'h11_pos' in locals() else 0
        pts.append(f"{num:02d}. Manifestation Pulse: The relationship between the self (Udayam) and the goal (11L) is {'strong' if dist in [1, 5, 9, 11] else 'neutral'} for this competition.")
        num += 1

        return pts, num

    def _generate_conclusion(self) -> str:
        """Generates an elaborative, customer-friendly conclusion with phases on separate lines and remedy bullets."""
        kav_h = self._get_house_num(self.kavippu, self.udayam)
        lift_date, next_sign_name = self._get_kavippu_lift_date_raw()
        rp = self.ruling_planet
        
        # Build intent-specific starting sentence
        q_text = self.jam.get('query_text', 'your query')
        diag_str = ""
        if self.intent == "HEALTH":
            d = self.findings.get('diagnosis', 'vulnerable areas')
            b = self.findings.get('block', 'energy centers')
            diag_str = f" The analysis pinpoints the **{d}** as the primary affected region, with a temporary energy block in the **{b}**."
        elif self.intent == "CAREER":
            diag_str = " The chart indicates a professional transition phase where effort and timing are both critical."
        elif self.intent == "MARRIAGE":
            diag_str = " The relationship energy is currently in a state of flux, requiring patience and elder guidance."

        conclusion = (
            f"Regarding \"{q_text}\" -{diag_str} Recovery and progress require sustained effort due to Kavippu in {kav_h}H. "
            f"Significant improvement and the 'unlock' are expected approximately around {lift_date.strftime('%B %d, %Y')} when {rp} shifts into {next_sign_name}."
        )
        query_ctx = self.query_text.strip() if self.query_text.strip() else "the queried matter"
        prefix = "CONCLUSION: "
        if len(query_ctx) > 80:
            query_ctx = query_ctx[:77] + "..."

        aru_house = self._get_house_num(self.arudam, self.udayam)
        kav_house = self._get_house_num(self.kavippu, self.udayam)
        aru_positive = aru_house in [1, 5, 9, 10, 11]
        kav_blocking = kav_house in [1, 7, 10]
        lift_date, next_sign_name = self._get_kavippu_lift_date_raw()
        lift_time = f"approximately around {lift_date.strftime('%B %d, %Y')}"
        final_manifest_date = (lift_date + _dt.timedelta(days=41)).strftime('%B %d, %Y')

        rp = self.ruling_planet
        rasi_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        curr_rasi = self.positions.get(rp, 1)
        next_rasi = rasi_names[(curr_rasi % 12)]
        br = "<br/>"
        bull = "&#8226;"

        if self.intent == "COMPETITION":
            is_cricket = self.jam.get("is_strict_competition_mode") or any(w in self.query_text.lower() for w in ["cricket", "match", "score", "toss", "vs", "team a", "team b"])
            if is_cricket and not hasattr(self, 'cricket_data'):
                self.cricket_data = self._calculate_cricket_prediction()
            
            cd = getattr(self, 'cricket_data', None)
            if cd:
                # Custom Cricket Worksheet Output - 5 Questions Format
                cricket_summary = (
                    f"<b>🏏 Cricket Match Analysis: {cd['team_a']} vs {cd['team_b']}</b>{br}"
                    f"<b>1. WHO WILL WIN THE TOSS?</b>{br}"
                    f"&nbsp;&nbsp;&nbsp;&nbsp;{cd['toss_winner']}{br}"
                    f"&nbsp;&nbsp;&nbsp;&nbsp;<i>Logic: {cd['toss_reason']}</i>{br}"
                    f"<b>2. WHO WILL BAT FIRST?</b>{br}"
                    f"&nbsp;&nbsp;&nbsp;&nbsp;{cd['bat_first']}{br}"
                    f"&nbsp;&nbsp;&nbsp;&nbsp;<i>Logic: {cd['bat_first_reason']}</i>{br}"
                    f"<b>3. BATTING FIRST, WHAT SCORE WILL THEY SCORE?</b>{br}"
                    f"&nbsp;&nbsp;&nbsp;&nbsp;{cd['bat_first']} will score {cd['bat_first_score']} runs.{br}"
                    f"&nbsp;&nbsp;&nbsp;&nbsp;<i>Logic: {cd['bat_first_score_reason']}</i>{br}"
                    f"<b>4. BATTING SECOND, WHAT SCORE WILL THEY SCORE?</b>{br}"
                    f"&nbsp;&nbsp;&nbsp;&nbsp;{cd['bat_second']} will score {cd['bat_second_score']} runs.{br}"
                    f"&nbsp;&nbsp;&nbsp;&nbsp;<i>Logic: {cd['bat_second_score_reason']}</i>{br}"
                    f"<b>5. WHO WILL WIN THE MATCH?</b>{br}"
                    f"&nbsp;&nbsp;&nbsp;&nbsp;{cd['predicted_winner']} ({cd['predicted_margin']}){br}"
                    f"&nbsp;&nbsp;&nbsp;&nbsp;<i>Logic: {cd['outcome_reason']}</i>{br}{br}"
                )
                
                if aru_positive and not kav_blocking:
                    return (
                        f"{cricket_summary}"
                        f"The general competitive configuration is highly favorable. "
                        f"Arudam in {aru_house}H validates strong momentum toward victory. "
                        f"The shift of {rp} into {next_sign_name} ({lift_time}) will be the defining moment for triumph."
                        f"{br}{br}"
                        f"<b>Expected Timeline:</b>{br}"
                        f"{bull} Phase 1 (First Innings): Momentum builds according to house strengths.{br}"
                        f"{bull} Phase 2 (Critical Overs): {rp} transition points to the key turning moment.{br}"
                        f"{bull} Phase 3 (Final Delivery): Result confirms approximately on the event cycle."
                        f"{br}{br}"
                        f"<b>Victory Remedies:</b>{br}"
                        f"{bull} Worship Lord Hanuman or Lord Murugan for strength{br}"
                        f"{bull} Perform key actions during {rp} or Mars Hora{br}"
                        f"{bull} Visualize success and maintain absolute mental clarity"
                    )
                else:
                    return (
                        f"{cricket_summary}"
                        f"Outcome requires discipline due to Kavippu in {kav_house}H. "
                        f"Hidden hurdles or intense pressure is indicated until {lift_time}."
                        f"{br}{br}"
                        f"<b>Game Forecast:</b>{br}"
                        f"{bull} Initial: Resistance from opponents or slow start. Strategy is crucial.{br}"
                        f"{bull} Turnaround: The tide starts shifting after the planetary block eases.{br}"
                        f"{bull} Final: Success expected through sustained effort and composure."
                    )
            
            # ELECTION / OTHER COMPETITION
            if aru_positive and not kav_blocking:
                return (
                    f'{prefix}Regarding "{query_ctx}" - the competitive configuration is highly favorable. '
                    f"Arudam in {aru_house} house validates a strong momentum toward success/victory. "
                    f"The shift of {rp} into {next_sign_name} ({lift_time}) will be the defining moment for triumph."
                    f"{br}{br}"
                    f"<b>Expected Timeline:</b>{br}"
                    f"{bull} Phase 1 (Now): Strategy and preparation are key. Maintain focus.{br}"
                    f"{bull} Phase 2 (Event Window): Peak performance and favorable turns during the event.{br}"
                    f"{bull} Phase 3 (Outcome): Final result or victory confirmation expected approximately around {final_manifest_date}."
                    f"{br}{br}"
                    f"<b>Recommended Remedies:</b>{br}"
                    f"{bull} Worship Lord Hanuman or Lord Murugan for strength and victory{br}"
                    f"{bull} Perform key actions during {rp} or Mars Hora{br}"
                    f"{bull} Visualize success and maintain absolute mental clarity{br}"
                    f"{bull} Donate food to athletes or workers as a symbolic gesture"
                )
            else:
                return (
                    f'{prefix}Regarding "{query_ctx}" - the outcome is requiring patience due to Kavippu in {kav_house}H. '
                    f"Hidden hurdles or intense competition from the other side is indicated until {lift_time}."
                    f"{br}{br}"
                    f"<b>Expected Timeline:</b>{br}"
                    f"{bull} Phase 1 (Initial): Resistance from opponents or external delays. Do not lose heart.{br}"
                    f"{bull} Phase 2 (Turnaround): The tide starts shifting in your favor after the planetary block eases.{br}"
                    f"{bull} Phase 3 (Final): Success expected through sustained effort approximately around {final_manifest_date}."
                    f"{br}{br}"
                    f"<b>Essential Remedies:</b>{br}"
                    f"{bull} Recite 'Hanuman Chalisa' or 'Kanda Sashti Kavasam' daily{br}"
                    f"{bull} Light a lamp at dusk and pray for the removal of obstacles{br}"
                    f"{bull} Avoid overconfidence and respect the competition's strength{br}"
                    f"{bull} Feed birds or street animals on Tuesdays/Saturdays"
                )

        elif self.intent == "CAREER":
            if aru_positive and not kav_blocking:
                return (
                    f'{prefix}Regarding "{query_ctx}" - the Prasna configuration is favorable for career advancement. '
                    f"Arudam in {aru_house}H validates strong professional momentum. "
                    f"The ruling planet {rp} will transit to {next_rasi} {lift_time}, which marks the key window for career breakthrough."
                    f"{br}{br}"
                    f"<b>Expected Timeline:</b>{br}"
                    f"{bull} Phase 1 (Days 1-10): Begin applying and networking actively.{br}"
                    f"{bull} Phase 2 (Days 11-25): A significant opportunity or interview will emerge.{br}"
                    f"{bull} Phase 3 (Days 26-41): Expect a concrete outcome - offer, confirmation, or clear direction. Full career manifestation expected approximately around {final_manifest_date} (Transit + 41 days)."
                    f"{br}{br}"
                    f"<b>Recommended Remedies:</b>{br}"
                    f"{bull} Worship Lord Murugan or Surya on Sundays for career boost{br}"
                    f"{bull} Perform career-related actions during {rp} Hora for best results{br}"
                    f"{bull} Light camphor at home before attending interviews{br}"
                    f"{bull} Carry a piece of raw turmeric for positive energy"
                )
            else:
                return (
                    f'{prefix}Regarding "{query_ctx}" - the career path has a temporary block from Kavippu in {kav_house}H. '
                    f"This block is expected to ease {lift_time} when {rp} transits to {next_rasi}."
                    f"{br}{br}"
                    f"<b>Expected Timeline:</b>{br}"
                    f"{bull} Phase 1 (Now to block lift): Focus on preparation - update skills, resume, and research opportunities. Do not make impulsive moves.{br}"
                    f"{bull} Phase 2 (After block lifts): Active job search/career moves will start yielding results within 15-20 days.{br}"
                    f"{bull} Phase 3 (Within 41 days of block lift): Full manifestation of career outcome expected approximately around {final_manifest_date} (Transit + 41 days)."
                    f"{br}{br}"
                    f"<b>Essential Remedies:</b>{br}"
                    f"{bull} Light a sesame oil lamp on Saturdays{br}"
                    f"{bull} Chant 'Om Shanaischaraya Namaha' 108 times daily{br}"
                    f"{bull} Donate black sesame seeds or black items on Saturday{br}"
                    f"{bull} Avoid announcing career plans until the offer is confirmed"
                )

        elif self.intent == "MARRIAGE":
            if aru_positive and not kav_blocking:
                return (
                    f'{prefix}Regarding "{query_ctx}" - the alliance configuration is positive. '
                    f"Arudam in {aru_house}H shows genuine potential for the relationship to proceed successfully. "
                    f"Key timing: {rp} transiting to {next_rasi} ({lift_time}) will open the alliance gate."
                    f"{br}{br}"
                    f"<b>Expected Timeline:</b>{br}"
                    f"{bull} Phase 1 (Days 1-15): Initial discussions and family alignment.{br}"
                    f"{bull} Phase 2 (Days 16-30): Formal proposal or alliance meeting.{br}"
                    f"{bull} Phase 3 (Days 31-41): Decision and commitment finalization expected approximately around {final_manifest_date} (Transit + 41 days)."
                    f"{br}{br}"
                    f"<b>Recommended Remedies:</b>{br}"
                    f"{bull} Offer white flowers to Goddess Parvati on Fridays{br}"
                    f"{bull} Recite 'Om Shukraya Namaha' 108 times daily{br}"
                    f"{bull} Wear white or light blue on alliance discussion days{br}"
                    f"{bull} Avoid arguments on Fridays"
                )
            else:
                return (
                    f'{prefix}Regarding "{query_ctx}" - moderate outcome expected due to Kavippu in {kav_house}H. '
                    f"Hidden concerns or delays from the other side may surface before {lift_time}."
                    f"{br}{br}"
                    f"<b>Expected Timeline:</b>{br}"
                    f"{bull} Phase 1 (Now): Address family concerns patiently. Do not push for immediate decision.{br}"
                    f"{bull} Phase 2 (After Kavippu eases): Re-initiate formal discussions when {rp} transits to {next_rasi}.{br}"
                    f"{bull} Phase 3 (Within next 60 days): Complete resolution expected approximately around {final_manifest_date} (Transit + 41 days)."
                    f"{br}{br}"
                    f"<b>Essential Remedies:</b>{br}"
                    f"{bull} Offer milk and white flowers at Devi temple on Fridays{br}"
                    f"{bull} Donate sweets to young girls{br}"
                    f"{bull} Avoid ego clashes within the family{br}"
                    f"{bull} Maintain a peaceful and clean home environment"
                )

        elif self.intent == "HEALTH":
            diag = self.findings.get('diagnosis', 'vulnerable areas')
            block = self.findings.get('block', 'energy pathways')
            if aru_positive and not kav_blocking:
                return (
                    f'{prefix}Regarding "{query_ctx}" - the Prasna indicates that recovery is well-supported. '
                    f"The analysis pinpoints **{diag}** as the primary affected region, with a minor block in **{block}**. "
                    f"The transit of {rp} to {next_rasi} ({lift_time}) will mark the point of significant improvement."
                    f"{br}{br}"
                    f"<b>Recovery Forecast:</b>{br}"
                    f"{bull} Phase 1 (Now to 10 days): Noticeable reduction in acute symptoms.{br}"
                    f"{bull} Phase 2 (11-25 days): Sustained stabilization and health gains.{br}"
                    f"{bull} Phase 3 (26-41 days): Significant turning point and full recovery expected approximately around {final_manifest_date} (Transit + 41 days)."
                    f"{br}{br}"
                    f"<b>Recovery Remedies:</b>{br}"
                    f"{bull} Offer water to the rising Sun daily (Surya Arghya){br}"
                    f"{bull} Light a sesame oil lamp on Saturdays for 41 days{br}"
                    f"{bull} Maintain a sattvic diet and observe the prescribed Pariharams{br}"
                    f"{bull} Worship your Kuladevata for protection and vitality"
                )
            else:
                return (
                    f'{prefix}Regarding "{query_ctx}" - recovery needs sustained effort due to the Kavippu block in {kav_house}H. '
                    f"The analysis pinpoints **{diag}** as the primary affected region, with the energy block currently impacting the **{block}**. "
                    f"Significant improvement is expected {lift_time} when {rp} transits into {next_rasi}."
                    f"{br}{br}"
                    f"<b>Recovery Forecast:</b>{br}"
                    f"{bull} Phase 1 (Initial): Gradual stabilization while the block persists.{br}"
                    f"{bull} Phase 2 (After block lifts): Rapid recovery phase starts within 15 days of the transit.{br}"
                    f"{bull} Phase 3 (Complete): Full stabilization and breakthrough expected approximately around {final_manifest_date} (Transit + 41 days)."
                    f"{br}{br}"
                    f"<b>Essential Remedies:</b>{br}"
                    f"{bull} Strictly follow medical advice and spiritual remedies consistently{br}"
                    f"{bull} Light a lamp daily at dusk and pray to Lord Shambho (Healing Form of Shiva){br}"
                    f"{bull} Donate food to the needy on the ruling planet's weekday{br}"
                    f"{bull} Chant health mantras (Om Jhoom Saha) daily 108 times"
                )


        # GENERAL
        if aru_positive and not kav_blocking:
            return (
                f'{prefix}Regarding "{query_ctx}" - the overall Prasna configuration is positive. '
                f"Arudam in {aru_house}H validates the seeker's intent. "
                f"{rp} transiting to {next_rasi} ({lift_time}) accelerates the manifestation."
                f"{br}{br}"
                f"<b>Expected Timeline:</b>{br}"
                f"{bull} Phase 1 (Days 1-14): First signs of movement.{br}"
                f"{bull} Phase 2 (Days 15-30): Tangible progress visible.{br}"
                f"{bull} Phase 3 (Days 31-41): Full resolution expected approximately around {final_manifest_date} (Transit + 41 days)."
                f"{br}{br}"
                f"<b>Recommended Remedies:</b>{br}"
                f"{bull} Light a sesame oil lamp at dusk daily{br}"
                f"{bull} Perform key activities during {rp} Hora{br}"
                f"{bull} Recite your chosen deity's mantra 108 times for 41 days{br}"
                f"{bull} Donate food or essentials to those in need"
            )
        return (
            f'{prefix}Regarding "{query_ctx}" - mixed results indicated due to Kavippu in {kav_house}H creating resistance. '
            f"The obstruction is expected to ease {lift_time} when {rp} transits to {next_rasi}."
            f"{br}{br}"
            f"<b>Expected Timeline:</b>{br}"
            f"{bull} Phase 1 (Now): Prepare and consolidate. Avoid major new commitments.{br}"
            f"{bull} Phase 2 (After block lifts): Active pursuit will yield results.{br}"
            f"{bull} Phase 3 (Within 60 days): Full outcome expected approximately around {final_manifest_date} (Transit + 41 days)."
            f"{br}{br}"
            f"<b>Essential Remedies:</b>{br}"
            f"{bull} Perform Navagraha Pooja{br}"
            f"{bull} Feed crows or stray animals regularly{br}"
            f"{bull} Light sesame oil lamp on Saturdays{br}"
            f"{bull} Maintain daily 108-count mantra chanting for 41 days"
        )

    def _get_natal_conclusion_overlay(self) -> str:
        """Generates native-specific synthesis conclusion overlay text (Mode 2 only)."""
        if not self.natal or not self.natal.get("Lagna"):
            return ""
        br = "<br/>"
        bull = "&#8226;"
        n_lagna = self.natal.get("Lagna", "")
        n_nak = self.natal.get("Nakshatra", "")
        n_states = self.natal.get("PlanetaryStates", {})
        lagna_rasi = self.natal.get("LagnaRasi", 0)
        dasha = self.natal.get("Dasha", "")

        lagna_house = self._get_house_num(lagna_rasi, self.udayam) if lagna_rasi else 0
        alignment = ""
        if lagna_house in [1, 5, 9]:
            alignment = "trine — excellent karmic alignment"
        elif lagna_house in [4, 7, 10]:
            alignment = "kendram — strong action energy"
        elif lagna_house in [6, 8, 12]:
            alignment = "dusthana — extra effort needed"
        else:
            alignment = "neutral — steady measured progress"

        overlay = (
            f"{br}{br}"
            f"<b>Native Birth Chart Insight:</b>{br}"
            f"{bull} Birth Lagna: {n_lagna} | Nakshatra: {n_nak} | Alignment: {alignment}{br}"
        )
        
        if self.intent == "CAREER":
            sat = n_states.get("Saturn", "Normal")
            overlay += f"{bull} Natal Saturn ({sat}): {'supports career discipline' if 'Friend' in str(sat) else 'requires patience in professional growth'}{br}"
        elif self.intent == "MARRIAGE":
            ven = n_states.get("Venus", "Normal")
            overlay += f"{bull} Natal Venus ({ven}): {'strong relationship karma' if 'Friend' in str(ven) or 'Direct' in str(ven) else 'relationship area needs nurturing'}{br}"
        elif self.intent == "HEALTH":
            sun = n_states.get("Sun", "Normal")
            overlay += f"{bull} Natal Sun ({sun}): {'strong constitution' if 'Friend' in str(sun) else 'vitality needs boosting'}{br}"
        
        if dasha:
            overlay += f"{bull} Current Dasha: {dasha} — interacts with Prasna outcome{br}"
        
        return overlay

    def _get_sign_name(self, rasi: int) -> str:
        names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        return names[(rasi - 1) % 12]

    def _get_sign_significance(self, house_num: int) -> str:
        signs = {
            1: "Personal identity", 2: "Family/Wealth", 3: "Efforts", 4: "Comforts/Home",
            5: "Progeny/Intellect", 6: "Obstacles/Health", 7: "Partnership", 
            8: "Karmic baggage", 9: "Fortune/Guru", 10: "Profession", 11: "Gains", 12: "Expenses"
        }
        return signs.get(house_num, "General")
