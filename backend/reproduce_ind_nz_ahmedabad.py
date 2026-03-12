import sys, os
from datetime import datetime
# Ensure backend is in path
current_dir = os.getcwd()
if 'backend' not in sys.path:
    sys.path.append(os.path.join(current_dir, 'backend'))

from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine

def main():
    # India vs New Zealand, 8 March 2026, 7PM Ahmedabad
    # NZ won toss, elected to field. India batted first.
    lat=23.0225; lon=72.5714; dt=datetime(2026, 3, 8, 19, 0, 0)
    je = JamakkalEngine(lat, lon, dt)
    jd = je.compute_all()
    
    # Simulate backend behavior
    jd['query_time'] = dt.isoformat()
    jd['is_strict_competition_mode'] = True
    jd['toss_winner'] = 'New Zealand'
    jd['toss_decision'] = 'Field'
    
    qt = 'India vs New Zealand'
    
    se = SynthesisEngine(jd, qt)
    se.generate_synthesis()
    
    if hasattr(se, 'cricket_data'):
        cd = se.cricket_data
        print(f"Match: {cd.get('team_a')} vs {cd.get('team_b')}")
        print(f"Toss Winner: {cd.get('toss_winner')}")
        print(f"Bat First: {cd.get('bat_first')} | Score: {cd.get('bat_first_score')}")
        print(f"Bat Second: {cd.get('bat_second')} | Score: {cd.get('bat_second_score')}")
        print(f"Predicted Winner: {cd.get('predicted_winner')}")
        
        # Check raw strengths - these are in se after generate_synthesis or _calculate_cricket_prediction
        # We can re-run the strength calc or look at what's in se if possible
        # Actually l1 and l7 are computed inside _calculate_cricket_prediction
        
        print('--- RAW DATA ---')
        print(f"Udayam: {se.udayam}")
        print(f"Arudam: {se.arudam}")
        print(f"Kavippu: {se.kavippu}")
        print(f"Ruling Planet: {se.ruling_planet}")
        
        print('--- REASONING BA ---')
        print(cd.get('bat_first_score_reason'))
        print('--- REASONING BB ---')
        print(cd.get('bat_second_score_reason'))
    else:
        print('No cricket data generated.')

if __name__ == '__main__':
    main()
