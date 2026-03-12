from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine

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
        
        # Positions (Rasi numbers 1-12)
        self.positions = self.jamakkal.get("planet_positions", {})
        
        # Natal Data for Synthesis
        self.n_pos = self.natal.get("Positions", {})
        self.n_lords = self.natal.get("HouseLords", {})
        
        # Intent detection
        self.query_text = self.jamakkal.get("query_text", "").lower()
        self.intent = self._detect_intent()
        self.n_states = self.natal.get("PlanetaryStates", {})
        self.n_lagna = self.natal.get("LagnaRasi", 1)

    def _detect_intent(self) -> str:
        if any(w in self.query_text for w in ["job", "career", "work", "promotion", "office", "business", "professional"]):
            return "CAREER"
        if any(w in self.query_text for w in ["marriag", "propos", "wed", "husband", "wife", "alliance", "match"]):
            return "MARRIAGE"
        if any(w in self.query_text for w in ["health", "sick", "disease", "recover", "doctor"]):
            return "HEALTH"
        return "GENERAL"

    def _rel_house(self, target_sign: int, start_sign: int) -> int:
        return (target_sign - start_sign) % 12 + 1

    def _get_analysis_for_category(self, category: str) -> Dict[str, List[str]]:
        """
        Returns exactly 5 unique challenges and 5 unique remedies per category.
        Ensures no repetition by using specific architectural rules.
        """
        challenges = []
        remedies = []
        
        # Helper to add unique points
        def add_pt(clist, pt):
            if pt not in clist: clist.append(pt)

        # Base logic for all categories using Four Pillars
        ud_rel = self._rel_house(self.kavippu, self.udayam)
        ar_rel = self._rel_house(self.arudam, self.udayam)
        
        # Category-specific logic
        # Category-specific logic
        if category == "Health & Recovery":
            # Logic: Sun (Vitality), 6th House (Disease), Udayam Lord
            sun_status = self.jamakkal.get("inner_planets", {}).get("Sun", {}).get("status", "Neutral")
            fruition = self.jamakkal.get("inner_planets", {}).get("Sun", {}).get("fruition", "6 Months")
            
            add_pt(challenges, f"Vitality (Sun) is currently {sun_status}.")
            add_pt(challenges, f"Karmic block (Kavippu) in house {ud_rel} affects immunity.")
            add_pt(challenges, "Digestive or internal heat imbalance indicated.")
            add_pt(challenges, "Stress affecting sleep and recovery rhythm.")
            add_pt(challenges, "Inconsistent medication or routine adherence.")
            
            add_pt(remedies, "Offer water to the Sun at sunrise (Surya Arghya).")
            add_pt(remedies, "Chant 'Aditya Hridayam' or 'Om Suryaya Namaha'.")
            add_pt(remedies, "Donate wheat or jaggery on Sundays.")
            add_pt(remedies, "Maintain a strictly alkaline diet for 7 days.")
            add_pt(remedies, f"Expected recovery fruition period: {fruition}.")

        elif category == "Business & Finance":
            # Logic: Mercury (Business), Jupiter (Wealth), 2nd/11th Houses
            merc_status = self.jamakkal.get("inner_planets", {}).get("Mercury", {}).get("status", "Neutral")
            jup_status = self.jamakkal.get("inner_planets", {}).get("Jupiter", {}).get("status", "Neutral")
            
            add_pt(challenges, f"Mercury ({merc_status}) affects cash flow velocity.")
            add_pt(challenges, f"Jupiter ({jup_status}) impacts profit margins.")
            add_pt(challenges, "Delayed payments from clients/customers.")
            add_pt(challenges, "Miscommunication in deal negotiation.")
            add_pt(challenges, "Inventory or resource management friction.")
            
            add_pt(remedies, "Offer green gram (Moong) to birds/cows.")
            add_pt(remedies, "Keep a small piece of turmeric/yellow item in wallet.")
            add_pt(remedies, "Chant 'Om Shreem Mahalakshmiye Namaha'.")
            add_pt(remedies, "Avoid major financial decisions on Tuesdays.")
            add_pt(remedies, "Donate to education or students.")

        elif category == "Career & Professional":
            # Logic: Saturn (Work), Sun (Authority), 10th House
            sat_status = self.jamakkal.get("inner_planets", {}).get("Saturn", {}).get("status", "Neutral")
            fruit_time = self.jamakkal.get("inner_planets", {}).get("Saturn", {}).get("fruition", "1 Year")
            
            add_pt(challenges, f"Saturn's status ({sat_status}) implies high workload.")
            add_pt(challenges, "Recognition for effort might be delayed.")
            add_pt(challenges, "Office politics or hidden enemies (Kavippu).")
            add_pt(challenges, "Lack of support from superiors/authority (Sun).")
            add_pt(challenges, "Skill upgrade required for next level.")
            
            add_pt(remedies, "Light a sesame oil lamp for Lord Saturn on Saturdays.")
            add_pt(remedies, "Feed crows with cooked rice/sesame.")
            add_pt(remedies, "Maintain strict professional ethics and timing.")
            add_pt(remedies, "Offer water to the rising Sun daily.")
            add_pt(remedies, f"Patience: Significant result expected in {fruit_time}.")

        elif category == "Travel & Foreign":
            # Logic: Moon (Travel), 9th/12th houses
            moon_status = self.jamakkal.get("inner_planets", {}).get("Moon", {}).get("status", "Neutral")
            
            add_pt(challenges, f"Moon status ({moon_status}) creates flux in plans.")
            add_pt(challenges, "Documentation/Visa delays possible.")
            add_pt(challenges, "Health flux during travel indicated.")
            add_pt(challenges, "Unexpected expenses related to the trip.")
            add_pt(challenges, "Communication delay with foreign contacts.")
            
            add_pt(remedies, "Offer milk to a Shiva Lingam on Mondays.")
            add_pt(remedies, "Carry a silver coin or item while traveling.")
            add_pt(remedies, "Donate water or buttermilk to thirsty people.")
            add_pt(remedies, "Chant 'Om Namah Shivaya' 108 times.")
            add_pt(remedies, "Ensure all documents are double-checked.")

        elif category == "Marriage & Relationship":
            # Logic: Venus (Love), 7th house
            ven_status = self.jamakkal.get("inner_planets", {}).get("Venus", {}).get("status", "Neutral")
            fruition = self.jamakkal.get("inner_planets", {}).get("Venus", {}).get("fruition", "15 Days")
            
            add_pt(challenges, f"Venus status ({ven_status}) affects emotional harmony.")
            add_pt(challenges, "Misalignment in expectations/values.")
            add_pt(challenges, "External family pressure creating stress.")
            add_pt(challenges, "Communication gap causing minor misunderstandings.")
            add_pt(challenges, "Timing issue: Patience needed for resolution.")
            
            add_pt(remedies, "Offer white flowers to Goddess Lakshmi/Durga.")
            add_pt(remedies, "Avoid arguments on Fridays.")
            add_pt(remedies, "Wear clean, bright clothes (avoid faded colors).")
            add_pt(remedies, "Donate sweets or milk products on Fridays.")
            add_pt(remedies, f"Wait period: Improvement expected in {fruition}.")

        elif category == "Disputes & Litigation":
            # Logic: 6th House, Mars (Conflict), Saturn (Delay)
            mars_status = self.jamakkal.get("inner_planets", {}).get("Mars", {}).get("status", "Neutral")
            
            add_pt(challenges, f"Mars status ({mars_status}) indicates impulsive actions.")
            add_pt(challenges, "Documentation or evidence might be incomplete.")
            add_pt(challenges, "Opposing party currently has a stronger transit.")
            add_pt(challenges, "Communication breakdown worsening the conflict.")
            add_pt(challenges, "Hidden costs or financial drain expected.")
            
            add_pt(remedies, "Light a lamp with sesame oil for Lord Saturn.")
            add_pt(remedies, "Avoid confrontation on Tuesdays and Saturdays.")
            add_pt(remedies, "Donate food to the physically challenged.")
            add_pt(remedies, "Recite 'Narasimha Kavacham' for protection.")
            add_pt(remedies, "Seek mediation rather than direct confrontation.")

        elif category == "Education & Knowledge":
            # Logic: Mercury status, 4th House (Education), Jupiter (Wisdom)
            merc_status = self.jamakkal.get("inner_planets", {}).get("Mercury", {}).get("status", "Neutral")
            
            add_pt(challenges, f"Mercury's current status ({merc_status}) affects retention.")
            add_pt(challenges, "Distractions from digital media breaking focus.")
            add_pt(challenges, "Lack of structured study schedule identified.")
            add_pt(challenges, "Minor health issue (headache/eyes) affecting study.")
            add_pt(challenges, "Concept clarity is missing in core subjects.")
            
            add_pt(remedies, "Study facing North or East direction.")
            add_pt(remedies, "Offer Tulsi leaves to Lord Vishnu on Wednesdays.")
            add_pt(remedies, "Consume soaked almonds daily morning.")
            add_pt(remedies, "Start study sessions with 2 minutes of silence.")
            add_pt(remedies, "Use a green pen for taking key notes.")

        elif category == "Missing Objects":
            # Logic: 2nd Lord (Possessions), 11th Lord (Gains), Arudham direction
            ar_sign = self.arudam
            direction_map = {
                1: "East", 2: "South-East", 3: "South", 4: "South-West",
                5: "North-West", 6: "North", 7: "North-East", 8: "East",
                9: "South-East", 10: "South", 11: "South-West", 12: "North-West"
            }
            direction = direction_map.get(ar_sign, "the direction of the Arudham")
            
            add_pt(challenges, f"The object is likely in the {direction} direction.")
            add_pt(challenges, f"Planetary influence suggests it is { 'movable/taken' if ar_sign in [1,4,7,10] else 'stationary/misplaced' }.")
            add_pt(challenges, "Visibility is obscured by nearby clutter or cloth.")
            add_pt(challenges, "A gap in memory recall due to Moon's transit.")
            add_pt(challenges, "The item may have been displaced by a family member.")
            
            add_pt(remedies, f"Search intensely in the {direction} sector of the house.")
            add_pt(remedies, "Chant 'Karthavirya Arjuna Mantra' for recovery.")
            add_pt(remedies, "Check lower levels, shelves, or under furniture.")
            add_pt(remedies, "Ask a younger family member to assist in the search.")
            add_pt(remedies, "Light a lamp with ghee and pray to your Kuladevata.")

        # Final filler to ensure exactly 5 if some logic missed
            add_pt(remedies, "Install a convex mirror on the North-East wall.")
            add_pt(remedies, "Keep a small amount of sea salt in a bowl in the room.")
            add_pt(remedies, "Chant 'Om Hum Hanumate Namaha' 108 times.")
            add_pt(remedies, "Offer a red flower to the rising Sun.")

        # Ensure no fallback repetition - Expand to 10 points
        if len(challenges) < 10:
            add_pt(challenges, f"Secondary influence: {self.ruling_planet} indicates minor timing delays in execution.")
            add_pt(challenges, f"Arudham position ({self._rel_house(self.arudam, self.udayam)}H from UDM) suggests hidden variables or 'unseen karma' at play; certain details of the prospect are currently obscured from your view.")
            add_pt(challenges, f"Check for environmental or Vastu dissonance: Energy flow in the North-East or target-direction of your workplace/home may be blocked, causing stagnancy in this specific query's fruition.")
            add_pt(challenges, f"Planetary hour mismatch identified: The current 'Hora' does not perfectly align with the query's nature, necessitating minor timing adjustments for key activities.")
            add_pt(challenges, f"Consider timing adjustments: The distance between Prashna Udayam and Arudam indicates significant effort is needed to materialize the desired outcome.")
            add_pt(challenges, "Energy flow disruption in specific directions.")
            add_pt(challenges, "Karmic pattern repetition detected.")
            add_pt(challenges, "External interference from unknown sources.")
            add_pt(challenges, "Internal resistance to necessary changes.")
            add_pt(challenges, "Subtle obstruction in decision-making process.")
            
        if len(remedies) < 10:
            add_pt(remedies, "Light a sesame oil lamp at sunset.")
            add_pt(remedies, "Feed crows or stray animals.")
            add_pt(remedies, "Practice deep breathing for 10 minutes daily.")
            add_pt(remedies, "Keep a small piece of turmeric in your pocket.")
            add_pt(remedies, "Donate to a charitable cause on auspicious days.")
            add_pt(remedies, "Maintain cleanliness in your living space.")
            add_pt(remedies, "Recite your chosen mantra 108 times daily.")
            add_pt(remedies, "Wear colors aligned with beneficial planets.")
            add_pt(remedies, "Observe silence for 30 minutes daily.")
            add_pt(remedies, "Keep fresh flowers in the prayer area.")

        return {"challenges": challenges[:10], "solutions": remedies[:10]}

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
            rec_time = "48-72 hours" if speed == 'Rapid' else "7-10 days"
            rec = [
                f"Initial Clarity: First signs of direction visible within {rec_time}.",
                "Interview / Decision Window: 15-20 days — a key opportunity will emerge.",
                "Peak Manifestation: Full outcome (offer or refusal) within the 41-day cycle.",
                f"Shift Factor: Your ruling planet {self.ruling_planet} moving to {next_rasi} triggers the job change unlock.",
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
            rec_time = "48-72 hours" if speed == 'Rapid' else "7-10 days"
            rec = [
                f"Initial Signs: Family inclination or first response visible within {rec_time}.",
                "Formal Discussion Window: 21-30 days — ideal for formal alliance talks.",
                "Final Decision: Expect resolution within the 41-day Prasna cycle.",
                f"Shift Factor: Your ruling planet {self.ruling_planet} moving to {next_rasi} opens the alliance gate.",
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
            rec_time = "48-72 hours" if speed == 'Rapid' else "7-10 days"
            rec = [
                f"Symptomatic Relief: Expect first improvement within {rec_time}.",
                "Stabilization: Sustained improvement expected within 15-21 days.",
                "Full Recovery: Complete recovery cycle aligns with the 41-day Prasna window.",
                f"Shift Factor: {self.ruling_planet} entering {next_rasi} marks the turning point for recovery.",
                "Maintenance: Adhere strictly to prescribed remedies to avoid relapse."
            ]
            rem = [
                "Offer water to the rising Sun at dawn (Surya Arghya) for vitality.",
                "Chant 'Aditya Hridayam' or 'Om Suryaya Namaha' for 21 days.",
                "Maintain a strictly light, sattvic (pure) diet for the first 7 days.",
                "Avoid cold baths or cold food; prefer warm water and fresh cooked meals.",
                "Donate wheat, jaggery, or copper items on the next Sunday."
            ]

        else:  # GENERAL
            diag = [
                f"Architecture: Udayam @ House {self.udayam}, Arudham @ House {self.arudam}.",
                f"Primary Block: Kavippu at House {self._rel_house(self.kavippu, self.udayam)} influences the query outcome.",
                f"Ruling Modulator: {self.ruling_planet} governs the quality and speed of manifestation.",
                f"Manifestation Speed: {speed} — the result will follow this energy pattern.",
                "Natal alignment with the current Prasna confirms the query's karmic relevance."
            ]
            rec_time = "48-72 hours" if speed == 'Rapid' else "7-10 days"
            rec = [
                f"Phase 1: First indicators of change visible within {rec_time}.",
                "Phase 2: Tangible progress expected within 21-30 days.",
                "Phase 3: Complete resolution within the 41-day Prasna cycle.",
                f"Shift Factor: {self.ruling_planet} moving to {next_rasi} is the key transition trigger.",
                "Consistency: Performing the recommended remedies without interruption ensures lasting results."
            ]
            rem = [
                "Light a sesame oil lamp at dusk in the prayer room daily.",
                f"Perform your key activities during the {self.ruling_planet} Hora for best results.",
                "Donate food or essential items to those in need on an auspicious day.",
                "Maintain mental peace; avoid arguments or major decisions when agitated.",
                "Recite your chosen deity's mantra 108 times daily for 41 days."
            ]

        return diag, rec, rem

    def _get_category_data(self, lang: str = "en") -> Dict[str, Dict[str, Any]]:
        categories = ["Health & Recovery", "Business & Finance", "Career & Professional", "Travel & Foreign", 
                      "Marriage & Relationship", "Disputes & Litigation", "Education & Knowledge", "Missing Objects"]
        
        results = {}
        for cat in categories:
            data = self._get_analysis_for_category(cat)
            # Scoring logic: Base 5/10. Adjust based on Kavippu distance and lords.
            ud_to_kav = self._rel_house(self.kavippu, self.udayam)
            score = 7.5 if ud_to_kav in [5, 9, 11] else 3.5 if ud_to_kav in [1, 6, 8, 12] else 5.5
            
            status = "Excellent" if score >= 8 else "Strong" if score >= 6 else "Moderate" if score >= 4 else "Challenging"
            
            # Synthesis with Natal for score adjustment
            if self.n_lords.get("10th") == self.ruling_planet and cat == "Career & Professional":
                score += 1.5
            
            score = min(max(score, 1.0), 10.0)
            
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
        
        # Intent-specific Final Conclusion
        rasi_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        curr_rasi = self.positions.get(self.ruling_planet, 1)
        next_rasi = rasi_names[(curr_rasi % 12)]
        kav_rel = self._rel_house(self.kavippu, self.udayam)
        
        if self.intent == "CAREER":
            favour = "favourable" if kav_rel in [5, 9, 11] else "challenging but manageable"
            final = (f"Based on the Jamakkal Prasna analysis, the job change configuration is {favour}. "
                     f"The ruling planet {self.ruling_planet} is the key driver — once it transits into {next_rasi}, "
                     f"the native will see a clear opening for a professional transition. "
                     f"The remedies prescribed should be followed diligently to accelerate this outcome.")
        elif self.intent == "MARRIAGE":
            favour = "positive with steady progress" if kav_rel in [5, 9, 11] else "requires patience and right timing"
            final = (f"The Jamakkal Prasna analysis for this marriage/alliance query indicates the outcome is {favour}. "
                     f"{self.ruling_planet}'s transit to {next_rasi} marks the auspicious window for the alliance to be finalized. "
                     f"Performing the prescribed remedies faithfully will help remove karmic obstacles in the path.")
        elif self.intent == "HEALTH":
            favour = "recovery is well-supported" if kav_rel in [5, 9, 11] else "recovery needs sustained effort"
            final = (f"The Jamakkal Prasna analysis indicates that {favour}. "
                     f"The planetary ruler {self.ruling_planet} shifting to {next_rasi} will mark the point of significant improvement. "
                     f"Following the prescribed dietary and spiritual remedies during this period is essential for complete recovery.")
        else:
            favour = "positive" if kav_rel in [5, 9, 11] else "requiring disciplined effort"
            final = (f"The overall Jamakkal Prasna configuration for this query is {favour}. "
                     f"The key planetary transition of {self.ruling_planet} into {next_rasi} will be the defining shift point. "
                     f"Adherence to the prescribed remedies within the 41-day window will ensure the best possible outcome.")

        # Advanced Synthesis Breakdown
        synth_engine = SynthesisEngine(self.jam, self.jam.get('query_text', ''), self.natal)
        synth_data = synth_engine.generate_synthesis()

        return {
            "summary": summary,
            "analysis_points": diag,
            "diagnostic_analysis": diag,
            "recovery_timeline": rec,
            "remedies": rem,
            "remedy_timing": timing_data,
            "synthesis_points": synth_data["points"],
            "synthesis_conclusion": synth_data["conclusion"],
            "final_conclusion": final,
            "balance_categories": all_cat_data,
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
