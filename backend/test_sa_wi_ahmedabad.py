import sys, os
from datetime import datetime
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine

def main():
    # SA vs WI, 26 Feb 2026, 7PM Ahmedabad
    lat=23.0225; lon=72.5714; dt=datetime(2026, 2, 26, 19, 0, 0)
    je = JamakkalEngine(lat, lon, dt)
    jd = je.compute_all()
    
    # We set strict competition mode correctly as backend does
    jd['is_strict_competition_mode'] = True
    jd['toss_winner'] = 'West Indies'
    jd['toss_decision'] = 'Bat'
    
    qt = 'TEAM A : SOUTH AFRICA\nTEAM B : WEST INDIES'
    
    se = SynthesisEngine(jd, qt)
    se.generate_synthesis()
    
    if hasattr(se, 'cricket_data'):
        cd = se.cricket_data
        print('Team A (L1):', cd.get('team_a'))
        print('Team B (L7):', cd.get('team_b'))
        print('Toss Winner:', cd.get('toss_winner'))
        print('Bat First Score:', cd.get('bat_first_score'))
        print('Bat Second Score:', cd.get('bat_second_score'))
        print('Predicted Winner:', cd.get('predicted_winner'))
        print('--- Reasoning A ---')
        print(cd.get('team_a_score_reason'))
        print('--- Reasoning B ---')
        print(cd.get('team_b_score_reason'))
    else:
        print('No cricket data generated.')

if __name__ == '__main__':
    main()
