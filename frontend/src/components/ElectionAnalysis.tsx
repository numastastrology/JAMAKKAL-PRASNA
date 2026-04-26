import React, { useRef, useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, AlertTriangle, Star, Shield, Users, Crown, Download, Info, Edit3, CheckCircle, ArrowRight } from 'lucide-react';
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';

type CandidateId = 
  | 'stalin' | 'eps' | 'seeman' | 'vijay' | 'annamalai' | 'ramadoss'
  | 'mamata' | 'suvendu' | 'abhishek' | 'sukanta' | 'adhir' | 'salim';

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

const tnCandidatesData: CandidateData[] = [
  {
    id: 'stalin',
    name: 'M.K. Stalin (DMK)',
    icon: <Crown size={20} />,
    color: '#ff6b6b',
    dobInfo: '01.03.1953 - 19:05:00, Chennai',
    astrology: 'Lagna: Leo | Rasi: Leo | Star: Pooram-4 | Dasa: Saturn - Bhukti: Rahu - Antaram: Mercury',
    verdict: 'The Dasa-Bhukti alignment strongly points to a loss of the Chief Minister position but a transition into a highly powerful Leader of the Opposition. Saturn Dasa and Rahu Bhukti are in a 4/10 axis leading to resting rather than ruling. The ruling state (Leo Rasi) going through Ashtama Shani and transiting Ketu over the Janma Moon guarantees a change of leadership and a period of strategic detachment (Janma Ketu).',
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
      'Lagna lord Sun in Sathayam (Rahu\'s star) running Rahu Bhukti, triggering ancestral karma and governmental setbacks.',
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
    verdict: 'A ferocious, victorious comeback powered by phenomenal Dasa dynamics and favorable transits. Transiting Saturn in the 11th House (Labha Shani) and transiting Jupiter in the 1st House create a "Kingdom-Winning" yoga. Navamsa alignments display supreme Raja Yogas triggering an Oath of Office. Complete astrological synchronization with the ADMK party chart confirms he will recapture and hold the Chief Minister post with overwhelming authority.',
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
    verdict: 'Despite triggering massive, organic crowd fervour and vastly expanding his overall state-wide vote share percentage, mathematical conversions evade him. Ashtama Shani and an unyielding Ketu prevent the tactical alliances required to win in a winner-takes-all system.',
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
      'Ketu\'s isolation heavily enforces a stubborn refusal to form critical tactical alliances needed to win winner-takes-all elections.',
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
    id: 'annamalai',
    name: 'K. Annamalai (BJP / NDA)',
    icon: <Shield size={20} />,
    color: '#ff9933',
    dobInfo: '04.06.1984 - 12:00 PM, Karur',
    astrology: 'Lagna: Aries | Rasi: Cancer | Star: Ashlesha | Dasa: Jupiter - Bhukti: Venus',
    verdict: 'Massive aggressive expansion of party machinery and polarizing crowd-pulling capabilities. However, translating this intense momentum into widespread seat conversions hits a harsh mathematical ceiling without a solidified Dravidian alliance.',
    chartData: ['ல', 'சூரி புத சுக்', '', 'சந் மா', '', 'ரா', 'செ(R) சனி(R)', '', 'குரு(R)', '', '', 'கே'],
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
    id: 'ramadoss',
    name: 'Anbumani Ramadoss (PMK)',
    icon: <Users size={20} />,
    color: '#ebba34',
    dobInfo: '09.10.1968 - 12:00 PM, Puducherry',
    astrology: 'Lagna: Scorpio | Rasi: Aries | Star: Ashwini | Dasa: Saturn - Bhukti: Jupiter',
    verdict: 'Maintains an absolute, unshakeable grip over the Northern belt\'s sub-caste arithmetic. He will play a ruthless and decisive bargaining role in alliance formations, securing a highly concentrated block of reliable seats.',
    chartData: ['சந்', '', '', 'ரா', 'செ குரு', 'சூரி', 'புத(R) சுக் மா', 'ல', '', 'கே', '', 'சனி(R)'],
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

const wbCandidatesData: CandidateData[] = [
  {
    id: 'mamata',
    name: 'Mamata Banerjee (AITC)',
    icon: <Crown size={20} />,
    color: '#2e7d32',
    dobInfo: '05.01.1955 - 00:00:01, Kolkata',
    astrology: 'Lagna: Virgo | Rasi: Taurus | Star: Krittika-2 | Dasa: Jupiter - Bhukti: Rahu',
    verdict: 'The "Unyielding Empress of Bengal" faces her most complex astrological test. While Jupiter Dasa provides a protective umbrella of "Dharma-Ratha" (Chariot of Duty), the Rahu Bhukti in the 8th house from Dasa lord triggers intense internal subversion and bureaucratic hurdles. However, her Taurus Moon resilience remains unmatched, ensuring she retains the core of her kingdom through sheer emotional resonance with the grassroots electorate.',
    chartData: [
      'செ',          // Aries 0
      'சந்',         // Taurus 1
      'கே',          // Gemini 2
      'குரு(R)',     // Cancer 3
      '',            // Leo 4
      'ல',           // Virgo 5
      'சனி',         // Libra 6
      '',            // Scorpio 7
      'ரா',          // Sagittarius 8
      'சூரி புத',    // Capricorn 9
      'சுக்',        // Aquarius 10
      ''             // Pisces 11
    ],
    positives: [
      'Jupiter Dasa provides a "Maha Purusha" protective layer, keeping her public image as the "Protector of Bengal" intact.',
      'Exalted Moon (Rasi Lord) grants her an unshakeable emotional connection with rural female voters.',
      'Transiting Jupiter in the 1st House from Janma Rasi (Taurus) creates a powerful "Gaja-Kesari" effect on voting day.',
      'Saturn\'s transit in the 11th from Lagna (Labha Sthana) ensures structural stability and retention of key urban strongholds.',
      'Mercury (Lagna Lord) in the 5th house grants her sharp, reactive political instinct that outsmarts national narratives.',
      'Venus in the 6th ensures that despite intense legal and central agency pressure, no final "killing blow" can be dealt.',
      'Sun in the 5th house ensures her individual authoritative grip over the party machinery remains absolute.',
      'Navamsa placements show a strong "Raja Yoga" continuing through early 2027.',
      'Rahu in the 4th house (Matru Sthana) reinforces her "Didi" persona, making her the central mother figure of Bengal politics.',
      'Ketu in the 10th (Karmasthan) grants her a "Saintly Warrior" image that resonates with the traditional Bengali psyche.'
    ],
    negatives: [
      'Rahu Bhukti in the 8th from Dasa lord Jupiter indicates a "Snake in the Grass" scenario—internal betrayals by senior-most aides.',
      'Transiting Saturn in the 12th from Janma Rasi (Viraya Shani) triggers massive drains on state resources and administrative fatigue.',
      'Ketu transiting the 4th house from Lagna disrupts domestic peace and creates localized infrastructure-based anger.',
      'Sun-Mercury conjunction in the 5th (Natal) triggers impulsive decision-making under high-stakes pressure.',
      'Ashtakavarga strength of Mars is low during April, indicating physical exhaustion and health-related campaign breaks.',
      'Rahu\'s transit over the Natal Rahu position creates a "Karmic Reset" that demands shedding old, corrupt administrative skins.',
      'Severe demographic shift in the border districts due to Rahu-Ketu axis volatility affecting traditional vote banks.',
      'Jupiter\'s retrogression in the natal chart causes delayed implementation of key welfare schemes just before the poll.',
      'The "Sade Sati" tail-end pressure brings intense friction with the central judiciary and investigative bodies.',
      'Transiting Mars in the 7th house triggers aggressive, violent localized clashes that damage the "Peaceful Bengal" narrative.'
    ]
  },
  {
    id: 'suvendu',
    name: 'Suvendu Adhikari (BJP)',
    icon: <Shield size={20} />,
    color: '#ff9933',
    dobInfo: '15.12.1970 - 10:00:00, Tamluk',
    astrology: 'Lagna: Sagittarius | Rasi: Gemini | Star: Arudra | Dasa: Venus - Bhukti: Rahu',
    verdict: 'The "Ferocious Challenger" is currently in a hyper-active astrological phase. Venus Dasa (Lagna Lord of the BJP) running with Rahu Bhukti makes him a formidable, unpredictable force. His Gemini Rasi receives direct support from Saturn\'s transit, granting him the "Karma-Siddha" ability to dismantle entrenched strongholds. He will emerge as the undisputed alternative power center, significantly closing the gap with the incumbent.',
    chartData: [
      'சனி(R)',      // Aries 0
      '',             // Taurus 1
      'சந்',          // Gemini 2
      '',             // Cancer 3
      'கே',           // Leo 4
      '',             // Virgo 5
      '',             // Libra 6
      'சுக் குரு',     // Scorpio 7
      'ல சூரி புத',   // Sagittarius 8
      '',             // Capricorn 9
      'ரா',           // Aquarius 10
      'செ'            // Pisces 11
    ],
    positives: [
      'Dasa lord Venus in the 12th (Natal) running with Rahu Bhukti grants him "Asura-Gati" momentum—ruthless and highly effective tactics.',
      'Lagna lord Jupiter transiting the 6th house (Enemies) ensures he successfully dismantles the opposition\'s rural booths.',
      'Saturn in the 3rd from Lagna ( natal Aquarius) provides him with an unbreakable "Warrior Spirit" and physical stamina.',
      'Rahu in the 3rd (Natal) magnifying his communication skills, making his "anti-corruption" narrative viral across Bengal.',
      'Sun-Mercury in Lagna grants him the intellectual authority and command to lead a diverse alliance.',
      'Mars in the 4th house gives him a deep, aggressive grip over the "Bhoomiputra" (Son of the Soil) sentiment in Medinipur.',
      'Transiting Jupiter in Taurus (6th from Lagna) acts as a "Harsha Yoga" protector against legal hurdles.',
      'The exact degree-match of transiting Saturn with his natal Rahu triggers a "Breakout Event" in the North Bengal belt.',
      'Strong Navamsa alignments with the BJP party chart (Lotus Resonance) confirm him as the face of the challenge.',
      'Venus Bhukti ensures a massive influx of national strategic and financial resources at the exact right moment.'
    ],
    negatives: [
      'Rahu in the 6th (Transiting) creates "Maya" (Illusion)—he may overestimate his lead in certain minority-dominated pockets.',
      'Venus as the 6th and 11th lord in the 12th (Natal) indicates heavy personal expenditure and potential betrayal by "imported" aides.',
      'Ketu in the 12th from Lagna triggers sudden, unexpected tactical errors in the final 48 hours of polling.',
      'Sun\'s transit over the 5th house during April triggers ego-clashes with national leadership over candidate selection.',
      'Saturn\'s aspect on the 9th house (Bhagya) indicates that while he wins the battle, the "Crown" may still remain slightly out of reach.',
      'Mercury\'s debilitated transit in Pisces causes momentary confusion in the digital campaign narrative.',
      'Natal Saturn-Rahu conjunction in Aquarius brings "Ancestral Karma" that requires him to shed his previous political identity completely.',
      'Jupiter\'s transit in the 6th indicates intense friction with traditionalists within his own party.',
      'Mars in the 10th (Gochara) triggers aggressive central interventions that might cause a "Bengali Pride" backlash.',
      'The "Arudra" Nakshatra intensity makes him prone to polarizing statements that alienate neutral urban middle-class voters.'
    ]
  },
  {
    id: 'abhishek',
    name: 'Abhishek Banerjee (AITC)',
    icon: <Users size={20} />,
    color: '#00c853',
    dobInfo: '07.11.1987 - 11:30:00, Kolkata',
    astrology: 'Lagna: Sagittarius | Rasi: Taurus | Star: Krittika | Dasa: Rahu - Bhukti: Jupiter',
    verdict: 'The "Heir Apparent" is navigating a high-stakes Rahu Mahadasa. As the organizational backbone of the TMC, his Jupiter Bhukti provides the necessary "Bramha-Sthana" stability. However, the transit of Saturn in the 10th from Lagna (Virgo) indicates a period of extreme "Karma-Pariksha"—where every organizational move is scrutinized. He will be the primary target of opposition fire but will successfully maintain the party\'s organizational integrity.',
    chartData: [
      'குரு(R)',      // Aries 0
      'சந்',          // Taurus 1
      '',             // Gemini 2
      '',             // Cancer 3
      '',             // Leo 4
      'கே',           // Virgo 5
      'சூரி',         // Libra 6
      'ல செ புத சுக் சனி', // Scorpio 7
      '',             // Sagittarius 8
      '',             // Capricorn 9
      '',             // Aquarius 10
      'ரா'            // Pisces 11
    ],
    positives: [
      'Rahu Dasa in the 4th house (Natal) grants him modern, data-driven "Chanakya" style organizational control.',
      'Jupiter Bhukti in the 12th from Dasa lord (Natal) allows him to handle complex, hidden negotiations and alliances.',
      'Transiting Jupiter on Janma Rasi (Taurus) provides a "Protective Shield" during the heat of the campaign.',
      'Sun-Mercury-Mars conjunction in Scorpio (Natal) grants him intense, warrior-like focus and debating power.',
      'Venus in the 1st house (Natal) gives him a youthful, charismatic appeal that resonates with first-time voters.',
      'Saturn in the 12th from Lagna (Natal) rewards his long-term, behind-the-scenes organizational building.',
      'Mercury\'s transit in the 5th house during the poll fuels sharp, reactive social media strategies.',
      'The "Krittika" Nakshatra energy provides him with the "Cutting Edge" needed to dismantle opposition narratives.',
      'Strong 10th house (Natal) ensures he remains the undisputed successor and commander-in-chief of the ground forces.',
      'Ketu in the 10th (Natal) grants him an intuitive understanding of the rural Bengali power structure.'
    ],
    negatives: [
      'Transiting Saturn in the 10th (Gochara) from Lagna brings "Administrative Shackles" and extreme accountability pressure.',
      'Rahu in the 4th (Natal) triggers recurring controversies regarding "Matru-Bhumi" (Land) and local administration.',
      'Jupiter as the 1st and 4th lord in the 5th (Natal) indicates high risk to reputation through subordinates\' actions.',
      'Mars transit in the 4th house during April triggers aggressive, localized dissent in previously safe pockets.',
      'Venus-Saturn opposition in the natal chart creates friction with older, traditionalist elements of the party.',
      'Rahu\'s transit over the 4th house triggers sudden, disruptive legal interventions in family-linked entities.',
      'Ketu transiting the 10th house (Gochara) indicates a period of "Workplace Isolation" where he must lead alone.',
      'Mercury as the 7th and 10th lord in the 12th (Natal) indicates potential "Intellectual Burnout" under 24/7 pressure.',
      'Sun transiting the 8th from Natal Sun triggers health issues and stamina drains during the peak summer campaign.',
      'The "Ego-Planet" (Sun) in the 12th from Dasa Lord indicates momentary lapses in diplomatic relations with alliance partners.'
    ]
  },
  {
    id: 'sukanta',
    name: 'Sukanta Majumdar (BJP)',
    icon: <TrendingUp size={20} />,
    color: '#ff6d00',
    dobInfo: '29.12.1978 - 12:00:00, Balurghat',
    astrology: 'Lagna: Aquarius | Rasi: Sagittarius | Star: Moola | Dasa: Mercury - Bhukti: Jupiter',
    verdict: 'The "Intellectual Strategist" brings a "Saturnian" discipline to the BJP\'s Bengal unit. His Mercury Dasa is highly favorable for communication and structural growth. Transiting Jupiter in the 4th from Lagna (Taurus) provides him with the "Sukhada" (Giver of Comfort) energy to unite different factions. He will play the critical role of the "Bridge" between the national high command and the local grassroots.',
    chartData: [
      '',             // Aries 0
      '',             // Taurus 1
      '',             // Gemini 2
      'குரு(R)',      // Cancer 3
      'சனி ரா',       // Leo 4
      '',             // Virgo 5
      '',             // Libra 6
      'சுக்',         // Scorpio 7
      'ல சந் சூரி புத', // Sagittarius 8
      'செ',           // Capricorn 9
      'கே',           // Aquarius 10
      ''              // Pisces 11
    ],
    positives: [
      'Mercury Dasa (Lagna Lord of the BJP) acts as a "Sudarshana Chakra" for his political communication and strategy.',
      'Jupiter Bhukti in the 11th from Lagna (Natal) ensures he successfully gathers a diverse, intellectual support base.',
      'Transiting Saturn in Lagna (Natal Aquarius) grants him the "Sasa-Mahapurusha" Yoga—supreme authority and discipline.',
      'Mars in the 11th (Natal) ensures he has a highly dedicated, "militant" youth cadre at his command.',
      'Sun-Mercury in the 11th (Natal) grants him "Budha-Aditya" yoga, making him a sharp, respected intellectual voice.',
      'Venus in the 10th house (Natal) gives him a polished, respectable image that appeals to the urban Bengali middle class.',
      'Transiting Jupiter in the 4th (Gochara) aspects his 10th house, ensuring a "Karma-Siddhi" (Success in Work).',
      'The "Moola" Nakshatra energy allows him to dig deep into the "Root" causes of local issues, resonating with voters.',
      'Rahu in the 2nd (Natal) makes him a powerful, persuasive orator in the North Bengal belt.',
      'Ketu in the 8th (Natal) grants him the ability to handle hidden political crises with "detached" efficiency.'
    ],
    negatives: [
      'Transiting Rahu in the 2nd house (Gochara) triggers "Vak-Dosha"—potential for verbal slips that cause media controversies.',
      'Saturn\'s "Sade Sati" peak for Sagittarius Rasi indicates intense physical and mental pressure during the poll month.',
      'Ketu in the 8th (Natal) triggers sudden, unexpected internal mutinies in the North Bengal party unit.',
      'Sun transiting the 3rd house during April triggers aggressive opposition counter-attacks on his "academic" background.',
      'Mercury as the 5th and 8th lord in the 11th (Natal) indicates high dependency on "volatile" alliance partners.',
      'Mars transiting the 2nd house during voting day triggers aggressive, heated exchanges with local administrative officers.',
      'Natal Moon-Ketu proximity in Sagittarius triggers "Chandra-Grahana" effects—moments of deep uncertainty on results day.',
      'Venus as the 4th and 9th lord in the 10th (Natal) indicates that his "Goodness" might be used against him by more ruthless opponents.',
      'Jupiter\'s transit in the 4th house indicates heavy administrative workload that limits his time for personal campaigning.',
      'The "Intellectual" branding fails to penetrate the deepest, most "Emotional" pockets of South Bengal.'
    ]
  },
  {
    id: 'adhir',
    name: 'Adhir Ranjan Chowdhury (INC)',
    icon: <Users size={20} />,
    color: '#00b0ff',
    dobInfo: '02.04.1956 - 12:00:00, Berhampore',
    astrology: 'Lagna: Gemini | Rasi: Scorpio | Star: Jyeshta | Dasa: Saturn - Bhukti: Venus',
    verdict: 'The "Lion of Murshidabad" continues to fight a "Saturnian" battle of attrition. His Saturn Dasa is in its final phase, demanding extreme resilience. While his local fortress remains strong due to Mars resonance, the national alignment limits his state-wide expansion. He remains the critical "Swing Factor" in a polarized contest.',
    chartData: [
      'சூரி புத',     // Aries 0
      'சுக் கே',      // Taurus 1
      'ல',            // Gemini 2
      '',             // Cancer 3
      'குரு',         // Leo 4
      '',             // Virgo 5
      '',             // Libra 6
      'சந் சனி ரா',   // Scorpio 7
      'செ',           // Sagittarius 8
      '',             // Capricorn 9
      '',             // Aquarius 10
      ''              // Pisces 11
    ],
    positives: [
      'Saturn Dasa in the 6th from Lagna (Natal) grants him the "Shatru-Hanta" (Destroyer of Enemies) ability in his home turf.',
      'Mars in the 6th (Natal) ensures he remains a fierce, unyielding street fighter who commands personal loyalty.',
      'Transiting Jupiter in the 7th from Janma Rasi (Scorpio) provides a "Gaja-Kesari" support from unexpected quarters.',
      'Sun-Mercury in the 10th house (Natal) grants him the authority of a "People\'s Leader" in the Murshidabad-Malda belt.',
      'Venus in the 11th (Natal) ensures a dedicated, emotional core vote bank that transcends party lines.',
      'The "Jyeshta" Nakshatra energy grants him the "Seniority" and "Wisdom" to lead a complex alliance.',
      'Transiting Saturn in the 4th from Janma Rasi indicates a "Karmic" duty to protect his home base.',
      'Jupiter aspects his 10th house during the election month, granting him a "dignified" presence in the assembly.',
      'Rahu in the 12th (Natal) grants him the ability to handle "unconventional" and "hidden" political tactics.',
      'Mercury\'s transit in the 10th house (Gochara) fuels his sharp, "Bengali-rooted" political rhetoric.'
    ],
    negatives: [
      'Saturn Dasa reaching its "Chidra" (Final) phase indicates a period of "Endings" and transition.',
      'Rahu transiting the 10th house from Janma Rasi triggers "Karma-Bhrashta"—disruption of established power structures.',
      'Ketu in the 4th from Janma Rasi indicates a "Disconnect" from the younger, modernizing demographic of Bengal.',
      'Mars transit in the 5th from Janma Rasi triggers impulsive aggression that might alienate senior alliance partners.',
      'The "Sade Sati" tail-end for Scorpio Rasi brings intense physical exhaustion and localized administrative shocks.',
      'Venus in the 11th (Natal) is combusted by the Sun, indicating that while he has support, it may not translate to massive seats.',
      'Mercury in the 10th (Natal) is debilitated, causing momentary "communication gaps" with the national high command.',
      'Natal Saturn-Rahu-Ketu configuration creates a "Sarpa-Yoga" like pressure on his state-wide leadership.',
      'Jupiter\'s transit in the 12th from Lagna indicates high personal costs and "hidden" losses in suburban belts.',
      'The polarization between TMC and BJP leaves his "Middle Path" structurally vulnerable across 70% of the state.'
    ]
  },
  {
    id: 'salim',
    name: 'Mohammad Salim (CPIM)',
    icon: <Users size={20} />,
    color: '#d32f2f',
    dobInfo: '05.06.1957 - 12:00:00, Kolkata',
    astrology: 'Lagna: Leo | Rasi: Leo | Star: Pooram | Dasa: Saturn - Bhukti: Rahu',
    verdict: 'The "Resilient Ideologue" is leading the Left resurgence through a "Karmic" Saturn Dasa. His Leo Rasi (matching Stalin\'s) indicates a period of "Restructuring". While seat conversions remain a mathematical challenge, his astrological chart shows a significant "Ideological Victory"—regaining lost ground and respect in the urban industrial belts.',
    chartData: [
      'கே',           // Aries 0
      'சூரி புத',     // Taurus 1
      'செ சுக்',      // Gemini 2
      '',             // Cancer 3
      'ல சந் குரு',   // Leo 4
      '',             // Virgo 5
      'ரா',           // Libra 6
      'சனி(R)',       // Scorpio 7
      '',             // Sagittarius 8
      '',             // Capricorn 9
      '',             // Aquarius 10
      ''              // Pisces 11
    ],
    positives: [
      'Saturn Dasa in the 4th from Lagna (Natal) grants him deep, "Saturnian" organizational patience and persistence.',
      'Sun in the 10th house (Natal) grants him the authority of a "Principled Leader" and clear vision.',
      'Transiting Jupiter in the 10th from Lagna (Taurus) provides a "Karma-Siddhi" surge in his public appeal.',
      'Mars in the 11th (Natal) ensures he has a disciplined, "militant" cadre that is ready for the long fight.',
      'Mercury in the 10th (Natal) grants him sharp, analytical, and highly effective debating skills.',
      'Venus in the 11th (Natal) ensures a resurgence of support from the urban youth and intellectual circles.',
      'The "Pooram" Nakshatra energy gives him a "Charismatic Authority" that is grounded in cultural identity.',
      'Transiting Saturn in the 7th from Lagna (Natal Aquarius) grants him the power to form strong tactical alliances.',
      'Rahu in the 3rd (Natal) magnifying his communication reach through modern digital platforms.',
      'Ketu in the 9th (Natal) grants him a "detached" and "principled" image that contrasts with corrupt narratives.'
    ],
    negatives: [
      'Saturn Dasa in the 4th house indicates a "Slow Burn"—results take much longer to manifest than anticipated.',
      'Rahu transiting the 8th house from Janma Rasi triggers "Sudden Disruptions" and resource crunches.',
      'Ketu transiting the 2nd house (Gochara) triggers "Financial Restrictions" and logistical hurdles.',
      'Sun transiting the 9th house during April triggers friction with older, "conservative" elements of the party.',
      'Mars transit in the 8th from Janma Rasi triggers health issues and "burnout" during the peak campaign.',
      'The "Ashtama Shani" tail-end for Leo Rasi brings localized administrative shocks and narrow-margin losses.',
      'Venus as the 3rd and 10th lord in the 11th (Natal) indicates that gains are primarily "Inspirational" rather than "Numerical".',
      'Mercury in the 10th (Natal) is combusted by the Sun, indicating that his logic might be "overpowered" by emotional waves.',
      'Jupiter\'s transit in the 10th house indicates extreme accountability and a heavy administrative burden on his shoulders.',
      'The mathematical barrier of the TMC-BJP bipolarity remains the ultimate "Saturnian" wall for seat conversions.'
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
  const [selectedState, setSelectedState] = useState<string>('');
  const [candidates, setCandidates] = useState<CandidateData[]>([]);
  const [displayLimit, setDisplayLimit] = useState<number>(6);
  const [viewState, setViewState] = useState<'validation' | 'report'>('validation');
  const [editingId, setEditingId] = useState<CandidateId | null>(null);
  
  // Edit Form State
  const [editDobInfo, setEditDobInfo] = useState('');
  const [editAstrology, setEditAstrology] = useState('');

  const [selectedCandidateId, setSelectedCandidateId] = useState<CandidateId>('stalin');
  const [generatingPDF, setGeneratingPDF] = useState(false);
  const reportRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (selectedState === 'tamilnadu') {
      setCandidates(tnCandidatesData);
      setSelectedCandidateId('stalin');
    } else if (selectedState === 'westbengal') {
      setCandidates(wbCandidatesData);
      setSelectedCandidateId('mamata');
    } else {
      setCandidates([]);
    }
  }, [selectedState]);

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
            
            // Skip zero-height or invalid sections
            if (pdfImgHeight <= 0) continue;

            const isNewPageRequested = section.getAttribute('data-newpage') === "true";
            const isTall = pdfImgHeight > (pageHeight - 20);
            const fitsOnCurrentPage = (currentY + pdfImgHeight) < (pageHeight - 15);
            
            // Unified Pagination Logic
            if (isNewPageRequested && i > 0 && currentY > 25) {
              pdf.addPage();
              pdf.setFillColor(13, 27, 42);
              pdf.rect(0, 0, pdfWidth, pageHeight, 'F');
              currentY = 15;
            } else if (!isTall && !fitsOnCurrentPage && currentY > 25) {
              pdf.addPage();
              pdf.setFillColor(13, 27, 42);
              pdf.rect(0, 0, pdfWidth, pageHeight, 'F');
              currentY = 15;
            }
            
            if (isTall) {
              // Multi-page overflow logic
              let heightLeft = pdfImgHeight;
              let position = currentY;

              pdf.addImage(imgData, 'PNG', marginX, position, innerPdfWidth, pdfImgHeight);
              heightLeft -= (pageHeight - position);

              while (heightLeft > 0) {
                pdf.addPage();
                pdf.setFillColor(13, 27, 42);
                pdf.rect(0, 0, pdfWidth, pageHeight, 'F');
                position = heightLeft - pdfImgHeight;
                pdf.addImage(imgData, 'PNG', marginX, position, innerPdfWidth, pdfImgHeight);
                
                if (heightLeft < pageHeight) {
                  currentY = heightLeft + 15; 
                } else {
                  currentY = pageHeight;
                }
                heightLeft -= pageHeight;
              }
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

  const chunkArray = <T,>(arr: T[], size: number): T[][] => {
    return Array.from({ length: Math.ceil(arr.length / size) }, (v, i) =>
      arr.slice(i * size, i * size + size)
    );
  };

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
                <option value="westbengal">West Bengal (2026)</option>
                <option value="kerala" disabled>Kerala (Coming Soon)</option>
                <option value="karnataka" disabled>Karnataka (Coming Soon)</option>
             </select>
           </div>

           {selectedState && (
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

        {selectedState ? (
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

        {selectedState && (
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
            <Star /> {selectedState === 'tamilnadu' ? 'TN' : 'WB'} Election 2026 In-Depth Analysis
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
           <p style={{ textAlign: 'center', color: 'var(--color-text)', fontSize: '1.5rem', marginBottom: '2rem' }}>Comprehensive Astrological Audit - {selectedState === 'tamilnadu' ? 'TN' : 'WB'} 2026 Legislative Assembly Elections</p>
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
          <div key={candidate.id} style={{ marginBottom: '2rem' }}>
            {/* Candidate Header Section */}
            <div className="pdf-section glass-panel" data-newpage="true" style={{ padding: '2.5rem', marginBottom: '1rem', border: `1px solid ${candidate.color}50`, background: 'var(--color-navy)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '1.5rem' }}>
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
              
              <div style={{ background: 'rgba(0,0,0,0.3)', padding: '2rem', borderRadius: '12px', borderLeft: `5px solid ${candidate.color}` }}>
                <h3 style={{ fontSize: '1.6rem', color: 'var(--color-text)', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <ArrowRight size={22} color={candidate.color} /> Ultimate Astrological Verdict
                </h3>
                <ul style={{ paddingLeft: '2rem', color: '#F8F9FA', lineHeight: '2.0', fontSize: '1.6rem', fontWeight: 500 }}>
                  {candidate.verdict.split('. ').filter(Boolean).map((sentence, idx) => (
                     <li key={idx} style={{ marginBottom: '1.5rem' }}>{sentence.trim()}{sentence.endsWith('.') ? '' : '.'}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Chunked Positives */}
            {chunkArray(candidate.positives, 5).map((chunk, cIdx) => (
              <div key={`pos-${cIdx}`} className="pdf-section glass-panel" style={{ padding: '2.5rem', marginBottom: '1rem', border: '1px solid rgba(81, 207, 102, 0.2)', background: 'var(--color-navy)' }}>
                {cIdx === 0 && (
                  <h3 style={{ color: '#51cf66', marginBottom: '1.5rem', fontSize: '1.6rem', display: 'flex', alignItems: 'center', gap: '0.5rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.8rem' }}>
                    Positive Astrological Drivers
                  </h3>
                )}
                <ul style={{ paddingLeft: '1.8rem', color: '#F8F9FA', lineHeight: '1.7', fontSize: '1.5rem', fontWeight: 500 }}>
                  {chunk.map((point, idx) => (
                    <li key={idx} style={{ marginBottom: '1.8rem' }}>{point}</li>
                  ))}
                </ul>
              </div>
            ))}

            {/* Chunked Negatives */}
            {chunkArray(candidate.negatives, 5).map((chunk, cIdx) => (
              <div key={`neg-${cIdx}`} className="pdf-section glass-panel" style={{ padding: '2.5rem', marginBottom: '1rem', border: '1px solid rgba(255, 107, 107, 0.2)', background: 'var(--color-navy)' }}>
                {cIdx === 0 && (
                  <h3 style={{ color: '#ff6b6b', marginBottom: '1.5rem', fontSize: '1.6rem', display: 'flex', alignItems: 'center', gap: '0.5rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.8rem' }}>
                    Negative Vulnerabilities
                  </h3>
                )}
                <ul style={{ paddingLeft: '1.8rem', color: '#F8F9FA', lineHeight: '1.7', fontSize: '1.5rem', fontWeight: 500 }}>
                  {chunk.map((point, idx) => (
                    <li key={idx} style={{ marginBottom: '1.8rem' }}>{point}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        ))}

        {/* MATH SYNTHESIS FRAGMENT 1: TN/WB Primary Party 1 */}
        <div className="pdf-section glass-panel" data-newpage="true" style={{ padding: '3.5rem', marginBottom: '1rem', border: '1px solid rgba(194,151,49,0.3)', background: 'var(--color-navy)' }}>
          <h3 style={{ fontSize: '2.1rem', color: '#fcc419', marginBottom: '2rem', display: 'flex', alignItems: 'center', gap: '0.75rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '1.5rem' }}>
            <TrendingUp /> Mathematical Synthesis: {selectedState === 'tamilnadu' ? 'DMK Friction' : 'TMC Resurgence'} Logic
          </h3>
          <div style={{ background: selectedState === 'tamilnadu' ? 'rgba(255, 107, 107, 0.05)' : 'rgba(81, 207, 102, 0.05)', padding: '2.5rem', borderRadius: '15px', border: `1px solid ${selectedState === 'tamilnadu' ? 'rgba(255, 107, 107, 0.2)' : 'rgba(81, 207, 102, 0.2)'}` }}>
             <h4 style={{ color: selectedState === 'tamilnadu' ? '#ff6b6b' : '#51cf66', fontSize: '1.6rem', marginBottom: '1.2rem' }}>
               Why {selectedState === 'tamilnadu' ? '-25% Friction is given for DMK' : '+20% Resilience is given for TMC'}
             </h4>
             <p style={{ color: '#F8F9FA', fontSize: '1.25rem', marginBottom: '1.5rem', fontStyle: 'italic' }}>
               {selectedState === 'tamilnadu' 
                 ? 'The -25% is a cumulative "Nodal Squeeze" that forces the party from a potential sweep into a period of withdrawal.'
                 : 'The +20% is a "Gaja-Kesari Shield" that protects the incumbent from intense central narrative pressure.'}
             </p>
             <ul style={{ color: '#F8F9FA', fontSize: '1.25rem', lineHeight: '2', paddingLeft: '1.5rem' }}>
                {selectedState === 'tamilnadu' ? (
                  <>
                    <li style={{ marginBottom: '1.2rem' }}><strong>The Janma Ketu Impact (-10%):</strong> Transiting Ketu is positioned exactly on Stalin’s natal Moon (Janma Rasi). Astrologically, this creates a <strong>Frequency Disconnect</strong> between the leader and the public pulse.</li>
                    <li style={{ marginBottom: '1.2rem' }}><strong>The Ashtama Shani Factor (-10%):</strong> Saturn in the 8th house for Leo Rasi indicates "Sudden Disruption" and "Administrative Shocks," leading to a 10% loss in structural efficiency.</li>
                    <li style={{ marginBottom: '1.2rem' }}><strong>The 4th House Influence (-5%):</strong> The planetary alignment on May 4 focuses energy on "Resting" (Sukha) rather than "Ruling" (Karma).</li>
                  </>
                ) : (
                  <>
                    <li style={{ marginBottom: '1.2rem' }}><strong>The Jupiter-Moon Resonance (+10%):</strong> Transiting Jupiter in Taurus on voting day aspects the Rasi Lord, creating an unbreakable emotional bond with rural female voters.</li>
                    <li style={{ marginBottom: '1.2rem' }}><strong>The Labha Shani Stability (+5%):</strong> Saturn in the 11th from Lagna ensures that while narratives shift, the structural vote bank remains un-eroded in key urban sectors.</li>
                    <li style={{ marginBottom: '1.2rem' }}><strong>The Mercury Tactical Advantage (+5%):</strong> Strong Lagna Lord placement during the poll month grants the party a 5% "Narrative Edge" in digital and ground strategy.</li>
                  </>
                )}
             </ul>
             <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: `1px dashed ${selectedState === 'tamilnadu' ? 'rgba(255, 107, 107, 0.3)' : 'rgba(81, 207, 102, 0.3)'}`, fontWeight: 'bold', color: selectedState === 'tamilnadu' ? '#ff6b6b' : '#51cf66', fontSize: '1.3rem' }}>
               Total {selectedState === 'tamilnadu' ? 'Friction: -25% | Final Range: 95 - 105' : 'Resilience: +20% | Final Range: 145 - 155'} Seats.
             </div>
          </div>
        </div>

        {/* MATH SYNTHESIS FRAGMENT 2: TN/WB Primary Party 2 */}
        <div className="pdf-section glass-panel" style={{ padding: '3.5rem', marginBottom: '1rem', border: '1px solid rgba(194,151,49,0.3)', background: 'var(--color-navy)' }}>
          <h3 style={{ fontSize: '2.1rem', color: '#fcc419', marginBottom: '2rem', display: 'flex', alignItems: 'center', gap: '0.75rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '1.5rem' }}>
            <TrendingUp /> Mathematical Synthesis: {selectedState === 'tamilnadu' ? 'AIADMK Momentum' : 'BJP Bengal Surge'} Logic
          </h3>
          <div style={{ background: selectedState === 'tamilnadu' ? 'rgba(81, 207, 102, 0.05)' : 'rgba(255, 153, 51, 0.05)', padding: '2.5rem', borderRadius: '15px', border: `1px solid ${selectedState === 'tamilnadu' ? 'rgba(81, 207, 102, 0.2)' : 'rgba(255, 153, 51, 0.2)'}` }}>
             <h4 style={{ color: selectedState === 'tamilnadu' ? '#51cf66' : '#ff9933', fontSize: '1.6rem', marginBottom: '1.2rem' }}>
               Why {selectedState === 'tamilnadu' ? '+30% Momentum is given for AIADMK' : '+25% Breakthrough is given for BJP'}
             </h4>
             <p style={{ color: '#F8F9FA', fontSize: '1.25rem', marginBottom: '1.5rem', fontStyle: 'italic' }}>
               {selectedState === 'tamilnadu'
                 ? 'The +30% is a "Triple-Engine Yoga" that fuels a late-stage surge across rural belts.'
                 : 'The +25% is a "Karmic Breakthrough" that allows the challenger to breach previously impenetrable rural bastions.'}
             </p>
             <ul style={{ color: '#F8F9FA', fontSize: '1.25rem', lineHeight: '2', paddingLeft: '1.5rem' }}>
                {selectedState === 'tamilnadu' ? (
                  <>
                    <li style={{ marginBottom: '1.2rem' }}><strong>The Labha Shani Engine (+15%):</strong> Saturn transiting the 11th House (Pisces) is the **Yuddha Bhaga** multiplier, converting narrow-loss seats into narrow-win seats.</li>
                    <li style={{ marginBottom: '1.2rem' }}><strong>The Janma Guru (Jupiter) Aura (+10%):</strong> Transiting Jupiter on Lagna creates a "Protective Shield" and attracts floating voters.</li>
                    <li style={{ marginBottom: '1.2rem' }}><strong>The Neecha Bhanga Multiplier (+5%):</strong> Planetary cancellation of debilitation triggers a "Last-Minute Surge" in the final 5 rounds of counting.</li>
                  </>
                ) : (
                  <>
                    <li style={{ marginBottom: '1.2rem' }}><strong>The Rahu-Venus Momentum (+12%):</strong> Challenger leadership running Rahu Bhukti creates a "Disruptive Wave" that shatters established poll arithmetic.</li>
                    <li style={{ marginBottom: '1.2rem' }}><strong>The 3rd House Saturn Strength (+8%):</strong> Saturn\'s transit provides the necessary "Street Power" and cadre stamina to dominate booth management in North Bengal.</li>
                    <li style={{ marginBottom: '1.2rem' }}><strong>The Navamsa Raja Yoga (+5%):</strong> Alignment with the national party chart ensures maximum synchronization of resources and messaging.</li>
                  </>
                )}
             </ul>
             <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: `1px dashed ${selectedState === 'tamilnadu' ? 'rgba(81, 207, 102, 0.3)' : 'rgba(255, 153, 51, 0.3)'}`, fontWeight: 'bold', color: selectedState === 'tamilnadu' ? '#51cf66' : '#ff9933', fontSize: '1.3rem' }}>
               Total {selectedState === 'tamilnadu' ? 'Momentum: +30% | Final Range: 118 - 125' : 'Breakthrough: +25% | Final Range: 105 - 115'} Seats.
             </div>
          </div>
        </div>

        {/* FINAL VERDICT ATOMIC SECTIONS */}
        <div className="pdf-section glass-panel" data-newpage="true" style={{ padding: '3.5rem', marginBottom: '1rem', borderTop: '6px solid var(--color-gold)', background: 'var(--color-navy)' }}>
          <h3 style={{ fontSize: '2.1rem', color: '#fcc419', marginBottom: '1.8rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '1.5rem' }}>
            <Crown /> Final Conclusion & Astrological Verdict
          </h3>
          <p style={{ lineHeight: '1.8', color: '#F8F9FA', fontSize: '1.45rem', fontWeight: 500 }}>
            {selectedState === 'tamilnadu' 
              ? 'The 2026 Tamil Nadu Election is fundamentally an anti-establishment, chaotic disruption, mediated by heavily fragmented voting.'
              : 'The 2026 West Bengal Election is a Titan\'s Clash between incumbency resilience and a ferocious challenger wave, defined by intense emotional polarization.'}
          </p>
        </div>

        <div className="pdf-section glass-panel" style={{ padding: '2.5rem 3.5rem', marginBottom: '1rem', background: 'var(--color-navy)' }}>
          <h4 style={{ fontSize: '1.7rem', color: '#fcc419', marginBottom: '1rem' }}>{selectedState === 'tamilnadu' ? 'The Verdict on Both Dates' : 'The Verdict on Election Phases'}</h4>
          <p style={{ lineHeight: '1.8', color: '#F8F9FA', fontSize: '1.4rem', fontWeight: 500 }}>
            {selectedState === 'tamilnadu' 
              ? 'April 23 favors TVK and AIADMK (anti-establishment wave). May 4 brings "Labha Shani" results for EPS, triggering an Oath of Office, while the Ketu-Janma influence forces the DMK into strategic withdrawal as the opposition.'
              : 'April 23 and 29 phases show intense planetary friction. May 4 results day highlights "Gaja-Kesari" protection for the incumbent but significant "Labha Shani" breakthroughs for the challenger in urban zones.'}
          </p>
        </div>

        <div className="pdf-section glass-panel" style={{ padding: '2.5rem 3.5rem', marginBottom: '1rem', background: 'var(--color-navy)' }}>
          <h4 style={{ fontSize: '1.7rem', color: '#fcc419', marginBottom: '1rem' }}>Astrological Seat Projection (Total: {selectedState === 'tamilnadu' ? '234' : '294'})</h4>
          <p style={{ lineHeight: '1.8', color: '#F8F9FA', fontSize: '1.4rem', fontWeight: 500 }}>
            {selectedState === 'tamilnadu'
              ? 'The disruption caused by Rahu in Aquarius and TVK\'s Janma Rasi Voting Day Transit ensures a brutally fractured vote.'
              : 'The "Resilience Factor" of the Taurus Moon incumbent vs the "Breakthrough Karma" of the Gemini Rasi challenger ensures a high-voltage, narrow-margin outcome.'}
          </p>
        </div>

        {/* PARTY BRACKETS AS ATOMIC SECTIONS */}
        {selectedState === 'tamilnadu' ? (
          <>
            <div className="pdf-section glass-panel" style={{ padding: '2rem 3.5rem', background: 'var(--color-navy)' }}>
                <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', borderLeft: '5px solid #ff6b6b' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ fontSize: '1.4rem', color: '#ff6b6b' }}>DMK Alliance (95 - 105 Seats)</strong>
                    <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#ff6b6b' }}>Proj. Vote Share: ~35.5%</span>
                  </div>
                  <p style={{ marginTop: '0.75rem', fontSize: '1.35rem', lineHeight: '1.6', color: '#F8F9FA' }}>Transitions to Opposition. Ketu-Janma creates a net loss of critical seats in northern/urban belts.</p>
                </div>
            </div>

            <div className="pdf-section glass-panel" style={{ padding: '2rem 3.5rem', background: 'var(--color-navy)' }}>
                <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', borderLeft: '5px solid #51cf66' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ fontSize: '1.4rem', color: '#51cf66' }}>AIADMK Front (118 - 125 Seats)</strong>
                    <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#51cf66' }}>Proj. Vote Share: ~36.5%</span>
                  </div>
                  <p style={{ marginTop: '0.75rem', fontSize: '1.35rem', lineHeight: '1.6', color: '#F8F9FA' }}>Returns to Power. Labha Shani influence on counting day ensures a narrow but clear CM post victory.</p>
                </div>
            </div>

            <div className="pdf-section glass-panel" style={{ padding: '2rem 3.5rem', background: 'var(--color-navy)' }}>
                <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', borderLeft: '5px solid #339af0' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ fontSize: '1.4rem', color: '#339af0' }}>TVK / Vijay (20 - 25 Seats)</strong>
                    <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#339af0' }}>Proj. Vote Share: ~14.0%</span>
                  </div>
                  <p style={{ marginTop: '0.75rem', fontSize: '1.35rem', lineHeight: '1.6', color: '#F8F9FA' }}>The Kingmaker. Unprecedented 20+ debut marks Vijay as the inevitable future of TN politics.</p>
                </div>
            </div>

            <div className="pdf-section glass-panel" style={{ padding: '2rem 3.5rem', background: 'var(--color-navy)' }}>
                <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', borderLeft: '5px solid #fcc419' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ fontSize: '1.4rem', color: '#fcc419' }}>NTK / Seeman (0 - 2 Seats)</strong>
                    <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#fcc419' }}>Proj. Vote Share: ~7.5%</span>
                  </div>
                  <p style={{ marginTop: '0.75rem', fontSize: '1.35rem', lineHeight: '1.6', color: '#F8F9FA' }}>Ideological Force. Tragic victim of winner-takes-all voting and Ketu isolation preventing tactical alliances.</p>
                </div>
            </div>

            <div className="pdf-section glass-panel" style={{ padding: '2rem 3.5rem 4rem 3.5rem', borderRadius: '0 0 20px 20px', background: 'var(--color-navy)' }}>
                <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', borderLeft: '5px solid #ff9933' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ fontSize: '1.4rem', color: '#ff9933' }}>NDA / Others (0 - 2 Seats)</strong>
                    <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#ff9933' }}>Proj. Vote Share: ~4.0%</span>
                  </div>
                  <p style={{ marginTop: '0.75rem', fontSize: '1.35rem', lineHeight: '1.6', color: '#F8F9FA' }}>Stagnated Growth. Lack of a massive Dravidian shield prevents seat conversion despite aggressive campaigning.</p>
                </div>
            </div>
          </>
        ) : (
          <>
            <div className="pdf-section glass-panel" style={{ padding: '2rem 3.5rem', background: 'var(--color-navy)' }}>
                <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', borderLeft: '5px solid #2e7d32' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ fontSize: '1.4rem', color: '#2e7d32' }}>TMC Alliance (145 - 155 Seats)</strong>
                    <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#2e7d32' }}>Proj. Vote Share: ~45.0%</span>
                  </div>
                  <p style={{ marginTop: '0.75rem', fontSize: '1.35rem', lineHeight: '1.6', color: '#F8F9FA' }}>Retains Power. "Didi's Resilience" and Gaja-Kesari protection ensure a slim but clear majority victory.</p>
                </div>
            </div>

            <div className="pdf-section glass-panel" style={{ padding: '2rem 3.5rem', background: 'var(--color-navy)' }}>
                <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', borderLeft: '5px solid #ff9933' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ fontSize: '1.4rem', color: '#ff9933' }}>BJP Bengal (105 - 115 Seats)</strong>
                    <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#ff9933' }}>Proj. Vote Share: ~39.5%</span>
                  </div>
                  <p style={{ marginTop: '0.75rem', fontSize: '1.35rem', lineHeight: '1.6', color: '#F8F9FA' }}>Formidable Opposition. Rahu-Venus momentum shatters previous records but falls short of the magic figure.</p>
                </div>
            </div>

            <div className="pdf-section glass-panel" style={{ padding: '2rem 3.5rem', background: 'var(--color-navy)' }}>
                <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', borderLeft: '5px solid #00b0ff' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ fontSize: '1.4rem', color: '#00b0ff' }}>Left-Congress Front (15 - 20 Seats)</strong>
                    <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#00b0ff' }}>Proj. Vote Share: ~10.5%</span>
                  </div>
                  <p style={{ marginTop: '0.75rem', fontSize: '1.35rem', lineHeight: '1.6', color: '#F8F9FA' }}>Ideological Resistance. Regains ground in Murshidabad and urban industrial belts through Saturnian persistence.</p>
                </div>
            </div>

            <div className="pdf-section glass-panel" style={{ padding: '2rem 3.5rem 4rem 3.5rem', borderRadius: '0 0 20px 20px', background: 'var(--color-navy)' }}>
                <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', borderLeft: '5px solid #adb5bd' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ fontSize: '1.4rem', color: '#adb5bd' }}>Others / ISF (2 - 5 Seats)</strong>
                    <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#adb5bd' }}>Proj. Vote Share: ~5.0%</span>
                  </div>
                  <p style={{ marginTop: '0.75rem', fontSize: '1.35rem', lineHeight: '1.6', color: '#F8F9FA' }}>Localized Pockets. Influence remains restricted to specific sub-regional demographics.</p>
                </div>
            </div>
          </>
        )}

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
