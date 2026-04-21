import React, { useRef, useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, AlertTriangle, Star, Shield, Users, Crown, Download, Info, Edit3, CheckCircle, ArrowRight } from 'lucide-react';
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';

type CandidateId = 'stalin' | 'eps' | 'seeman' | 'vijay' | 'annamalai' | 'ramadoss';

interface CandidateData {
  id: CandidateId;
  name: string;
  icon: React.ReactNode;
  color: string;
  dobInfo: string;
  astrology: string;
  verdict: string;
  chartData: string[]; // 12 elements starting from Aries
  chartColors?: Record<number, string>; // CSS color overides for specific Rasi blocks
  positives: string[];
  negatives: string[];
}

const initialCandidatesData: CandidateData[] = [
  {
    id: 'stalin',
    name: 'M.K. Stalin (DMK)',
    icon: <Crown size={20} />,
    color: '#ff6b6b',
    dobInfo: '01.03.1953 - 19:05:00, Chennai',
    astrology: 'Lagna: Leo | Rasi: Leo | Star: Pooram-4 | Dasa: Saturn - Bhukti: Rahu - Antaram: Mercury',
    verdict: 'The Dasa-Bhukti alignment strongly points to a loss of the Chief Minister position but a transition into a highly powerful Leader of the Opposition. Saturn Dasa and Rahu Bhukti are in a 4/10 axis leading to resting rather than ruling. The ruling state (Leo Rasi) going through Ashtama Shani and transiting Ketu guarantees a change of leadership.',
    chartData: [
      'குரு\nசுக்#', // Aries 0
      '',             // Taurus 1
      '',             // Gemini 2
      '(கே)',          // Cancer 3
      'சந்',           // Leo 4 (Removed ல)
      '',             // Virgo 5
      '(சனி) மா',      // Libra 6
      '',             // Scorpio 7
      '',             // Sagittarius 8
      '(ரா+)',        // Capricorn 9
      'சூரி',          // Aquarius 10
      'செ புத'         // Pisces 11
    ],
    chartColors: {
      2: 'rgba(56, 189, 248, 0.4)', // Gemini Cyan
      6: 'rgba(168, 126, 126, 0.5)', // Libra Brown
      9: 'rgba(168, 126, 126, 0.5)'  // Capricorn Brown
    },
    positives: [
      'Bhukti lord Rahu in the 6th from Lagna and 10th of Kala Purusha (Capricorn) guarantees a firm legislative position, specifically the Opposition Leader.',
      'Rahu, though a Mudakku Graha, acts as a Yogi Graha for him, securing massive Islamic and minority votes keeping the defeat highly respectable.',
      'Transiting Saturn and Rahu in their own stars structurally reduces complete wipeout, granting a dignified number of seats despite the wave.',
      'Moving Lagna (Nagaram Lagna) reaches Aries, where exalted Saturn in 7th gains Digbala, granting strong mass support.',
      'Rahu in 10th from Moving Lagna ensures he remains a formidable, highly respected voice in the assembly.',
      'The strong foundation built during the early phase of exalted Saturn Dasa provides an unbreakable core vote bank.',
      'Transiting Sun allows for aggressive campaigning despite physical limitations.',
      'The Kala Purusha Guru-Sani mutual aspect continues to protect his legacy from total destruction.',
      'Mercury Antaram, though weak, will still activate certain loyal traditional bureaucratic channels.',
      'The 6th house Rahu connection ensures enemies cannot legally dismantle his family\'s core political grip.'
    ],
    negatives: [
      'Dasa lord Saturn and Bhukti lord Rahu are positioned in a 4/10 axis, indicating resting (Sukha Sthana) rather than active CM rule.',
      'Saturn is 6th from natal Saturn and Rahu is 12th from natal Rahu, rendering both unable to grant full executive power.',
      'Both Dasa and Bhukti lords reside in Thithi Shoonya Rasis, minimizing their ability to yield massive victories in old age.',
      'Rahu is in the 12th star from Janma Nakshatra, bringing severe political embarrassments and unwinnable situations.',
      'Lagna lord Sun is in Sathayam (Rahu\'s star) running Rahu Bhukti, triggering ancestral karma and governmental setbacks.',
      'Antaram lord Mercury is natal debilitated and transits Ashwini, turning government machinery and postal votes entirely against him.',
      'Transiting Jupiter is too far by degrees to beneficially aspect Saturn and Rahu, rendering it completely ineffective.',
      'Transiting Rahu is in 12th to transiting Saturn causing a total disconnect from the public pulse, leading to raw vote loss.',
      'Transiting Rahu over Lagna/Rasi lord Sun drastically drains physical stamina and mental fortitude.',
      'Transiting Ketu over Lagna and Rasi signals an inevitable loss of high office and deep personal grief.',
      'Transiting Mercury over Ashwini (Avayogi Venus\'s star) aggressively flips female voters against the DMK alliance.',
      'Age Lagna reaches Virgo; transiting Jupiter in the 10th from it mandates the stripping of current authoritative titles.',
      'Bhukti lord Rahu acts as a Mudakku Graha transiting over the Sun, intellectually cornering him.',
      'Ashtama Shani (8th House Saturn) signifies being severely misguided by closest aides leading to defeat.'
    ]
  },
  {
    id: 'eps',
    name: 'Edappadi K. Palaniswami (AIADMK)',
    icon: <Shield size={20} />,
    color: '#51cf66',
    dobInfo: '20.03.1954 - 10:33 AM, Edappadi',
    astrology: 'Lagna: Taurus | Rasi: Virgo | Star: Hastham-1 | Dasa: Mercury - Bhukti: Venus - Antaram: Rahu',
    verdict: 'A ferocious, victorious comeback powered by phenomenal Dasa dynamics. Transits and Navamsa alignments display supreme Raja Yogas triggering an Oath of Office. Complete astrological synchronization with the ADMK party chart confirms he will recapture and hold the Chief Minister post with overwhelming authority.',
    chartData: [
      '',          // Aries 0
      'ல',         // Taurus 1
      'கே குரு',    // Gemini 2
      '',          // Cancer 3
      '',          // Leo 4
      'சந்',       // Virgo 5
      'சனி(R)',    // Libra 6
      'செ',        // Scorpio 7
      'ரா',        // Sagittarius 8
      '',          // Capricorn 9
      'சுக்',       // Aquarius 10
      'சூரி புத'    // Pisces 11
    ],
    positives: [
      'Dasa lord Mercury in the 10th (Karma Sthana) running the 6th Dasa points directly to supreme executive authority.',
      'Transiting Rahu over Dasa lord Mercury structurally magnifies his power, position, and mass appeal.',
      'Bhukti lord Venus receives Adhi Yoga from Full Moon, is exalted conjunct Sun in Pisces, granting overwhelming governmental success.',
      'In Navamsa, Dasa lord Mercury, Bhukti lord Venus, and Antara lord Rahu all converge in the 9th from the Moon (Oath of Office Yoga).',
      'Transits are perfectly aligned: Saturn in 11th, Jupiter in 2nd, Rahu in 10th, Ketu in 4th create a flawless battlefield advantage.',
      'Transiting Saturn in Virgo\'s 7th house gains Digbala, translating to massive grass-root public backing.',
      'Transiting Jupiter aspects the Dasa lord Mercury with its 9th aspect, ensuring an immediate elevation of status and luck (Bhagya).',
      'Dasa lord Mercury operates as a Yogi Graha running its own Dasa, denoting uninterrupted central reign and vast economic growth.',
      'Perfect Astrological Synchronization with the ADMK chart (Taurus Lagna, Virgo influence), confirming he fully embodies the party\'s destiny.',
      'The party\'s Navamsa Lagna Mercury acts as EPS\'s Dasa lord running till 01.09.2038, projecting a very long, unshakeable tenure as Chief Minister.'
    ],
    negatives: [
      'Ketu transiting the 4th house generates localized real-estate or infrastructure-based rumors affecting certain specific district margins.',
      'Rahu in the 10th requires relentless physical touring, inherently threatening immense health exhaustion and vocal strain.',
      'Lack of a massive national alliance shield implies the absolute margin of victory heavily depends strictly on his personal charisma.',
      'TVK aggressively targets the exact same anti-establishment youth vote, potentially cannibalizing minor margins in deep urban pockets.',
      'Mercury running in Jyeshta-2 brings complex intra-party legal maneuvers that cause momentary media-based distractions.',
      'Financial squeezes dynamically trigger around mid-April affecting highly critical last-minute booth logistics.',
      'Sudden Election Commission scrutiny directly orchestrated by the fleeing ruling party machinery.',
      'Northern districts tightly held by DMK historically present a massive barrier that requires exorbitant campaign energy to dent.',
      'Minor cross-voting in specific allied camps during the final week of polling due to highly localized sub-caste grudges.',
      'Media narratives engineered by opposition IT cells will aggressively attempt to under-report the reality of his massive rural swell.'
    ]
  },
  {
    id: 'seeman',
    name: 'Seeman (NTK)',
    icon: <Users size={20} />,
    color: '#fcc419',
    dobInfo: '08.11.1966 - 06:15 AM, Sivagangai',
    astrology: 'Lagna: Scorpio | Rasi: Leo | Star: Purva Phalguni | Dasa: Jupiter - Bhukti: Venus',
    verdict: 'Despite triggering massive, organic crowd fervour and vastly expanding his overall state-wide vote share percentage, mathematical conversions evade him. Ashtama Shani and an unyielding Ketu prevent the tactical alliances required to win in a First-Past-The-Post system.',
    chartData: [
      'ரா', // Aries
      '', // Taurus
      '', // Gemini
      'குரு', // Cancer
      'சந்', // Leo
      '', // Virgo
      'சூரி சுக் கே', // Libra
      'ல புத செ', // Scorpio 
      '', // Sag
      '', // Cap
      '', // Aq
      'சனி' // Pisces
    ],
    positives: [
      'Jupiter Mahadasa brings unprecedented expansion of statewide vote share, cementing his ideological platform.',
      'Exalted Sun transit structurally elevates the party to a recognized institutional level.',
      'Mars Antaram fuels hyper-aggressive, viral campaign speeches that dominate the narrative.',
      'Saturn\'s aspect rewards die-hard grassroots loyalty spanning decades.',
      'Rahu in 7th from Moon commands organic, massive internet groundswells and social media supremacy.',
      'Venus Bhukti brings a surprising and much-needed influx of female demographic support.',
      'Mercury\'s brilliance ensures complete oratorical dominance in every political debate.',
      'Natal Moon in Leo provides immense, unyielding willpower despite continuous setbacks.',
      'Ketu\'s cult loyalty ensures his cadre cannot be bought, bribed, or intimidated by major parties.',
      'Independent transit aligns with the cultural anti-establishment nerve of the State perfectly.'
    ],
    negatives: [
      'Ashtama Shani represents the ultimate mathematical barrier, brutally blocking seat conversions.',
      'Ketu\'s isolation heavily enforces a stubborn refusal to form critical tactical alliances needed to win FPTP elections.',
      'Shocking pre-poll defections of long-standing district lieutenants due to Rahu in 7th.',
      'Direct demographic collision with Vijay (TVK) shatters his monopoly on the rebellious youth vote.',
      'Over-aggression in speeches alienates the neutral, peace-seeking, and elderly voting blocks.',
      'Severe state machinery oppression proactively restricts transport and campaign logistics.',
      'Deep financial struggles peaking dangerously in the final 48 hours of booth management.',
      'Result day anxiety as heartland seats slip away agonizingly by razor-thin margins.',
      'Intense judicial scrutiny and sudden police FIRs disrupting schedules.',
      'Mainstream media blackout forces total reliance on digital spaces which don\'t always vote.'
    ]
  },
  {
    id: 'vijay',
    name: 'Vijay (TVK)',
    icon: <TrendingUp size={20} />,
    color: '#339af0',
    dobInfo: '22.06.1974 - 12:00 PM, Chennai',
    astrology: 'Lagna: Leo | Rasi: Cancer | Star: Pushya | Dasa: Saturn - Bhukti: Mercury',
    verdict: 'An astonishing, logic-defying political debut. The exact transit of the Moon across his Janma Rasi on Voting Day triggers an uncontrollable emotional voting tsunami. While contesting 234 solo burns absolute majority chances, he lands as the ultimate kingmaker and supreme disruptor.',
    chartData: [
      '', // Aries
      'சுக் கே', // Taurus
      'சூரி சனி', // Gemini
      'சந் செ', // Cancer
      'ல', // Leo
      '', // Virgo
      '', // Libra
      'ரா', // Scorpio
      '', // Sagittarius
      '', // Capricorn
      'குரு', // Aquarius
      'புத' // Pisces
    ],
    positives: [
      'Transiting Moon exactly on Janma Rasi on voting day triggers an unstoppable emotional tsunami.',
      'Rahu in the 8th house completely detonates traditional Dravidian poll arithmetic making him the ultimate disruptor.',
      'Saturn in 9th (Destiny) officially inaugurates a long-term, structurally sound political dynasty.',
      'Jupiter in 12th base initiates massive global branding, funding, and philanthropic goodwill.',
      'Venus Antaram translates cinematic god-level charisma directly into impregnable political armor.',
      'Exalted Sun Raja Yoga on counting day instantly catapults him to kingmaker power-player status.',
      'Cold, data-driven candidate selection and ground-level strategy guided by Mercury Bhukti.',
      'Unprecedented female voter swing bypassing traditional party loyalties due to Venus resonance.',
      'Fearless solo-contesting violently validates his "lone wolf" appeal to the youth demographic.',
      '5th House transit on May 4th yields historic debut gains, outperforming all political analysts.'
    ],
    negatives: [
      'Slow onset of Sade Sati pressure brings massive physical exhaustion and harsh political reality-checks.',
      'Colossal, unrecoverable drain of immense personal wealth to fund 234 seats solo.',
      'Complete lack of cynical, battle-hardened local booth machinery compared to Dravidian majors.',
      'Unwittingly aids the ruling DMK party by splitting the anti-incumbency vote exactly in half.',
      'Star novelty decays rapidly when facing deeply entrenched rural village realities.',
      'Hesitation in deep agrarian strongholds strictly limits absolute statewide penetration.',
      'Solo arrogance makes crossing the 118 simple-majority line mathematically impossible on his first try.',
      'Heavy infiltration by seasoned, corrupt opportunists looking for a free wave to ride.',
      'Over-reliance on digital hype fails to convert to physical booth slips in the critical final 12 hours.',
      'Euphoric debut inevitably clashes with the harsh, dragging reality of sitting in the opposition.'
    ]
  },
  {
    id: 'annamalai' as CandidateId,
    name: 'K. Annamalai (BJP / NDA)',
    icon: <Shield size={20} />,
    color: '#ff9933',
    dobInfo: '04.06.1984 - 12:00 PM, Karur',
    astrology: 'Lagna: Aries | Rasi: Cancer | Star: Ashlesha | Dasa: Jupiter - Bhukti: Venus',
    verdict: 'Massive aggressive expansion of party machinery and polarizing crowd-pulling capabilities. However, translating this intense momentum into widespread seat conversions hits a harsh mathematical ceiling without a solidified Dravidian alliance.',
    chartData: ['','','','சந்','','','','','','','',''],
    positives: [
      'Transiting Jupiter in the 2nd house ensures massive influx of national financial backing.',
      'Exalted transit of Sun during election month supercharges his individual authoritative appeal.',
      'Strong natal Mars ensures relentless physical stamina and aggressive ground-level campaigning.',
      'Rahu transiting the 11th house brings unexpected, unorthodox alliances with minor regional players.',
      'Navamsa alignments strongly connect him directly to the central national leadership.',
      'Current Dasa lord Jupiter sits favourably, ensuring long-term institutional growth for the party.',
      'Saturn in the 11th house systematically rewards his highly disciplined, continuous padyatras.',
      'Venus Bhukti allows for a polished, highly visible corporate-style media presentation.',
      'Mercury\'s transit ensures hyper-reactive, sharp debating skills dismantling opponents.',
      'Ketu in the 6th ensures his immediate political enemies within the party are naturally neutralized.'
    ],
    negatives: [
      'Total lack of deep-rooted Dravidian arithmetic acts as an ultimate mathematical barricade.',
      'Sade Sati pressure brings instances of extreme physical exhaustion and unexpected roadblocks.',
      'Harsh planetary aspects on the 7th house make forming stable, trusting tactical alliances nearly impossible.',
      'Rahu\'s illusionary effects cause social media hype that fails to translate to actual rural booth slips.',
      'Over-aggression driven by Mars alienates the neutral, peace-seeking urban middle class.',
      'Transiting Saturn severely restricts his ability to penetrate the deep southern and delta agrarian belts.',
      'Sudden internal party mutinies triggered by Ketu alignments just weeks before the poll.',
      'Over-reliance on national leadership narratives fails to resonate with hyper-local constituency issues.',
      'Financial freezes in key constituencies during the critical last 48 hours.',
      'Result day reveals high vote-share but critically low actual MLA seat conversions.'
    ]
  },
  {
    id: 'ramadoss' as CandidateId,
    name: 'Anbumani Ramadoss (PMK)',
    icon: <Users size={20} />,
    color: '#ebba34',
    dobInfo: '09.10.1968 - 12:00 PM, Puducherry',
    astrology: 'Lagna: Scorpio | Rasi: Aries | Star: Ashwini | Dasa: Saturn - Bhukti: Jupiter',
    verdict: 'Maintains an absolute, unshakeable grip over the Northern belt\'s sub-caste arithmetic. He will play a ruthless and decisive bargaining role in alliance formations, securing a highly concentrated block of reliable seats.',
    chartData: ['சந்','','','','','','','','','','',''],
    positives: [
      'Saturn Dasa completely fortifies his traditional Northern Tamil Nadu strongholds.',
      'Jupiter Bhukti brings mature, diplomatic negotiation skills for securing maximum seats in alliances.',
      'Transiting Rahu acts exceptionally well in consolidating specific sub-caste demographic votes.',
      'Mars element ensures his cadre remains highly militant and intensely loyal.',
      'Navamsa placements guarantee a continuous generational transfer of absolute party control.',
      'The 5th house transit of Jupiter sparks highly intelligent, data-driven manifesto drafting.',
      'Sun\'s exalted transit provides strong bargaining power over both major Dravidian parties.',
      'Venus transit brings a momentary softening of his image among neutral urban voters.',
      'Mercury alignments ensure his core messaging remains extremely sharp and regionally focused.',
      'Ketu placement ensures absolute immunity from any internal party fragmentation.'
    ],
    negatives: [
      'Strict regional confinement entirely prevents any significant state-wide scaling or dominance.',
      'Ashtama Shani pressure brings intense friction and impossible demands from junior alliance partners.',
      'Rahu\'s transit restricts his maximum seat-ceiling, keeping him strictly as a regional kingmaker.',
      'Mars afflictions cause momentary lapses in diplomatic relations with national parties.',
      'Inability to penetrate the southern districts due to highly opposing astrological demographic alignments.',
      'Venus afflictions show a complete lack of appeal to first-time youth and floating women voters.',
      'Over-reliance on extremely specific caste-arithmetic makes his vote-bank rigid and predictable.',
      'Sudden financial drains caused by Saturn\'s slow movement in the 12th house axis.',
      'Media narratives consistently box him into regionalism due to Mercury\'s restrictive transits.',
      'Result day anxieties around narrow margins in semi-urban constituencies.'
    ]
  }
];

