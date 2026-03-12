from typing import Dict, Any, List, Optional
import re

class SynthesisEngine:
    """
    Advanced Synthesis Engine for Jamakkal Prasna.
    Implements Professional Horary Standards with deep elaborative narrative.
    """

    def __init__(self, jamakkal_data: Dict[str, Any], query_text: str = "", natal_data: Dict[str, Any] = None):
        self.jam = jamakkal_data
        self.query_text = query_text.lower()
        self.natal = natal_data or {}
        
        # Inner pillars
        inner = self.jam.get("inner_planets", {})
        self.udayam = self._extract_rasi(inner.get("Udayam"))
        self.arudam = self._extract_rasi(inner.get("Arudam"))
        self.kavippu = self._extract_rasi(inner.get("Kavippu"))
        
        # Positions & Transits
        self.positions = self.jam.get("planet_positions", {})
        self.transits = self.jam.get("transits", {})
        
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
        if any(w in self.query_text for w in ["job", "career", "work", "promotion", "office", "business", "professional"]):
            return "CAREER"
        if any(w in self.query_text for w in ["marriag", "propos", "wed", "husband", "wife", "alliance", "match"]):
            return "MARRIAGE"
        if any(w in self.query_text for w in ["health", "sick", "disease", "recover", "doctor"]):
            return "HEALTH"
        return "GENERAL"

    def _get_planet_details(self, name: str) -> str:
        t = self.transits.get(name, {})
        if not t: return name
        return f"{name} ({t.get('rasi')} @ {t.get('degree')})"

    def generate_synthesis(self) -> Dict[str, Any]:
        points = []
        
        # 1. ARUDAM VALIDATION (The Root)
        aru_house = self._get_house_num(self.arudam, self.udayam)
        pt1 = f"01. ARUDAM ({self._get_sign_name(self.arudam)}) in {aru_house}H from UDAYAM ({self._get_sign_name(self.udayam)})."
        if aru_house in [1, 5, 9, 11]:
            pt1 += " This validates the seeker's intense focus and high probability of success for the query."
        elif aru_house in [2, 10]:
            pt1 += " Indicates the query is rooted in material gains and status stability."
        else:
            pt1 += " Suggests the query arises from a period of flux or external pressures."
        points.append(pt1)

        # 2. INTENT SPECIFIC LOGIC
        if self.intent == "CAREER":
            points.extend(self._generate_career_points())
        elif self.intent == "MARRIAGE":
            points.extend(self._generate_marriage_points())
        else:
            points.extend(self._generate_general_points())

        # 3. KAVIPPU (THE BLOCK)
        kav_h = self._get_house_num(self.kavippu, self.udayam)
        pt_kav = f"08. KAVIPPU in {kav_h}H ({self._get_sign_name(self.kavippu)}) "
        if kav_h == 1: pt_kav += "directly blocks the seeker's initiative; delay is inevitable."
        elif kav_h == 10: pt_kav += "indicates a professional hurdle or hidden enmity at the workplace."
        elif kav_h == 7: pt_kav += "suggests opposition from partners or significant delays in agreements."
        else: pt_kav += f"impacts the {self._get_sign_significance(kav_h)} area of life currently."
        points.append(pt_kav)

        # 4. MOON (THE MINDSET)
        mo_pos = self.positions.get("Moon", 1)
        pt_mo = f"09. MOON (Mind) at house {self._get_house_num(mo_pos, self.udayam)} from Udayam."
        if self._get_house_num(mo_pos, self.udayam) in [1, 5, 9]:
            pt_mo += " The native is strongly resolved and mentally prepared for the outcome."
        else:
            pt_mo += " There is considerable mental stress and uncertainty about the next steps."
        points.append(pt_mo)

        # 5. NATAL OVERLAY (IF AVAILABLE)
        if self.natal:
            n_lagna = self.natal.get("LagnaRasi", 1)
            n_house = self._get_house_num(n_lagna, self.udayam)
            pt_nat = f"10. JANMA LAGNA in {n_house}H from Prashna Udayam."
            if n_house in [1, 5, 9, 11]: pt_nat += " The birth potential is currently in synergy with the transit configuration."
            else: pt_nat += " Extra remedial effort is needed to align birth karmas with current desires."
            points.append(pt_nat)

        # 6. CONCLUSION
        conclusion = self._generate_conclusion()

        return {
            "points": points,
            "conclusion": conclusion
        }

    def _generate_career_points(self) -> List[str]:
        pts = []
        h10_rasi = (self.udayam + 9) % 12 or 12
        h10_lord = self.house_lords[h10_rasi]
        h10_pos = self.positions.get(h10_lord, 1)
        
        pts.append(f"02. Professional Lord (10L) {h10_lord} is placed in {self._get_house_num(h10_pos, self.udayam)}H.")
        if h10_pos == self.arudam: pts.append("03. 10L aligned with Arudam suggests professional status is the primary driver now.")
        elif h10_pos == self.kavippu: pts.append("03. 10L overshadowed by Kavippu indicates a temporary professional 'cutoff' or block.")
        
        # Saturn (Natural Career Indicator)
        sat_pos = self.positions.get("Saturn", 1)
        pts.append(f"04. Saturn (Karma-Karaka) sits in {self._get_house_num(sat_pos, self.udayam)}H, suggesting nature of work pressure.")
        
        # Stress Check
        if "stress" in self.query_text or "favourable" in self.query_text:
            h6_rasi = (self.udayam + 5) % 12 or 12
            h6_lord = self.house_lords[h6_rasi]
            pts.append(f"05. Service/Enemy Lord (6L) {h6_lord} is in {self._get_house_num(self.positions.get(h6_lord, 1), self.udayam)}H, causing mental stress.")
            
        pts.append(f"06. Transition Pulse: {self.house_lords[self.udayam]} and 10L are {self._get_house_num(h10_pos, self.udayam)} houses apart.")
        pts.append(f"07. Economic Gains: 11L {self.house_lords[(self.udayam+10)%12 or 12]} placement determines financial benefit of the change.")
        return pts

    def _generate_marriage_points(self) -> List[str]:
        pts = []
        h7_rasi = (self.udayam + 6) % 12 or 12
        h7_lord = self.house_lords[h7_rasi]
        h7_pos = self.positions.get(h7_lord, 1)
        
        pts.append(f"02. Marriage Lord (7L) {h7_lord} is placed in {self._get_house_num(h7_pos, self.udayam)}H.")
        if h7_pos == self.udayam: pts.append("03. 7L is coming towards Udayam, suggesting proposal/alliance is approaching quickly.")
        elif h7_pos == self.kavippu: pts.append("03. 7L in Kavippu suggests a major hidden hurdle or delayed decision from the other side.")
        
        # Family House
        h2_rasi = (self.udayam + 1) % 12 or 12
        h2_lord = self.house_lords[h2_rasi]
        pts.append(f"04. Family Lord (2L) {h2_lord} placement in {self._get_house_num(self.positions.get(h2_lord, 1), self.udayam)}H indicates family involvement.")
        
        pts.append(f"05. Mutual Compatibility: Distance between {self.house_lords[self.udayam]} and 7L indicates level of understanding.")
        pts.append(f"06. Domestic Harmony: 4L {self.house_lords[(self.udayam+3)%12 or 12]} indicates peace in the new alliance.")
        pts.append(f"07. Venus (Karaka): Placement of Venus determines the sweetness and success of the relationship.")
        return pts

    def _generate_general_points(self) -> List[str]:
        pts = []
        pts.append(f"02. Udayam Lord {self.house_lords[self.udayam]} is in {self._get_house_num(self.positions.get(self.house_lords[self.udayam], 1), self.udayam)}H.")
        pts.append(f"03. Arudam Lord {self.house_lords[self.arudam]} is in {self._get_house_num(self.positions.get(self.house_lords[self.arudam], 1), self.udayam)}H.")
        pts.append(f"04. House of Gains ({self._get_sign_name((self.udayam+10)%12 or 12)}) status check for fruitions.")
        pts.append(f"05. House of Loss ({self._get_sign_name((self.udayam+11)%12 or 12)}) analysis for potential outflows.")
        pts.append("06. Planetary relationship between UDM and ARU indicates the gap between desire and reality.")
        pts.append("07. Presence of any Malefics in Kendras (1, 4, 7, 10) indicates obstacles in path.")
        return pts

    def _generate_conclusion(self) -> str:
        if self.intent == "CAREER":
            h10_pos = self.positions.get(self.house_lords[(self.udayam + 9) % 12 or 12], 1)
            if self._get_house_num(h10_pos, self.udayam) in [1, 5, 9, 10, 11] and h10_pos != self.kavippu:
                return "CONCLUSION: Favorable transition indicated. The proposed job change will bring professional growth and better status."
            else:
                return "CONCLUSION: Caution advised. Hidden obstacles (Kavippu) suggest waiting for a few months before finalizing the change."
        elif self.intent == "MARRIAGE":
            if self._get_house_num(self.arudam, self.udayam) in [1, 7, 11] and self.kavippu != (self.udayam + 6) % 12 or 12:
                return "CONCLUSION: High compatibility and success. The alliance is promising and can move to finalization stages."
            else:
                return "CONCLUSION: Moderate results. Address the hidden concerns (Kavippu) before making a final commitment."
        return "CONCLUSION: Mixed results. Maintain steady effort and perform the suggested remedies for best outcome."

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
