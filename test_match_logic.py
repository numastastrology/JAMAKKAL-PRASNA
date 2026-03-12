import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from engines.jamakkal import JamakkalEngine
from engines.synthesis import SynthesisEngine
from datetime import datetime

je = JamakkalEngine(23.0225, 72.5714, datetime(2026,2,26,15,0,0))
jd=je.compute_all()
qt='South Africa vs West Indies match in Ahmedabad'
jd['query_text']=qt
se=SynthesisEngine(jd, qt)
print(f"\nDEBUG M1: Udayam={se.udayam}, 7H={(se.udayam+5)%12+1}, L1={se.house_lords[se.udayam]}, L7={se.house_lords[(se.udayam+5)%12+1]}")
out=se._generate_conclusion()
print('MATCH 1 (SA vs WI at 3PM):\n' + out.replace('<br/>', '\n').replace('&nbsp;', ' '))

je2 = JamakkalEngine(13.0827, 80.2707, datetime(2026,2,26,19,0,0))
jd2=je2.compute_all()
qt2='India vs Zimbabwe match in Chennai'
jd2['query_text']=qt2
se2=SynthesisEngine(jd2, qt2)
print(f"\nDEBUG M2: Udayam={se2.udayam}, 7H={(se2.udayam+5)%12+1}, L1={se2.house_lords[se2.udayam]}, L7={se2.house_lords[(se2.udayam+5)%12+1]}")
out2=se2._generate_conclusion()
print('\nMATCH 2 (IND vs ZIM at 7PM):\n' + out2.replace('<br/>', '\n').replace('&nbsp;', ' '))