const SouthIndianChart = ({ data, title, color, cellColors = {} }: { data: string[], title: string, color: string, cellColors?: Record<number, string> }) => {
  const getStyle = (index: number) => ({
    background: cellColors[index] || 'var(--color-navy-light)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: '8px',
    fontSize: '0.9rem',
    fontWeight: 600,
    color: 'white',
    border: '1px solid var(--color-glass-border)',
    textAlign: 'center' as const,
    whiteSpace: 'pre-wrap' as const
  });

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gridTemplateRows: 'repeat(4, 1fr)', gap: '1px', background: 'rgba(255,255,255,0.1)', width: '100%', maxWidth: '380px', aspectRatio: '1', margin: '1rem auto', border: `2px solid ${color}`, borderRadius: '4px', overflow: 'hidden' }}>
      {/* Row 1: Pisces(11), Aries(0), Taurus(1), Gemini(2) */}
      <div style={getStyle(11)}>{data[11]}</div>
      <div style={getStyle(0)}>{data[0]}</div>
      <div style={getStyle(1)}>{data[1]}</div>
      <div style={getStyle(2)}>{data[2]}</div>
      
      {/* Row 2: Aquarius(10), Center, Center, Cancer(3) */}
      <div style={getStyle(10)}>{data[10]}</div>
      <div style={{ gridColumn: 'span 2', gridRow: 'span 2', background: 'var(--color-navy)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: 'var(--color-text)', border: '1px solid var(--color-glass-border)' }}>
        <div style={{ fontSize: '1.2rem', fontWeight: 700, color, marginBottom: '0.2rem', textAlign: 'center' }}>V1 Rasi Chart</div>
        <div style={{ fontSize: '0.8rem', color: 'var(--color-text-dim)', textAlign: 'center' }}>{title}</div>
      </div>
      <div style={getStyle(3)}>{data[3]}</div>
      
      {/* Row 3: Capricorn(9), Cancer(3 above), Leo(4) */}
      <div style={getStyle(9)}>{data[9]}</div>
      <div style={getStyle(4)}>{data[4]}</div>
      
      {/* Row 4: Sagittarius(8), Scorpio(7), Libra(6), Virgo(5) */}
      <div style={getStyle(8)}>{data[8]}</div>
      <div style={getStyle(7)}>{data[7]}</div>
      <div style={getStyle(6)}>{data[6]}</div>
      <div style={getStyle(5)}>{data[5]}</div>
    </div>
  );
};


