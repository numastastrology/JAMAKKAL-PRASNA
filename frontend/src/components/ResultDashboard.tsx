import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FileDown, RefreshCw, Info, Award, Clock, Sparkles, Activity, Shield, Zap, Globe, Sun, Layers } from 'lucide-react';
import { downloadPDF } from '../api';
import type { PrasnaResponse } from '../types';

interface Props {
    result: PrasnaResponse;
    onReset: () => void;
    lang: string;
}

const formatDate = (dateStr: string | undefined) => {
    if (!dateStr) return "-";
    try {
        const date = new Date(dateStr);
        if (isNaN(date.getTime())) return dateStr;
        const d = String(date.getDate()).padStart(2, '0');
        const m = String(date.getMonth() + 1).padStart(2, '0');
        const y = date.getFullYear();
        return `${d}/${m}/${y}`;
    } catch (e) {
        return dateStr;
    }
};

const JamakkalChart: React.FC<{ result: PrasnaResponse }> = ({ result }) => {
    const zodiacs = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"];

    // Jamakkal Outer Planets (Jama Grahas) for border labels
    const outerLabels = Object.entries(result.jama_grahas || {}).map(([name, rasiNum]) => {
        const pName = name.replace('Jama ', '');
        const abbr = pName === 'Snake' ? 'SN' : pName.substring(0, 2).toUpperCase();
        return { abbr: 'J.' + abbr, rasiNum };
    });

    const getHouseNum = (rasiNum: number) => {
        const udRasi = result.inner_planets?.Udayam?.rasi_num || result.block || 1;
        return ((rasiNum - udRasi + 12) % 12) + 1;
    };

    const renderHouse = (zIdx: number) => {
        const rasiNum = zIdx + 1;
        const hNum = getHouseNum(rasiNum);
        const zodiac = zodiacs[zIdx];

        const transits = Object.entries(result.transits || {})
            .filter(([_, info]) => info.rasi_num === rasiNum)
            .map(([name, _]) => ({ name: name === 'Ascendant' ? 'ASC' : (name === 'Rahu' ? 'RA' : (name === 'Ketu' ? 'KE' : name.substring(0, 2).toUpperCase())), color: name === 'Ascendant' ? '#3B82F6' : '#10B981' }));

        const inner = Object.entries(result.inner_planets || {})
            .filter(([_, info]) => info.rasi_num === rasiNum)
            .map(([name, _]) => ({ name: name.substring(0, 2).toUpperCase(), color: '#EF4444' }));

        const jamas = Object.entries(result.jama_grahas || {})
            .filter(([_, h]) => h === rasiNum)
            .map(([name, _]) => {
                const parts = name.split(' ');
                const pName = parts[parts.length - 1];
                const abbr = pName === 'Snake' ? 'SN' : pName.substring(0, 2).toUpperCase();
                return { name: 'J.' + abbr, color: 'var(--color-gold)' };
            });

        const natal = Object.entries(result.natal?.Positions || {})
            .filter(([_, rasi]) => rasi === rasiNum)
            .map(([name, _]) => {
                let abbr = name === 'Mandhi' ? 'Ma' : (name === 'Mercury' ? 'Me' : name.substring(0, 2).toUpperCase());
                if (result.natal.PlanetaryStates?.[name] === 'Retrograde') abbr += '(R)';
                return { name: `(${abbr})`, color: 'var(--color-purple)' };
            });

        const isQueryBlock = result.block === hNum;

        return (
            <div key={zIdx} style={{
                border: isQueryBlock ? '2px solid var(--color-gold)' : '1px solid rgba(25, 45, 100, 0.15)',
                boxShadow: isQueryBlock ? 'inset 0 0 10px rgba(194, 151, 49, 0.1)' : 'none',
                background: isQueryBlock ? 'rgba(194,151,49,0.03)' : 'white',
                padding: '6px',
                position: 'relative',
                minHeight: '100px',
                display: 'flex',
                flexDirection: 'column',
                gap: '2px'
            }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', borderBottom: '1px solid #f1f5f9', marginBottom: '4px' }}>
                    <span style={{ fontSize: '0.6rem', color: '#64748b', fontWeight: 600 }}>{zodiac}</span>
                    <span style={{ fontSize: '0.6rem', color: '#3B82F6', opacity: 0.8, fontWeight: 700 }}>{hNum}</span>
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                    {inner.map(p => <span key={p.name} style={{ color: p.color, fontWeight: 800, fontSize: '0.8rem' }}>{p.name}</span>)}
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                    {transits.map(p => <span key={p.name} style={{ color: p.color, fontWeight: 700, fontSize: '0.75rem' }}>{p.name}</span>)}
                    {natal.map(p => <span key={p.name} style={{ color: p.color, fontWeight: 700, fontSize: '0.75rem' }}>{p.name}</span>)}
                </div>
                <div style={{ marginTop: 'auto', display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                    {jamas.map(p => <span key={p.name} style={{ color: p.color, fontSize: '0.65rem', fontWeight: 700 }}>{p.name}</span>)}
                </div>
            </div>
        );
    };

    const renderOuterLabels = (rasiNum: number, orientation: 'top' | 'bottom' | 'left' | 'right') => {
        const labels = outerLabels.filter(l => l.rasiNum === rasiNum);
        if (labels.length === 0) return null;

        const style: React.CSSProperties = {
            position: 'absolute',
            fontSize: '0.6rem',
            fontWeight: 800,
            color: 'var(--color-navy)',
            whiteSpace: 'nowrap',
            display: 'flex',
            gap: '5px'
        };

        if (orientation === 'top') { style.bottom = '100%'; style.left = '50%'; style.transform = 'translateX(-50%) translateY(-5px)'; }
        if (orientation === 'bottom') { style.top = '100%'; style.left = '50%'; style.transform = 'translateX(-50%) translateY(5px)'; }
        if (orientation === 'left') { style.right = '100%'; style.top = '50%'; style.transform = 'translateY(-50%) translateX(-5px) rotate(-90deg)'; }
        if (orientation === 'right') { style.left = '100%'; style.top = '50%'; style.transform = 'translateY(-50%) translateX(5px) rotate(90deg)'; }

        return <div style={style}>{labels.map(l => <div key={l.abbr}>{l.abbr}</div>)}</div>;
    };

    return (
        <div style={{ padding: '40px', background: 'white', borderRadius: '12px', border: '2px solid #3B82F6', position: 'relative' }}>
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(4, 1fr)',
                gridTemplateRows: 'repeat(4, 1fr)',
                gap: 0,
                border: '2px solid #1e293b',
                aspectRatio: '1/1',
                width: '100%',
                maxWidth: '500px',
                margin: '0 auto',
                background: '#f8fafc',
                position: 'relative'
            }}>
                {/* Top Row: 12, 1, 2, 3 (Pis, Ari, Tau, Gem) */}
                <div style={{ position: 'relative' }}>{renderHouse(11)} {renderOuterLabels(12, 'left')}</div>
                <div style={{ position: 'relative' }}>{renderHouse(0)} {renderOuterLabels(1, 'top')}</div>
                <div style={{ position: 'relative' }}>{renderHouse(1)} {renderOuterLabels(2, 'top')}</div>
                <div style={{ position: 'relative' }}>{renderHouse(2)} {renderOuterLabels(3, 'right')}</div>

                {/* Mid 1: 11, Data, 4 */}
                <div style={{ position: 'relative' }}>{renderHouse(10)} {renderOuterLabels(11, 'left')}</div>
                <div style={{ gridColumn: 'span 2', gridRow: 'span 2', padding: '10px', display: 'flex', flexDirection: 'column', justifyContent: 'center', textAlign: 'center', background: '#fff', border: '1px solid #cbd5e1', fontSize: '0.6rem' }}>
                    <div style={{ borderBottom: '1px solid #3B82F6', paddingBottom: '5px', marginBottom: '8px' }}>
                        <h4 style={{ margin: 0, color: '#1e293b', fontSize: '0.8rem', fontWeight: 800 }}>JAMAKKOL HORARY</h4>
                        <div style={{ color: '#3B82F6', fontWeight: 700 }}>
                            {formatDate(result.query_time_str)}
                        </div>
                    </div>
                    <p style={{ margin: '2px 0', fontSize: '0.65rem' }}>Jamam #{result.block || '-'} - Ruling: <b>{result.ruling_planet || '-'}</b></p>
                    <div style={{ marginTop: '5px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '5px', textAlign: 'left' }}>
                        <div style={{ borderRight: '1px solid #e2e8f0', paddingRight: '5px' }}>
                            {Object.entries(result.inner_planets || {}).map(([n, info]) => (
                                <div key={n} style={{ fontSize: '0.55rem' }}><b>{n.substring(0, 2).toUpperCase()}</b>: {info?.degree?.split(' ')[0] || '-'}</div>
                            ))}
                        </div>
                        <div style={{ paddingLeft: '2px' }}>
                            <div style={{ fontSize: '0.55rem' }}><b>SUN</b>: {result.transits?.Sun?.degree?.split(' ')[0] || '-'}</div>
                            <div style={{ fontSize: '0.55rem' }}><b>MOO</b>: {result.transits?.Moon?.degree?.split(' ')[0] || '-'}</div>
                            <div style={{ fontSize: '0.55rem' }}><b>RAH</b>: {result.transits?.Rahu?.degree?.split(' ')[0] || '-'}</div>
                            <div style={{ fontSize: '0.55rem' }}><b>KET</b>: {result.transits?.Ketu?.degree?.split(' ')[0] || '-'}</div>
                        </div>
                    </div>
                </div>
                <div style={{ position: 'relative' }}>{renderHouse(3)} {renderOuterLabels(4, 'right')}</div>

                {/* Mid 2: 10, 5 */}
                <div style={{ position: 'relative' }}>{renderHouse(9)} {renderOuterLabels(10, 'left')}</div>
                <div style={{ position: 'relative' }}>{renderHouse(4)} {renderOuterLabels(5, 'right')}</div>

                {/* Bottom Row: 9, 8, 7, 6 */}
                <div style={{ position: 'relative' }}>{renderHouse(8)} {renderOuterLabels(9, 'left')}</div>
                <div style={{ position: 'relative' }}>{renderHouse(7)} {renderOuterLabels(8, 'bottom')}</div>
                <div style={{ position: 'relative' }}>{renderHouse(6)} {renderOuterLabels(7, 'bottom')}</div>
                <div style={{ position: 'relative' }}>{renderHouse(5)} {renderOuterLabels(6, 'right')}</div>
            </div>
        </div>
    );
};

const ResultDashboard: React.FC<Props> = ({ result, onReset, lang }) => {
    const [downloading, setDownloading] = useState(false);

    const handleDownload = async () => {
        setDownloading(true);
        try {
            await downloadPDF(result);
        } catch (err) {
            console.error(err);
            alert('Error generating PDF.');
        } finally {
            setDownloading(false);
        }
    };

    const t = {
        en: {
            title: 'Professional Jamakkol Insights',
            rulingPlanet: 'Ruling Node',
            block: 'Jamam Block',
            panchanga: 'Panchanga Details',
            transits: 'Planetary Transits (Sidereal)',
            jamakkolPlanets: 'Jamakkol Inner/Outer Planets',
            diagnostics: '1. Diagnostic Analysis (Foundations)',
            recovery: '2. Recovery Timeline (Progression)',
            remedies: '3. Remedies & Guidance (Balance)',
            holistic: 'Holistic Forecast (Weighted)',
            download: 'Download Detailed PDF',
            reset: 'New Query',
            dayQuery: 'Day Time',
            nightQuery: 'Night Time'
        },
        ta: {
            title: 'தொழில்முறை ஜாமக்கோள் முடிவுகள்',
            rulingPlanet: 'ஆளும் அதிபதி',
            block: 'ஜாமக் கட்டம்',
            panchanga: 'பஞ்சாங்க விவரங்கள்',
            transits: 'கோசார நிலைகள்',
            jamakkolPlanets: 'ஜாமக்கோள் கிரகங்கள்',
            diagnostics: '1. கண்டறியும் ஆய்வு',
            recovery: '2. மீட்சி காலவரிசை',
            remedies: '3. பரிகாரங்கள் மற்றும் வழிகாட்டுதல்',
            holistic: 'முழுமையான முன்னறிவிப்பு',
            download: 'விரிவான அறிக்கையைப் பதிவிறக்கவும்',
            reset: 'புதிய வினவல்',
            dayQuery: 'பகல் நேரம்',
            nightQuery: 'இரவு நேரம்'
        }
    }[lang as 'en' | 'ta'];

    const renderList = (title: string, icon: React.ReactNode, points: string[] = []) => (
        <div style={{ marginBottom: '2.5rem' }}>
            <h3 className="card-title" style={{ borderBottom: '1px solid rgba(194,151,49,0.3)', paddingBottom: '0.5rem', marginBottom: '1.5rem' }}>
                {icon} {title}
            </h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '0.6rem' }}>
                {points.map((point, idx) => (
                    <motion.div
                        key={idx}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.1 + idx * 0.05 }}
                        style={{
                            padding: '0.8rem 1rem',
                            background: 'rgba(255,255,255,0.03)',
                            borderRadius: '8px',
                            borderLeft: '4px solid var(--color-gold)',
                            fontSize: '0.9rem',
                            display: 'flex',
                            gap: '1rem'
                        }}
                    >
                        <span style={{ fontWeight: 800, color: 'var(--color-gold)', minWidth: '20px' }}>{idx + 1}.</span>
                        <span style={{ color: 'var(--color-text)' }}>{point}</span>
                    </motion.div>
                ))}
            </div>
        </div>
    );

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            {/* Header & Main Stats */}
            <section className="glass-panel" style={{ padding: '2.5rem' }}>
                <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                    <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                            <h2 className="text-gold" style={{ fontSize: '2.4rem', margin: 0, letterSpacing: '-0.5px' }}>
                                {result.name || 'Professional Insights'}
                            </h2>
                            <span className="glass-panel" style={{ padding: '4px 12px', fontSize: '0.8rem', color: 'var(--color-gold)' }}>
                                {result.gender}
                            </span>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', marginTop: '0.75rem', opacity: 0.8 }}>
                            <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><Clock size={16} /> {formatDate(result.query_time_str)}</span>
                            <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><Globe size={16} /> Sidereal: {result.panchanga.SiderealTime}</span>
                        </div>
                    </div>
                    <div style={{ display: 'flex', gap: '1rem' }}>
                        <button onClick={handleDownload} className="btn-primary" disabled={downloading}>
                            <FileDown size={20} /> {downloading ? '...' : t.download}
                        </button>
                        <button onClick={onReset} className="glass-panel" style={{ padding: '10px', color: 'white', cursor: 'pointer', background: 'rgba(255,255,255,0.1)' }}>
                            <RefreshCw size={20} />
                        </button>
                    </div>
                </header>

                {result.query_text && (
                    <div className="glass-panel" style={{ padding: '1.2rem 1.5rem', borderLeft: '4px solid var(--color-gold)', background: 'rgba(194,151,49,0.05)', marginBottom: '3rem' }}>
                        <label style={{ fontSize: '0.7rem', textTransform: 'uppercase', color: 'var(--color-gold)', letterSpacing: '1px', marginBottom: '0.5rem', display: 'block' }}>Query Raised</label>
                        <p style={{ margin: 0, fontSize: '1.1rem', fontWeight: 500, fontStyle: 'italic', color: 'white' }}>"{result.query_text}"</p>
                    </div>
                )}

                <div className="grid-2" style={{ marginBottom: '3rem', gap: '2rem' }}>
                    <div style={{ flex: 1 }}>
                        <div className="grid-2" style={{ gap: '1rem', marginBottom: '1.5rem' }}>
                            <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center', border: '1px solid rgba(194,151,49,0.3)' }}>
                                <label style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--color-gold-dim)' }}>{t.rulingPlanet}</label>
                                <div style={{ fontSize: '2rem', fontWeight: 900, color: 'var(--color-gold)' }}>{result.ruling_planet}</div>
                            </div>
                            <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center' }}>
                                <label style={{ fontSize: '0.75rem', textTransform: 'uppercase' }}>{t.block}</label>
                                <div style={{ fontSize: '2rem', fontWeight: 900 }}>#{result.block}</div>
                            </div>
                        </div>
                        <div className="grid-2" style={{ gap: '1rem' }}>
                            <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center' }}>
                                <label style={{ fontSize: '0.75rem', textTransform: 'uppercase' }}>Time Lord</label>
                                <div style={{ fontSize: '1.8rem', fontWeight: 900 }}>{result.panchanga.Hora}</div>
                            </div>
                            <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center' }}>
                                <label style={{ fontSize: '0.75rem', textTransform: 'uppercase' }}>Lunar Phase</label>
                                <div style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '0.5rem' }}>{result.panchanga.Tithi}</div>
                            </div>
                        </div>
                    </div>
                    <div style={{ flex: 1 }}>
                        <JamakkalChart result={result} />
                    </div>
                </div>

                {/* Sub-Tables Grid */}
                <div style={{ display: 'grid', gridTemplateColumns: 'minmax(300px, 1fr) 2fr', gap: '2rem', marginBottom: '4rem' }}>
                    <div className="glass-panel" style={{ padding: '1.5rem', border: '1px solid rgba(255,255,255,0.1)' }}>
                        <h3 className="card-title" style={{ fontSize: '1.1rem' }}><Layers size={18} className="text-gold" /> {t.panchanga}</h3>
                        <div style={{ display: 'grid', gap: '1rem', marginTop: '1.5rem' }}>
                            {Object.entries(result.panchanga).map(([key, val]) => (
                                <div key={key} style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '0.5rem' }}>
                                    <span style={{ fontSize: '0.85rem', color: 'var(--color-text-dim)' }}>{key}</span>
                                    <span style={{ fontSize: '0.9rem', fontWeight: 600 }}>{val}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="glass-panel" style={{ padding: '1.5rem', border: '1px solid rgba(255,255,255,0.1)' }}>
                        <h3 className="card-title" style={{ fontSize: '1.1rem' }}><Sun size={18} className="text-gold" /> {t.transits}</h3>
                        <div style={{ overflowX: 'auto', marginTop: '1rem' }}>
                            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
                                <thead>
                                    <tr style={{ background: 'rgba(255,255,255,0.05)', textAlign: 'left' }}>
                                        <th style={{ padding: '0.75rem' }}>Planet</th>
                                        <th style={{ padding: '0.75rem' }}>Rasi</th>
                                        <th style={{ padding: '0.75rem' }}>Degree</th>
                                        <th style={{ padding: '0.75rem' }}>Nakshatra</th>
                                        <th style={{ padding: '0.75rem' }}>Lord</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {Object.entries(result.transits).map(([name, info]) => (
                                        <tr key={name} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                            <td style={{ padding: '0.75rem', fontWeight: 700, color: '#34d399' }}>{name}</td>
                                            <td style={{ padding: '0.75rem' }}>{info.rasi}</td>
                                            <td style={{ padding: '0.75rem', fontStyle: 'italic' }}>{info.degree}</td>
                                            <td style={{ padding: '0.75rem' }}>{info.nakshatra} ({info.pada})</td>
                                            <td style={{ padding: '0.75rem' }}>{info.star_lord}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* 2.5 Natal Profile Connection */}
                <div className="glass-panel" style={{ padding: '1.5rem', background: 'rgba(194,151,49,0.05)', border: '1px solid rgba(194,151,49,0.2)', marginBottom: '3rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem', marginBottom: '1.2rem' }}>
                        <Award size={20} className="text-gold" />
                        <h3 style={{ margin: 0, fontSize: '1.1rem', color: 'white' }}>Janma (Natal) Profile Synthesis</h3>
                    </div>
                    <div className="grid-4" style={{ gap: '1rem' }}>
                        <div style={{ textAlign: 'center' }}>
                            <label style={{ fontSize: '0.65rem' }}>Lagna (Ascendant)</label>
                            <div style={{ fontWeight: 700, color: 'var(--color-gold)' }}>{result.natal.Lagna}</div>
                        </div>
                        <div style={{ textAlign: 'center' }}>
                            <label style={{ fontSize: '0.65rem' }}>Birth Nakshatra</label>
                            <div style={{ fontWeight: 700, color: 'var(--color-gold)' }}>{result.natal.Nakshatra}</div>
                        </div>
                        <div style={{ textAlign: 'center' }}>
                            <label style={{ fontSize: '0.65rem' }}>Current Dasha</label>
                            <div style={{ fontWeight: 700, color: 'var(--color-gold)' }}>{result.natal.Dasha}</div>
                        </div>
                        <div style={{ textAlign: 'center' }}>
                            <label style={{ fontSize: '0.65rem' }}>Birth Place</label>
                            <div style={{ fontWeight: 700, color: 'var(--color-gold)', fontSize: '0.85rem' }}>{result.natal.birth_place || 'Not Specified'}</div>
                        </div>
                    </div>
                </div>

                {/* Main Analysis Sections */}
                {renderList(t.diagnostics, <Info size={22} className="text-gold" />, result.diagnostic_analysis)}
                {renderList(t.recovery, <Zap size={22} className="text-gold" />, result.recovery_timeline)}
                {renderList(t.remedies, <Shield size={22} className="text-gold" />, result.remedies)}

                {/* 4.5 Detailed Synthesis Breakdown (Horary Logic) */}
                <div style={{ marginTop: '3rem', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '2rem' }}>
                    {renderList("Detailed Synthesis Report (Horary Logic)", <Layers size={22} className="text-gold" />, result.synthesis_points)}

                    <div className="glass-panel" style={{
                        padding: '1.5rem',
                        background: 'rgba(59, 130, 246, 0.05)',
                        border: '1px solid rgba(59, 130, 246, 0.2)',
                        borderRadius: '12px',
                        marginBottom: '2rem'
                    }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem', marginBottom: '0.5rem' }}>
                            <Info size={18} className="text-blue-400" />
                            <h4 style={{ margin: 0, fontSize: '1rem', color: 'white', textTransform: 'uppercase' }}>Synthesis Conclusion</h4>
                        </div>
                        <p style={{ margin: 0, fontSize: '1.1rem', fontWeight: 500, color: 'rgba(255,255,255,0.9)', fontStyle: 'italic' }}>
                            {result.synthesis_conclusion}
                        </p>
                    </div>
                </div>

                {/* Final Guidance */}
                <div className="glass-panel" style={{ padding: '2rem', border: '2px solid var(--color-gold)', background: 'rgba(194,151,49,0.08)', marginTop: '2rem', textAlign: 'center' }}>
                    <h3 className="card-title" style={{ color: 'var(--color-gold-light)', fontSize: '1.4rem', justifyContent: 'center' }}><Sparkles size={24} /> Synthesis & Resolution</h3>
                    <p style={{ fontSize: '1.3rem', fontWeight: 600, color: 'white', lineHeight: '1.5', marginTop: '1rem' }}>
                        {result.final_conclusion}
                    </p>
                </div>

                {/* Holistic Categories */}
                <div style={{ marginTop: '4rem' }}>
                    <h3 className="card-title"><Activity size={22} className="text-gold" /> {t.holistic}</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', marginTop: '2rem' }}>
                        {Object.entries(result.balance_categories || {}).map(([cat, data], idx) => (
                            <motion.div
                                key={cat}
                                initial={{ opacity: 0, y: 30 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.1 + idx * 0.1 }}
                                className="glass-panel"
                                style={{
                                    padding: '2.5rem',
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    overflow: 'hidden'
                                }}
                            >
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
                                    <div style={{ flex: 1 }}>
                                        <h3 style={{ fontSize: '1.8rem', fontWeight: 700, color: 'white', marginBottom: '0.5rem' }}>{cat}</h3>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                            <div style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--color-gold)' }}>
                                                Score: {data.score.toFixed(1)} / 10 - {data.status}
                                            </div>
                                        </div>
                                    </div>
                                    <div style={{ width: '200px', textAlign: 'right' }}>
                                        <div style={{ height: '10px', background: 'rgba(255,255,255,0.1)', borderRadius: '5px', overflow: 'hidden', marginBottom: '0.5rem' }}>
                                            <motion.div
                                                initial={{ width: 0 }}
                                                animate={{ width: `${data.score * 10}%` }}
                                                style={{
                                                    height: '100%',
                                                    background: data.score > 7 ? '#34d399' : data.score > 4 ? 'var(--color-gold)' : '#f87171'
                                                }}
                                            />
                                        </div>
                                        <span style={{ fontSize: '0.8rem', color: 'var(--color-text-dim)', textTransform: 'uppercase' }}>Weighted Alignment</span>
                                    </div>
                                </div>

                                <div className="grid-2" style={{ gap: '2rem' }}>
                                    <div>
                                        <h4 style={{ color: '#f87171', fontSize: '1rem', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                            <Activity size={18} /> Challenges
                                        </h4>
                                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
                                            {(data.challenges || []).map((c, i) => (
                                                <div key={i} style={{ display: 'flex', gap: '0.8rem', fontSize: '0.95rem', color: 'rgba(255,255,255,0.85)' }}>
                                                    <span style={{ color: '#f87171', fontWeight: 800 }}>•</span>
                                                    <span>{c}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                    <div>
                                        <h4 style={{ color: '#34d399', fontSize: '1rem', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                            <Shield size={18} /> Pariharam & Solutions
                                        </h4>
                                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
                                            {(data.solutions || []).map((s, i) => (
                                                <div key={i} style={{ display: 'flex', gap: '0.8rem', fontSize: '0.95rem', color: 'rgba(255,255,255,0.85)' }}>
                                                    <span style={{ color: '#34d399', fontWeight: 800 }}>•</span>
                                                    <span>{s}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>
        </div>
    );
};

export default ResultDashboard;
