export interface TransitInfo {
    rasi: string;
    rasi_num: number;
    degree: string;
    nakshatra: string;
    pada: number;
    star_lord: string;
    abs_deg: number;
}

export interface NatalData {
    name?: string;
    gender?: string;
    Lagna?: string;
    LagnaRasi?: number;
    LagnaLord?: string;
    Nakshatra?: string;
    Dasha?: string;
    birth_place?: string;
    Positions?: Record<string, number>;
    HouseLords?: Record<string, string>;
    PlanetaryStates?: Record<string, string>;
}

export interface RemedyTiming {
    best_jama_planet: string | null;
    ideal_janma_star: string;
    ideal_sadhana_star: string;
    timing_advice: string[];
}

export interface CategoryData {
    score: number;
    status: string;
    challenges: string[];
    solutions: string[];
}

export interface PrasannaSpecial {
    udhayam: { planet: string; percent: number };
    udhayam_lord: { planet: string; bhava: number };
    arudam_bhava: number;
    arudam: { planet: string; percent: number };
    kavipu: { planet: string; percent: number };
    kavipu_bhava: number;
    exalted: string[];
    debilitated: string[];
    parivarthana: string[];
    kuligan_bhava: number;
    kuligan: { planet: string; percent: number };
    emakandam: { planet: string; percent: number };
    rahu_time: { planet: string; percent: number };
    mrithyu: { planet: string; percent: number };
}

export interface PrasnaResponse {
    name?: string;
    gender?: string;
    query_text?: string;
    summary: string;
    analysis_points: string[];
    diagnostic_analysis: string[];
    recovery_timeline: string[];
    remedies: string[];
    remedy_timing: RemedyTiming;
    synthesis_points: string[];
    synthesis_conclusion: string;
    final_conclusion: string;
    balance_categories: Record<string, CategoryData>;
    ruling_planet: string;
    block: number;
    is_day: boolean;
    positions: Record<string, number>;
    panchanga: Record<string, string>;
    transits: Record<string, TransitInfo>;
    jama_grahas: Record<string, number>;
    inner_planets: Record<string, TransitInfo>;
    prasanna_special?: PrasannaSpecial;
    sunrise_str?: string;
    sunset_str?: string;
    natal: NatalData;
    query_time_str: string;
}

export interface PrasnaRequest {
    name?: string;
    gender?: string;
    query_text?: string;
    lat: number;
    lon: number;
    query_time?: string;
    birth_date?: string;
    birth_time?: string;
    birth_place?: string;
    query_date_str?: string;
    query_time_str?: string;
    lang?: string;
    analysis_mode?: string;
}