const ElectionAnalysis: React.FC = () => {
  const [candidates, setCandidates] = useState<CandidateData[]>(initialCandidatesData);
  const [displayLimit, setDisplayLimit] = useState<number>(4);
  const [viewState, setViewState] = useState<'validation' | 'report'>('validation');
  const [editingId, setEditingId] = useState<CandidateId | null>(null);
  
  // Edit Form State
  const [editDobInfo, setEditDobInfo] = useState('');
  const [editAstrology, setEditAstrology] = useState('');

  const [selectedCandidateId, setSelectedCandidateId] = useState<CandidateId>('stalin');
  const [generatingPDF, setGeneratingPDF] = useState(false);
  const reportRef = useRef<HTMLDivElement>(null);

  const displayedCandidates = candidates.slice(0, displayLimit);
  const activeCandidate = displayedCandidates.find(c => c.id === selectedCandidateId) || displayedCandidates[0];

  const handleEditClick = (c: CandidateData) => {
    setEditingId(c.id);
    setEditDobInfo(c.dobInfo);
    setEditAstrology(c.astrology);
  };

  const handleSaveEdit = (c: CandidateData) => {
    setCandidates(prev => prev.map(cand => {
      if (cand.id === c.id) {
        return { ...cand, dobInfo: editDobInfo, astrology: editAstrology };
      }
      return cand;
    }));
    setEditingId(null);
  };

  const handleDownloadPDF = async () => {
    if (!reportRef.current) return;
    setGeneratingPDF(true);
    
    setTimeout(async () => {
      try {
        const canvas = await html2canvas(reportRef.current!, {
          scale: 2,
          backgroundColor: '#0D1B2A',
          logging: false,
          useCORS: true,
          windowWidth: reportRef.current!.scrollWidth,
          windowHeight: reportRef.current!.scrollHeight
        });
        
        const pdf = new jsPDF({
          orientation: 'portrait',
          unit: 'mm',
          format: 'a4'
        });

        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pageHeight = pdf.internal.pageSize.getHeight();
        const sections = reportRef.current!.querySelectorAll('.pdf-section');

        // Fill background of the very first page
        pdf.setFillColor(13, 27, 42); // Navy blue
        pdf.rect(0, 0, pdfWidth, pageHeight, 'F');

        let currentY = 15; // Strict top padding
        const marginX = 8; // Adjust margin
        const innerPdfWidth = pdfWidth - (marginX * 2);

        if (sections.length > 0) {
          for (let i = 0; i < sections.length; i++) {
            const section = sections[i] as HTMLElement;
            const canvas = await html2canvas(section, {
              scale: 2,
              backgroundColor: '#0D1B2A'
            });
            
            const imgData = canvas.toDataURL('image/png');
            const pdfImgHeight = (canvas.height * innerPdfWidth) / canvas.width;
            const isNewPageRequested = section.getAttribute('data-newpage') === "true";
            
            if (isNewPageRequested && i > 0 && currentY > 20) {
              pdf.addPage();
              pdf.setFillColor(13, 27, 42);
              pdf.rect(0, 0, pdfWidth, pageHeight, 'F');
              currentY = 15;
            } else if (currentY + pdfImgHeight > pageHeight - 15 && currentY > 20) {
              pdf.addPage();
              pdf.setFillColor(13, 27, 42);
              pdf.rect(0, 0, pdfWidth, pageHeight, 'F');
              currentY = 15;
            }
            
            if (pdfImgHeight > pageHeight - 20) {
              // Extremely long section fallback (rare)
              let heightLeft = pdfImgHeight;
              let position = currentY;

              pdf.addImage(imgData, 'PNG', marginX, position, innerPdfWidth, pdfImgHeight);
              heightLeft -= (pageHeight - position);

              while (heightLeft > 0) {
                position = heightLeft - pdfImgHeight;
                pdf.addPage();
                pdf.setFillColor(13, 27, 42);
                pdf.rect(0, 0, pdfWidth, pageHeight, 'F');
                pdf.addImage(imgData, 'PNG', marginX, position, innerPdfWidth, pdfImgHeight);
                heightLeft -= pageHeight;
              }
              currentY = pageHeight;
            } else {
              pdf.addImage(imgData, 'PNG', marginX, currentY, innerPdfWidth, pdfImgHeight);
              currentY += pdfImgHeight + 6;
            }
          }
        } else {
          // Fallback
          const canvas = await html2canvas(reportRef.current!, {
            scale: 2,
            backgroundColor: '#0D1B2A',
            windowWidth: reportRef.current!.scrollWidth,
            windowHeight: reportRef.current!.scrollHeight
          });
          
          const imgData = canvas.toDataURL('image/png');
          const pdfImgHeight = (canvas.height * innerPdfWidth) / canvas.width;
          let heightLeft = pdfImgHeight;
          let position = 10;

          pdf.addImage(imgData, 'PNG', marginX, position, innerPdfWidth, pdfImgHeight);
          heightLeft -= (pageHeight - position);

          while (heightLeft > 0) {
            position = heightLeft - pdfImgHeight;
            pdf.addPage();
            pdf.setFillColor(13, 27, 42);
            pdf.rect(0, 0, pdfWidth, pageHeight, 'F');
            pdf.addImage(imgData, 'PNG', marginX, position, innerPdfWidth, pdfImgHeight);
            heightLeft -= pageHeight;
          }
        }

        pdf.save(`JAMAKKAL_Election_Audit_2026_${selectedState}.pdf`);
      } catch (error) {
        console.error('Error generating PDF', error);
      } finally {
        setGeneratingPDF(false);
      }
    }, 100);
  };
  const [selectedState, setSelectedState] = useState<string>('');

  if (viewState === 'validation') {
    return (
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ padding: '1rem' }}>
        <h2 className="card-title text-gold" style={{ marginBottom: '1.5rem', textAlign: 'center', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.75rem' }}>
          <Info /> Validate Candidate Birth Details & Charts
        </h2>
        
        <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem', alignItems: 'center' }}>
           <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
             <strong className="text-gold" style={{ fontSize: '1.1rem' }}>Select State for Election Analysis:</strong>
             <select 
               value={selectedState} 
               onChange={(e) => setSelectedState(e.target.value)}
               style={{ padding: '10px 20px', background: 'rgba(255,255,255,0.05)', color: 'white', border: '1px solid var(--color-gold)', borderRadius: '8px', cursor: 'pointer', fontSize: '1.1rem', width: '250px' }}
             >
                <option value="">-- Select State --</option>
                <option value="tamilnadu">Tamil Nadu (2026)</option>
                <option value="kerala" disabled>Kerala (Coming Soon)</option>
                <option value="karnataka" disabled>Karnataka (Coming Soon)</option>
             </select>
           </div>

           {selectedState === 'tamilnadu' && (
             <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap', marginTop: '0.5rem', padding: '1rem', background: 'rgba(0,0,0,0.2)', borderRadius: '12px', border: '1px dashed rgba(255,255,255,0.1)' }}>
               <strong className="text-gold" style={{ fontSize: '1.1rem' }}>Select Dominant Candidates to Analyze:</strong>
               <select 
                 value={displayLimit} 
                 onChange={(e) => setDisplayLimit(Number(e.target.value))}
                 style={{ padding: '10px 20px', background: 'rgba(255,255,255,0.05)', color: 'white', border: '1px solid var(--color-gold)', borderRadius: '8px', cursor: 'pointer', fontSize: '1.1rem' }}
               >
                  <option value={2}>Top 2 Candidates (Bipolar Check)</option>
                  <option value={4}>Top 4 Candidates (Multi-Corner)</option>
                  <option value={6}>Top 6 Candidates (Full State Dynamics)</option>
               </select>
             </div>
           )}
        </div>

        {selectedState === 'tamilnadu' ? (
          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr)', gap: '2rem' }}>
            {displayedCandidates.map(cand => (
            <div key={cand.id} className="glass-panel" style={{ padding: '2rem', borderTop: `4px solid ${cand.color}` }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
                  <div style={{ flex: 1 }}>
                    <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: cand.color, marginBottom: '1rem', fontSize: '1.4rem' }}>
                      {cand.icon} {cand.name}
                    </h3>
                    
                    {editingId === cand.id ? (
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
                        <label>
                          DOB & Location:
                          <input value={editDobInfo} onChange={e => setEditDobInfo(e.target.value)} style={{ width: '100%', marginTop: '0.3rem', padding: '8px' }} />
                        </label>
                        <label>
                          Astrological Metrics:
                          <textarea 
                            value={editAstrology} 
                            onChange={e => setEditAstrology(e.target.value)} 
                            style={{ width: '100%', marginTop: '0.3rem', padding: '8px', minHeight: '60px', background: 'rgba(255,255,255,0.05)', color: 'white', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} 
                          />
                        </label>
                        <button onClick={() => handleSaveEdit(cand)} className="btn-primary" style={{ alignSelf: 'flex-start', marginTop: '0.5rem', padding: '8px 16px' }}>Save Changes</button>
                      </div>
                    ) : (
                      <div style={{ color: 'var(--color-text)', display: 'flex', flexDirection: 'column', gap: '0.5rem', lineHeight: '1.5' }}>
                        <div><strong>Birth Params:</strong> {cand.dobInfo}</div>
                        <div><strong>Astrology:</strong> <span style={{ color: 'var(--color-gold)' }}>{cand.astrology}</span></div>
                        
                        <button 
                          onClick={() => handleEditClick(cand)}
                          className="glass-panel"
                          style={{ padding: '8px 16px', marginTop: '1rem', border: '1px solid rgba(255,255,255,0.2)', color: 'white', cursor: 'pointer', display: 'flex', gap: '0.5rem', alignItems: 'center', width: 'fit-content' }}
                        >
                          <Edit3 size={16} /> Edit Data
                        </button>
                      </div>
                    )}
                  </div>

                  {/* Render Visual Rasi Chart */}
                  <div style={{ flex: '0 0 auto', width: '100%', maxWidth: '350px' }}>
                     <SouthIndianChart data={cand.chartData} title={cand.name} color={cand.color} cellColors={cand.chartColors} />
                  </div>

                </div>
              </div>
            </div>
          ))}
        </div>
        ) : (
          <div style={{ padding: '4rem 2rem', textAlign: 'center', color: 'var(--color-text-dim)', background: 'rgba(0,0,0,0.2)', borderRadius: '12px', border: '1px dashed rgba(255,255,255,0.1)' }}>
            Please select a deeply synthesized State from the dropdown menu to load specific political figures and astrological metrics.
          </div>
        )}

        {selectedState === 'tamilnadu' && (
          <div style={{ display: 'flex', justifyContent: 'center', marginTop: '3rem' }}>
            <button 
              onClick={() => setViewState('report')} 
              className="btn-primary" 
              style={{ fontSize: '1.2rem', padding: '16px 32px', display: 'flex', alignItems: 'center', gap: '1rem', boxShadow: '0 0 20px rgba(194, 151, 49, 0.4)' }}
            >
              <CheckCircle /> Confirm Validations & Generate Deep Analysis
            </button>
          </div>
        )}
      </motion.div>
    );
  }

  // REGULAR REPORT VIEW
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}
    >
      <div className="glass-panel" style={{ padding: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <button onClick={() => setViewState('validation')} className="glass-panel" style={{ padding: '6px 12px', border: 'none', cursor: 'pointer', color: 'var(--color-text-dim)', marginBottom: '1rem' }}>
            ← Back to Chart Validation
          </button>
          <h2 className="card-title text-gold" style={{ margin: 0 }}>
            <Star /> TN Election 2026 In-Depth Analysis
          </h2>
        </div>
        
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>

          <button 
            onClick={handleDownloadPDF} 
            className="btn-primary" 
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '10px 16px' }}
            disabled={generatingPDF}
          >
            <Download size={18} />
            {generatingPDF ? 'Generating PDF...' : 'Export Premium PDF'}
          </button>
        </div>
      </div>

      {/* PDF Export Container */}
      <div 
        ref={reportRef} 
        style={{ 
          background: 'var(--color-navy)', 
          borderRadius: '20px',
        }}
      >
        <div className="pdf-section" style={{ padding: '4.5rem 2.5rem', marginBottom: '2rem', border: '2px solid var(--color-gold)', borderRadius: '20px', background: 'radial-gradient(ellipse at center, rgba(13, 27, 42, 1) 0%, rgba(13, 27, 42, 1) 40%, rgba(194, 151, 49, 0.1) 100%)', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
           <h1 style={{ fontSize: '3rem', color: '#fcc419', textAlign: 'center', marginBottom: '2rem', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '1rem' }}>
             <Star size={40} /> Astrological Analysis - Final Audited Report
           </h1>
           <p style={{ textAlign: 'center', color: 'var(--color-text)', fontSize: '1.5rem', marginBottom: '2rem' }}>Comprehensive Astrological Audit - TN 2026 Legislative Assembly Elections</p>
           <div style={{ padding: '1rem 2rem', border: '1px solid var(--color-gold)', borderRadius: '12px', background: 'rgba(194, 151, 49, 0.1)', marginBottom: '3.5rem' }}>
             <p style={{ textAlign: 'center', color: 'var(--color-gold-light)', fontSize: '1.35rem', fontWeight: 'bold', margin: 0 }}>Astrological Analysis Executed by Rajagopal Kannan</p>
           </div>
           
           <div style={{ width: '100%', maxWidth: '900px', background: 'rgba(0,0,0,0.3)', padding: '2.5rem', borderRadius: '15px', border: '1px solid rgba(255,255,255,0.05)', boxShadow: '0 8px 32px 0 rgba(0,0,0,0.2)' }}>
              <h3 style={{ color: '#fcc419', fontSize: '1.6rem', marginBottom: '2rem', display: 'flex', alignItems: 'center', gap: '0.75rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '1rem' }}>
                <CheckCircle size={24} /> Analytical Methodology & Parameters
              </h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)', gap: '2rem' }}>
                <div>
                  <h4 style={{ color: '#51cf66', fontSize: '1.4rem', marginBottom: '1.2rem', letterSpacing: '0.5px' }}>Core Frameworks Consulted</h4>
                  <ul style={{ color: '#F8F9FA', fontSize: '1.25rem', lineHeight: '1.8', paddingLeft: '1.5rem' }}>
                    <li style={{ marginBottom: '0.8rem' }}><strong>Parashari Astrology:</strong> Foundational chart strength.</li>
                    <li style={{ marginBottom: '0.8rem' }}><strong>Jamakkal Prasna:</strong> Dynamic outcome probability.</li>
                    <li style={{ marginBottom: '0.8rem' }}><strong>Kala Purusha Thathwa:</strong> Macro state karmic directives.</li>
                    <li style={{ marginBottom: '0.8rem' }}><strong>Ashtakavarga:</strong> Mathematical strength of planetary transits.</li>
                  </ul>
                </div>
                <div>
                  <h4 style={{ color: '#339af0', fontSize: '1.4rem', marginBottom: '1.2rem', letterSpacing: '0.5px' }}>Key Evaluation Metrics</h4>
                  <ul style={{ color: '#F8F9FA', fontSize: '1.25rem', lineHeight: '1.8', paddingLeft: '1.5rem' }}>
                    <li style={{ marginBottom: '0.8rem' }}><strong>10th House:</strong> Executive Power & Governing Karma.</li>
                    <li style={{ marginBottom: '0.8rem' }}><strong>Nodal Axis (Rahu/Ketu):</strong> Volatility and disruptive shifts.</li>
                    <li style={{ marginBottom: '0.8rem' }}><strong>Dasa/Bhukti Alignment:</strong> Resonance with election dates.</li>
                    <li style={{ marginBottom: '0.8rem' }}><strong>Gochara (Transits):</strong> Influence on April 23 & May 4.</li>
                  </ul>
                </div>
              </div>
           </div>
        </div>

        {displayedCandidates.map(candidate => (
          <div key={candidate.id} style={{ marginBottom: '4rem' }}>
            <div className="pdf-section glass-panel" data-newpage="true" style={{ padding: '2.5rem', marginBottom: '1.5rem', border: `1px solid ${candidate.color}50`, boxShadow: `0 8px 32px 0 ${candidate.color}15`, background: 'var(--color-navy)' }}>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '1.5rem' }}>
              <div style={{ flex: 1 }}>
                <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', fontSize: '2.5rem', color: candidate.color, marginBottom: '0.5rem' }}>
                  {candidate.icon} {candidate.name}
                </h2>
                <div style={{ color: '#F8F9FA', fontSize: '1.35rem', display: 'grid', gridTemplateColumns: 'minmax(180px, auto) 1fr', gap: '1rem', marginTop: '1rem' }}>
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem' }}>
                    <Info size={20} style={{ marginTop: '0.2rem' }}/> <strong style={{ color: '#adb5bd' }}>DOB/Location:</strong>
                  </div>
                  <div style={{ lineHeight: '1.6' }}>{candidate.dobInfo}</div>
                  
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem' }}>
                    <Info size={20} style={{ marginTop: '0.2rem' }}/> <strong style={{ color: '#adb5bd' }}>Core Metrics:</strong>
                  </div>
                  <div style={{ color: '#fcc419', fontWeight: 600, lineHeight: '1.6' }}>{candidate.astrology}</div>
                </div>
              </div>
              <div style={{ width: '280px' }}>
                  <SouthIndianChart data={candidate.chartData} title="V1 Rasi Chart" color={candidate.color} cellColors={candidate.chartColors} />
              </div>
            </div>
            
            <div style={{ marginBottom: '1rem', background: 'rgba(0,0,0,0.3)', padding: '2rem', borderRadius: '12px', borderLeft: `5px solid ${candidate.color}`, boxShadow: '0 4px 15px rgba(0,0,0,0.2)' }}>
              <h3 style={{ fontSize: '1.6rem', color: 'var(--color-text)', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <ArrowRight size={22} color={candidate.color} /> Ultimate Astrological Verdict
              </h3>
              <ul style={{ paddingLeft: '2rem', color: '#F8F9FA', lineHeight: '2.0', fontSize: '1.6rem', fontWeight: 500, letterSpacing: '0.2px' }}>
                {candidate.verdict.split('. ').filter(Boolean).map((sentence, idx) => (
                   <li key={idx} style={{ marginBottom: '1.5rem' }}>{sentence.trim()}{sentence.endsWith('.') ? '' : '.'}</li>
                ))}
              </ul>
            </div>
            </div>

            <div className="pdf-section glass-panel" style={{ padding: '2.5rem', marginBottom: '1.5rem', border: '1px solid rgba(194,151,49,0.2)', background: 'var(--color-navy)' }}>
                <h3 style={{ color: '#fcc419', marginBottom: '2rem', fontSize: '1.6rem', display: 'flex', alignItems: 'center', gap: '0.5rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.8rem' }}>
                  Positive Astrological Drivers
                </h3>
                <ul style={{ paddingLeft: '1.8rem', color: '#F8F9FA', lineHeight: '1.7', fontSize: '1.5rem', fontWeight: 500, letterSpacing: '0.2px' }}>
                  {candidate.positives.map((point, idx) => (
                    <li key={idx} style={{ marginBottom: '2.2rem' }}>{point}</li>
                  ))}
                </ul>
            </div>
            <div className="pdf-section glass-panel" style={{ padding: '2.5rem', border: '1px solid rgba(255,107,107,0.2)', background: 'var(--color-navy)' }}>
                <h3 style={{ color: '#ff6b6b', marginBottom: '2rem', fontSize: '1.6rem', display: 'flex', alignItems: 'center', gap: '0.5rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.8rem' }}>
                  Negative Vulnerabilities
                </h3>
                <ul style={{ paddingLeft: '1.8rem', color: '#F8F9FA', lineHeight: '1.7', fontSize: '1.5rem', fontWeight: 500, letterSpacing: '0.2px' }}>
                  {candidate.negatives.map((point, idx) => (
                    <li key={idx} style={{ marginBottom: '2.2rem' }}>{point}</li>
                  ))}
                </ul>
            </div>
          </div>
        ))}

        <div className="pdf-section glass-panel" data-newpage="true" style={{ padding: '3.5rem 3.5rem 2rem 3.5rem', marginTop: '2rem', borderTop: '6px solid var(--color-gold)', borderRadius: '20px 20px 0 0', background: 'var(--color-navy)' }}>
          <h3 style={{ fontSize: '2.1rem', color: '#fcc419', marginBottom: '1.8rem', display: 'flex', alignItems: 'center', gap: '0.5rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '1.5rem' }}>
            <Crown /> Final Conclusion & Astrological Verdict
          </h3>
          <p style={{ lineHeight: '1.8', marginBottom: '2.5rem', color: '#F8F9FA', fontSize: '1.45rem', fontWeight: 500, letterSpacing: '0.2px' }}>
            The inclusion of specific date transits and the nodal axis (Rahu/Ketu) reveals that the 2026 Tamil Nadu Election is fundamentally an anti-establishment, chaotic disruption, mediated entirely by heavily fragmented voting.
          </p>
          
          <h4 style={{ fontSize: '1.7rem', color: '#fcc419', marginBottom: '1rem' }}>The Verdict on Both Dates</h4>
          <p style={{ lineHeight: '1.8', marginBottom: '2.5rem', color: '#F8F9FA', fontSize: '1.4rem', fontWeight: 500 }}>
            The Voting Date (April 23) leans phenomenally towards Vijay (TVK) and EPS (AIADMK), creating a massive early surge and an emotionally charged atmosphere. Conversely, Stalin and Seeman face massive internal and logistical friction on this day. The Counting Date (May 4) brings heavy panic and shockers for the ruling DMK, but an eventual begrudging hold on power. It triggers massive, history-making celebrations for TVK, and huge, validating comebacks for AIADMK.
          </p>

          <h4 style={{ fontSize: '1.7rem', color: '#fcc419', marginBottom: '1rem', marginTop: '2.5rem' }}>Astrological Seat Projection (Total: 234 Seats - Magic Number: 118)</h4>
          <p style={{ lineHeight: '1.8', marginBottom: '0', color: '#F8F9FA', fontSize: '1.4rem', fontWeight: 500 }}>
            The sheer disruption caused by Rahu in Aquarius and TVK's Janma Rasi Voting Day Transit ensures that no party will see a clean, unquestioned sweep. The vote is brutally fractured.
          </p>
        </div>

        <div className="pdf-section glass-panel" style={{ padding: '0 3.5rem', borderRadius: '0', background: 'var(--color-navy)' }}>
            <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', borderLeft: '5px solid #ff6b6b', marginBottom: '2rem', marginTop: '2rem' }}>
              <strong style={{ fontSize: '1.4rem', color: '#ff6b6b' }}>DMK Alliance (120 - 130 Seats):</strong>
              <p style={{ marginTop: '0.75rem', fontSize: '1.35rem', lineHeight: '1.8', color: '#F8F9FA' }}><strong>Verdict:</strong> Retains power, but heavily battered. Ketu on Stalin's Moon and the 4th house Counting Day Moon mean they win the required seats by razor-thin margins. It will be the most stressful victory of Stalin's career, heavily relying on the alliance's combined strength rather than an absolute DMK monopoly.</p>
            </div>
        </div>

        <div className="pdf-section glass-panel" style={{ padding: '0 3.5rem', borderRadius: '0', background: 'var(--color-navy)' }}>
            <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', borderLeft: '5px solid #51cf66', marginBottom: '2rem' }}>
              <strong style={{ fontSize: '1.4rem', color: '#51cf66' }}>AIADMK Front (80 - 90 Seats):</strong>
              <p style={{ marginTop: '0.75rem', fontSize: '1.35rem', lineHeight: '1.8', color: '#F8F9FA' }}><strong>Verdict:</strong> A ferocious comeback driven by EPS's 10th House Karma and Neecha Bhanga on counting day. They successfully absorb the anti-incumbency anger but fall short of absolute power largely because TVK cannibalizes their required youth swing votes. They become an overwhelmingly powerful opposition.</p>
            </div>
        </div>

        <div className="pdf-section glass-panel" style={{ padding: '0 3.5rem', borderRadius: '0', background: 'var(--color-navy)' }}>
            <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', borderLeft: '5px solid #339af0', marginBottom: '2rem' }}>
              <strong style={{ fontSize: '1.4rem', color: '#339af0' }}>TVK / Vijay (20 - 25 Seats):</strong>
              <p style={{ marginTop: '0.75rem', fontSize: '1.35rem', lineHeight: '1.8', color: '#F8F9FA' }}><strong>Verdict:</strong> Astrological History. The Janma Rasi transit on Voting Day ensures a legendary debut. While 234 solo contesting prevents a majority, securing 20+ seats on a debut marks TVK as the ultimate kingmaker and definitively announces Vijay as the inevitable future of Tamil Nadu politics.</p>
            </div>
        </div>

        <div className="pdf-section glass-panel" style={{ padding: '0 3.5rem 3.5rem 3.5rem', marginBottom: '2rem', borderRadius: '0 0 20px 20px', background: 'var(--color-navy)' }}>
            <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', borderLeft: '5px solid #fcc419' }}>
              <strong style={{ fontSize: '1.4rem', color: '#fcc419' }}>NTK / Seeman (0 - 2 Seats but ~10-12% Vote Share):</strong>
              <p style={{ marginTop: '0.75rem', fontSize: '1.35rem', lineHeight: '1.8', color: '#F8F9FA' }}><strong>Verdict:</strong> The tragic victim of the First-Past-The-Post (FPTP) voting system and Rahu/Ketu rigidness. Despite immense crowds and Jupiter's massive vote share expansion, Ketu's isolation prevents tactical alliances, and TVK steals the limelight. They remain an immense ideological force but lack legislative footprint.</p>
            </div>
        </div>

        <div className="pdf-section glass-panel" style={{ marginTop: '2rem', borderTop: '1px solid rgba(255,255,255,0.1)', padding: '3rem 2rem', textAlign: 'center', background: 'var(--color-navy)' }}>
          <div style={{ padding: '2rem', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.05)', marginBottom: '2rem' }}>
            <p style={{ color: 'var(--color-text-dim)', fontSize: '1.05rem', lineHeight: '1.8', fontStyle: 'italic' }}>
              <strong>Disclaimer:</strong> This astrological report is an automated algorithmic synthesis based on Jamakkal Prasna principles and provided birth parameters. Political outcomes are subject to divine will, collective karma, and free will. This is for research and entertainment purposes only.
            </p>
          </div>
          
          <div style={{ display: 'inline-block', padding: '1rem 2.5rem', background: 'rgba(28, 126, 68, 0.1)', border: '1px solid #1c7e44', borderRadius: '30px' }}>
             <strong style={{ color: '#51cf66', fontSize: '1.2rem', letterSpacing: '0.5px' }}>For Consultation : Contact by WhatsApp Rajagopal Kannan 98410 33514</strong>
          </div>
        </div>

      </div>
    </motion.div>
  );
};

export default ElectionAnalysis;
