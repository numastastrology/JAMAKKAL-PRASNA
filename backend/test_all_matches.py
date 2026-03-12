import sys, os
from datetime import datetime
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine

matches = [
    {"name": "SA vs IND (Feb 22, Ahmedabad)", "lat": 23.0225, "lon": 72.5714, "dt": datetime(2026, 2, 22, 19, 0, 0), "team_a": "SOUTH AFRICA", "team_b": "INDIA", "winner": "Team A (SA)"},
    {"name": "WI vs ZIM (Feb 23, Wankhede)", "lat": 18.9276, "lon": 72.8258, "dt": datetime(2026, 2, 23, 19, 0, 0), "team_a": "WEST INDIES", "team_b": "ZIMBABWE", "team_a_captain": "Rovman Powell", "winner": "Team A (WI)"},
    {"name": "PAK vs ENG (Feb 24, Pallekele)", "lat": 7.2846, "lon": 80.6380, "dt": datetime(2026, 2, 24, 19, 0, 0), "team_a": "PAKISTAN", "team_b": "ENGLAND", "winner": "Team B (ENG)"},
    {"name": "NZ vs SL (Feb 25, Colombo)", "lat": 6.9271, "lon": 79.8612, "dt": datetime(2026, 2, 25, 19, 0, 0), "team_a": "NEW ZEALAND", "team_b": "SRI LANKA", "team_a_captain": "Mitchell Santner", "winner": "Team A (NZ)"},
    {"name": "SA vs WI (Feb 26, Ahmedabad)", "lat": 23.0225, "lon": 72.5714, "dt": datetime(2026, 2, 26, 19, 0, 0), "team_a": "SOUTH AFRICA", "team_b": "WEST INDIES", "winner": "Team A (SA)"},
    {"name": "IND vs ZIM (Feb 26, Chennai)", "lat": 13.0827, "lon": 80.2707, "dt": datetime(2026, 2, 26, 19, 0, 0), "team_a": "INDIA", "team_b": "ZIMBABWE", "winner": "Team A (IND)"},
    {"name": "NZ vs ENG (Feb 27, Colombo)", "lat": 6.9271, "lon": 79.8612, "dt": datetime(2026, 2, 27, 19, 0, 0), "team_a": "NEW ZEALAND", "team_b": "ENGLAND", "winner": "Team B (ENG)"},
    {
        "name": "IND vs NZ (Mar 8, Ahmedabad)",
        "lat": 23.0225,
        "lon": 72.5714,
        "dt": datetime(2026, 3, 8, 19, 0, 0),
        "team_a": "INDIA",
        "team_b": "NEW ZEALAND",
        "team_a_captain": "Suryakumar Yadav",
        "team_b_captain": "Mitchell Santner",
        "winner": "Team A (IND)"
    }
]

for m in matches:
    print(f"\n{'='*50}\n{m['name']} -> Actual Winner: {m['winner']}\n{'='*50}")
    je = JamakkalEngine(m['lat'], m['lon'], m['dt'])
    jd = je.compute_all()
    # Enforce strict competition
    jd['is_strict_competition_mode'] = True
    team_a_str = f"{m['team_a']} ({m['team_a_captain']})" if 'team_a_captain' in m else m['team_a']
    team_b_str = f"{m['team_b']} ({m['team_b_captain']})" if 'team_b_captain' in m else m['team_b']
    query = f"TEAM A : {team_a_str}\nTEAM B : {team_b_str}"
    se = SynthesisEngine(jd, query)
    
    udm = se.udayam
    l1 = se.house_lords[udm]
    h7 = (udm + 6) % 12 or 12
    l7 = se.house_lords[h7]
    
    s_l1 = se._get_planet_strength_score(l1)
    s_l7 = se._get_planet_strength_score(l7)
    
    # Houses for A
    h3 = (udm + 2) % 12 or 12
    h6 = (udm + 5) % 12 or 12
    h10 = (udm + 9) % 12 or 12
    h11 = (udm + 10) % 12 or 12
    # Houses for B
    b_h3 = (h7 + 2) % 12 or 12
    b_h6 = (h7 + 5) % 12 or 12
    b_h10 = (h7 + 9) % 12 or 12
    b_h11 = (h7 + 10) % 12 or 12
    
    print(f"Udayam: {udm} ({je.RASI_NAMES[udm]}) -> L1: {l1} (Base Strength: {s_l1})")
    print(f"7th House: {h7} ({je.RASI_NAMES[h7]}) -> L7: {l7} (Base Strength: {s_l7})")
    
    s_h3 = se._get_planet_strength_score(se.house_lords[h3])
    s_h6 = se._get_planet_strength_score(se.house_lords[h6])
    s_h11 = se._get_planet_strength_score(se.house_lords[h11])
    
    bs_h3 = se._get_planet_strength_score(se.house_lords[b_h3])
    bs_h6 = se._get_planet_strength_score(se.house_lords[b_h6])
    bs_h11 = se._get_planet_strength_score(se.house_lords[b_h11])
    
    # Base Rays on Lagna and 7th
    l1_b_rays, l1_m_rays, _ = se._calculate_house_rays(udm)
    l7_b_rays, l7_m_rays, _ = se._calculate_house_rays(h7)
    
    # Kavippu check
    kvp = se.kavippu
    print(f"Kavippu Rasi: {kvp} ({je.RASI_NAMES[kvp]})")
    # Calculate synthesised strength by engine
    try:
        se.generate_synthesis()
        cd = se.cricket_data
        
        # Calculate the derived strengths manually to show
        l1_strength = s_l1 + (s_h3 + s_h6 + s_h11) * 0.334
        l7_strength = s_l7 + (bs_h3 + bs_h6 + bs_h11) * 0.334
        
        print(f"L1 Str: {l1_strength:.2f} | L7 Str: {l7_strength:.2f}")
        print(f"Pred: {cd.get('predicted_winner')} | A Score: {cd.get('team_a_score')} | B Score: {cd.get('team_b_score')}")
        print("--- A Reason ---")
        print(cd.get('team_a_score_reason').replace("<br/>", "\n").replace("&bull;", "-"))
        print("--- B Reason ---")
        print(cd.get('team_b_score_reason').replace("<br/>", "\n").replace("&bull;", "-"))
    except Exception as e:
        print(f"Error running synthesis: {e}")
