import sys, os
from datetime import datetime
# Ensure backend is in path
current_dir = os.getcwd()
if 'backend' not in sys.path:
    sys.path.append(os.path.join(current_dir, 'backend'))

from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine

def debug_strength():
    # India vs New Zealand, 8 March 2026, 7PM Ahmedabad
    lat=23.0225; lon=72.5714; dt=datetime(2026, 3, 8, 19, 0, 0)
    je = JamakkalEngine(lat, lon, dt)
    jd = je.compute_all()
    
    jd['is_strict_competition_mode'] = True
    qt = 'India vs New Zealand'
    
    se = SynthesisEngine(jd, qt)
    
    # We want to see the details inside _calculate_cricket_prediction
    # But it's internal. Let's replicate the logic or use a hook.
    
    print(f"Udayam: {se.udayam} | Arudam: {se.arudam} | Kavippu: {se.kavippu}")
    print(f"Ruling Planet: {se.ruling_planet}")
    
    l1 = se.house_lords[se.udayam]
    h7_rasi = (se.udayam + 6) % 12 or 12
    l7 = se.house_lords[h7_rasi]
    
    print(f"Team A Lord (L1): {l1} in House {se._get_house_num(se.positions.get(l1, 1), se.udayam)}")
    print(f"Team B Lord (L7): {l7} in House {se._get_house_num(se.positions.get(l7, 1), se.udayam)}")

    # Run the actual prediction to get the final res
    res = se._calculate_cricket_prediction()
    print(f"\nFinal Scores: {res['team_a_score']} vs {res['team_b_score']}")
    
    # Let's try to find where the 21.8 came from
    # I'll manually run parts of get_total_strength for l1
    
    print("\n--- India (L1: Sun) Strength Breakdown ---")
    base_s = se._get_planet_strength_score(l1, se.udayam)
    print(f"Base Score (_get_planet_strength_score): {base_s}")
    
    # Occ Bonus
    occ_bonus = 0
    ref_rasi = se.udayam
    for p, p_rasi in se.positions.items():
        is_jama = "Jama" in p
        if p_rasi == ref_rasi:
            norm_p = p.replace("Jama ", "")
            if se.EXALTATION_SIGNS.get(norm_p) == ref_rasi or ref_rasi in se.OWN_SIGNS.get(norm_p, []):
                val = 3.5 if se.EXALTATION_SIGNS.get(norm_p) == ref_rasi else 2.0
                occ_bonus += (val * 1.5 if is_jama else val)
            else:
                val = 1.5
                h_num = se._get_house_num(p_rasi, ref_rasi)
                if norm_p in se.MALEFIC_PLANETS:
                    if h_num in [3, 6, 11]: occ_bonus += (val * 1.5 if is_jama else val)
                    else: occ_bonus -= (val * 1.5 if is_jama else val)
                else:
                    occ_bonus += (val * 1.5 if is_jama else val)
    print(f"Occ Bonus: {occ_bonus}")
    
    # Arudam Bonus
    aru_h = se._get_house_num(se.arudam, ref_rasi)
    aru_bonus = 0
    if aru_h in [1, 10, 11, 5, 9]: aru_bonus = 3.0
    elif aru_h in [3, 6]: aru_bonus = 1.5
    elif aru_h in [8, 12]: aru_bonus = -2.0
    print(f"Arudam Bonus: {aru_bonus}")
    
    # Support Bonus
    h3 = (ref_rasi + 2) % 12 or 12
    h6 = (ref_rasi + 5) % 12 or 12
    h11 = (ref_rasi + 10) % 12 or 12
    support_bonus = sum([se._get_planet_strength_score(se.house_lords[r], ref_rasi) for r in [h3, h6, h11]]) / 3.0
    print(f"Support Bonus: {support_bonus}")
    
    # Kavippu
    k_penalty = 0
    if se.kavippu == ref_rasi: k_penalty = -1.5
    elif se.kavippu == (ref_rasi + 6)%12 or 12: k_penalty = 1.5
    print(f"Kavippu Adjustment: {k_penalty}")
    
    total = base_s + occ_bonus + aru_bonus + support_bonus + k_penalty
    print(f"TOTAL: {total}")

    print("\n--- NZ (L7: Saturn) Strength Breakdown ---")
    base_s2 = se._get_planet_strength_score(l7, h7_rasi)
    print(f"Base Score: {base_s2}")
    
    # get final string from cd
    print(f"L7 String: {res.get('bat_second_score_reason')}")

if __name__ == "__main__":
    debug_strength()
