import React, { useState } from 'react';
import { MapPin, Calendar, Clock, Send, Star, RefreshCw, Save, Trash2, UserCircle } from 'lucide-react';
import { calculatePrasna } from '../api';
import type { PrasnaResponse } from '../types';

interface Profile {
    id: string;
    name: string;
    gender: string;
    birth_date: string;
    birth_time: string;
    birth_place: string;
    lat: number;
    lon: number;
}

interface Props {
    onResult: (res: PrasnaResponse) => void;
    lang: string;
}

const PrasnaForm: React.FC<Props> = ({ onResult, lang }) => {
    // Default Prasna timing to current date and time
    const now = new Date();
    const defaultDate = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0') + '-' + String(now.getDate()).padStart(2, '0');
    const defaultTime = String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');

    const [formData, setFormData] = useState({
        name: '',
        gender: 'Male',
        query_text: '',
        lat: 13.0827,
        lon: 80.2707,
        birth_date: '',
        birth_time: '',
        birth_place: '',
        query_date_str: defaultDate,
        query_time_str: defaultTime,
    });
    const [suggestions, setSuggestions] = useState<any[]>([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [loading, setLoading] = useState(false);
    const [searching, setSearching] = useState(false);

    // Profile Management State
    const [profiles, setProfiles] = useState<Profile[]>(() => {
        try {
            const saved = localStorage.getItem('prasna_profiles');
            return saved ? JSON.parse(saved) : [];
        } catch (err) {
            console.error("Profile parsing error:", err);
            return [];
        }
    });
    const [showProfiles, setShowProfiles] = useState(false);

    const saveProfile = () => {
        if (!formData.name) {
            alert('Please enter a name to save profile');
            return;
        }
        const newProfile: Profile = {
            id: Date.now().toString(),
            name: formData.name,
            gender: formData.gender,
            birth_date: formData.birth_date,
            birth_time: formData.birth_time,
            birth_place: formData.birth_place,
            lat: formData.lat,
            lon: formData.lon
        };
        const updated = [newProfile, ...profiles];
        setProfiles(updated);
        localStorage.setItem('prasna_profiles', JSON.stringify(updated));
        setShowProfiles(true); // Automatically show profiles after saving
        alert('Profile saved successfully!');
    };

    const loadProfile = (p: Profile) => {
        setFormData({
            ...formData,
            name: p.name,
            gender: p.gender,
            birth_date: p.birth_date,
            birth_time: p.birth_time,
            birth_place: p.birth_place,
            lat: p.lat,
            lon: p.lon
        });
        setShowProfiles(false);
    };

    const deleteProfile = (id: string, e: React.MouseEvent) => {
        e.stopPropagation();
        const updated = profiles.filter(p => p.id !== id);
        setProfiles(updated);
        localStorage.setItem('prasna_profiles', JSON.stringify(updated));
    };

    const handlePlaceChange = async (val: string) => {
        setFormData({ ...formData, birth_place: val });
        const searchVal = val.trim();
        if (searchVal.length > 2) {
            setSearching(true);
            try {
                // Limit to India (countrycodes=in) and include address details
                const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchVal)}&addressdetails=1&countrycodes=in&limit=5`);
                const data = await res.json();
                setSuggestions(data);
                setShowSuggestions(true);
            } catch (err) {
                console.error("Geocoding error:", err);
            } finally {
                setSearching(false);
            }
        } else {
            setSuggestions([]);
            setShowSuggestions(false);
        }
    };

    const selectPlace = (place: any) => {
        setFormData({
            ...formData,
            birth_place: place.display_name,
            lat: parseFloat(place.lat),
            lon: parseFloat(place.lon)
        });
        setShowSuggestions(false);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await calculatePrasna({ ...formData, lang });
            onResult(res);
        } catch (err) {
            console.error(err);
            alert('Error calculating sequence. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const t = {
        en: {
            title: 'Prasna Query',
            subtitle: 'Enter details for accurate Jamakkal calculation',
            clientInfo: 'Client Information',
            name: 'Client Name',
            gender: 'Gender',
            query: 'Question of Query',
            queryPlaceholder: 'e.g., What is health condition as of now?',
            male: 'Male',
            female: 'Female',
            other: 'Other',
            location: 'Query Location (Chennai default)',
            birthDetails: 'Birth Details (Optional)',
            date: 'Birth Date',
            time: 'Birth Time',
            place: 'Birth Place',
            lat: 'Latitude',
            lon: 'Longitude',
            saveProfile: 'Save as Profile',
            savedProfiles: 'Saved Profiles',
            noProfiles: 'No profiles saved yet',
            load: 'Load',
            delete: 'Delete',
            queryTiming: 'Prasna Analysis Timing (Optional)',
            qDate: 'Analysis Date',
            qTime: 'Analysis Time',
            nowHint: '(Leave blank for current time)'
        },
        ta: {
            title: 'பிரசன்ன கேள்வி',
            subtitle: 'துல்லியமான ஜாமக்கோள் கணக்கீட்டிற்கான விவரங்களை உள்ளிடவும்',
            clientInfo: 'வாடிக்கையாளர் தகவல்',
            name: 'வாடிக்கையாளர் பெயர்',
            gender: 'பாலினம்',
            query: 'கேள்வி (Question)',
            queryPlaceholder: 'எ.கா., தற்போதைய ஆரோக்கிய நிலை என்ன?',
            male: 'ஆண்',
            female: 'பெண்',
            other: 'மற்றவை',
            location: 'கேள்வி இடம் (சென்னை இயல்புநிலை)',
            birthDetails: 'பிறப்பு விவரங்கள் (விருப்பமானது)',
            date: 'பிறந்த தேதி',
            time: 'பிறந்த நேரம்',
            place: 'பிறந்த இடம்',
            submit: 'பிரசன்னம் பார்க்க',
            lat: 'அட்சரேகை',
            lon: 'தீர்க்கரேகை',
            saveProfile: 'சுயவிவரமாகச் சேமி',
            savedProfiles: 'சேமிக்கப்பட்ட சுயவிவரங்கள்',
            noProfiles: 'சுயவிவரங்கள் எதுவும் சேமிக்கப்படவில்லை',
            load: 'ஏற்று',
            delete: 'அழி',
            queryTiming: 'பிரசன்ன பகுப்பாய்வு நேரம் (விருப்பமானது)',
            qDate: 'பகுப்பாய்வு தேதி',
            qTime: 'பகுப்பாய்வு நேரம்',
            nowHint: '(தற்போதைய காலத்திற்கு காலியாக விடவும்)'
        }
    }[lang as 'en' | 'ta'];

    return (
        <form onSubmit={handleSubmit} className="glass-panel" style={{ padding: '2rem', maxWidth: '600px', margin: '2rem auto' }}>
            <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                <h2 className="text-gold" style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>{t.title}</h2>
                <p style={{ color: 'var(--color-text-dim)' }}>{t.subtitle}</p>
            </div>

            {/* Profile Selection Logic */}
            <div style={{ marginBottom: '2rem', display: 'flex', justifyContent: 'flex-end' }}>
                <button
                    type="button"
                    className="glass-panel"
                    onClick={() => setShowProfiles(!showProfiles)}
                    style={{ padding: '8px 16px', display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'white', cursor: 'pointer' }}
                >
                    <UserCircle size={18} className="text-gold" /> {t.savedProfiles} ({profiles.length})
                </button>
            </div>

            {showProfiles && (
                <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '2rem', maxHeight: '400px', overflowY: 'auto', border: '1px solid var(--color-gold)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                        <h4 style={{ margin: 0, color: 'var(--color-gold)' }}>{t.savedProfiles}</h4>
                        <button
                            type="button"
                            onClick={() => setShowProfiles(false)}
                            style={{ background: 'none', border: 'none', color: 'white', cursor: 'pointer', fontSize: '1.2rem' }}
                        >
                            ×
                        </button>
                    </div>
                    {profiles.length === 0 ? (
                        <p style={{ textAlign: 'center', color: 'var(--color-text-dim)' }}>{t.noProfiles}</p>
                    ) : (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                            {profiles.map(p => (
                                <div
                                    key={p.id}
                                    className="suggestion-item"
                                    style={{
                                        display: 'flex',
                                        justifyContent: 'space-between',
                                        alignItems: 'center',
                                        borderRadius: '8px',
                                        padding: '12px',
                                        background: 'rgba(255,255,255,0.02)',
                                        border: '1px solid rgba(255,255,255,0.05)',
                                        marginBottom: '0.5rem'
                                    }}
                                >
                                    <div style={{ flex: 1 }}>
                                        <div style={{ fontWeight: 600, color: 'var(--color-gold)' }}>{p.name}</div>
                                        <div style={{ fontSize: '0.75rem', color: 'var(--color-text-dim)' }}>{p.birth_place}</div>
                                    </div>
                                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                                        <button
                                            type="button"
                                            onClick={() => loadProfile(p)}
                                            style={{
                                                padding: '4px 12px',
                                                fontSize: '0.75rem',
                                                borderRadius: '6px',
                                                background: 'var(--color-gold)',
                                                color: 'white',
                                                border: 'none',
                                                cursor: 'pointer'
                                            }}
                                        >
                                            {t.load}
                                        </button>
                                        <button
                                            type="button"
                                            onClick={(e) => deleteProfile(p.id, e)}
                                            style={{
                                                background: 'rgba(255,77,77,0.1)',
                                                border: '1px solid rgba(255,77,77,0.2)',
                                                color: '#ff4d4d',
                                                cursor: 'pointer',
                                                padding: '4px',
                                                borderRadius: '6px',
                                                display: 'flex',
                                                alignItems: 'center'
                                            }}
                                            title={t.delete}
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}

            <div style={{ marginBottom: '2rem' }}>
                <h3 className="card-title">{t.clientInfo}</h3>
                <div className="grid-2">
                    <div>
                        <label>{t.name}</label>
                        <input
                            type="text"
                            placeholder="Full Name"
                            value={formData.name}
                            onChange={e => setFormData({ ...formData, name: e.target.value })}
                        />
                    </div>
                    <div>
                        <label>{t.gender}</label>
                        <select
                            value={formData.gender}
                            onChange={e => setFormData({ ...formData, gender: e.target.value })}
                        >
                            <option value="Male">{t.male}</option>
                            <option value="Female">{t.female}</option>
                            <option value="Other">{t.other}</option>
                        </select>
                    </div>
                </div>
            </div>

            <div style={{ marginBottom: '2rem' }}>
                <h3 className="card-title">{t.query}</h3>
                <textarea
                    placeholder={t.queryPlaceholder}
                    value={formData.query_text}
                    onChange={e => setFormData({ ...formData, query_text: e.target.value })}
                    className="glass-panel"
                    style={{ width: '100%', padding: '12px', minHeight: '80px', color: 'white', border: '1px solid rgba(255,255,255,0.1)' }}
                />
            </div>

            <div style={{ marginBottom: '2rem' }}>
                <h3 className="card-title"><MapPin size={20} className="text-gold" /> {t.location}</h3>
                <div className="grid-2">
                    <div>
                        <label>{t.lat}</label>
                        <input
                            type="number" step="any"
                            value={formData.lat}
                            onChange={e => setFormData({ ...formData, lat: parseFloat(e.target.value) })}
                        />
                    </div>
                    <div>
                        <label>{t.lon}</label>
                        <input
                            type="number" step="any"
                            value={formData.lon}
                            onChange={e => setFormData({ ...formData, lon: parseFloat(e.target.value) })}
                        />
                    </div>
                </div>
            </div>

            <div style={{ marginBottom: '2rem' }}>
                <h3 className="card-title"><Clock size={20} className="text-gold" /> {t.queryTiming}</h3>
                <p style={{ fontSize: '0.75rem', color: 'var(--color-text-dim)', marginTop: '-0.8rem', marginBottom: '1rem' }}>{t.nowHint}</p>
                <div className="grid-2">
                    <div>
                        <label>{t.qDate}</label>
                        <input
                            type="date"
                            value={formData.query_date_str}
                            onChange={e => setFormData({ ...formData, query_date_str: e.target.value })}
                        />
                    </div>
                    <div>
                        <label>{t.qTime}</label>
                        <input
                            type="time"
                            value={formData.query_time_str}
                            onChange={e => setFormData({ ...formData, query_time_str: e.target.value })}
                        />
                    </div>
                </div>
            </div>

            <div style={{ marginBottom: '2rem' }}>
                <h3 className="card-title"><Star size={20} className="text-gold" /> {t.birthDetails}</h3>
                <label>{t.date}</label>
                <div style={{ position: 'relative' }}>
                    <Calendar size={18} style={{ position: 'absolute', left: '12px', top: '12px', color: 'var(--color-gold)' }} />
                    <input
                        type="date"
                        style={{ paddingLeft: '40px' }}
                        value={formData.birth_date}
                        onChange={e => setFormData({ ...formData, birth_date: e.target.value })}
                    />
                </div>

                <div className="grid-2">
                    <div>
                        <label>{t.time}</label>
                        <div style={{ position: 'relative' }}>
                            <Clock size={18} style={{ position: 'absolute', left: '12px', top: '12px', color: 'var(--color-gold)' }} />
                            <input
                                type="time"
                                style={{ paddingLeft: '40px' }}
                                value={formData.birth_time}
                                onChange={e => setFormData({ ...formData, birth_time: e.target.value })}
                            />
                        </div>
                    </div>
                    <div>
                        <div>
                            <label>{t.place}</label>
                            <div style={{ position: 'relative' }}>
                                <input
                                    type="text"
                                    placeholder="City, Country"
                                    value={formData.birth_place}
                                    onChange={e => handlePlaceChange(e.target.value)}
                                />
                                {searching && (
                                    <div style={{ position: 'absolute', right: '10px', top: '10px' }}>
                                        <RefreshCw size={16} className="animate-spin" />
                                    </div>
                                )}
                                {showSuggestions && (
                                    <div className="suggestions-list" style={{
                                        position: 'absolute', top: '100%', left: 0, right: 0,
                                        marginTop: '1px', maxHeight: '200px', overflowY: 'auto'
                                    }}>
                                        {suggestions.length > 0 ? suggestions.map((p, i) => (
                                            <div
                                                key={i}
                                                className="suggestion-item"
                                                onClick={() => selectPlace(p)}
                                            >
                                                {p.display_name}
                                            </div>
                                        )) : (
                                            <div className="no-results">No results found in India</div>
                                        )}
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                <button
                    type="submit"
                    className="btn-primary"
                    style={{ flex: 2, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem' }}
                    disabled={loading}
                >
                    {loading ? 'Calculating...' : <><Send size={18} /> {t.submit}</>}
                </button>
                <button
                    type="button"
                    onClick={saveProfile}
                    className="glass-panel"
                    style={{ flex: 1, padding: '12px', color: 'white', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}
                >
                    <Save size={18} className="text-gold" /> {t.saveProfile}
                </button>
            </div>
        </form>
    );
};

export default PrasnaForm;
