from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, date, time
from typing import Optional, Dict, Any, List
import os
import json
import dateutil.parser

from engines.jamakkal import JamakkalEngine
from engines.prediction import PredictionEngine
from engines.natal import NatalEngine
from utils.pdf_generator import PremiumPDFGenerator

app = FastAPI(title="Jamakkal Prasna API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Profile Storage ─────────────────────────────────────────────
PROFILES_FILE = os.path.join(os.path.dirname(__file__), "profiles.json")

def _read_profiles() -> list:
    if not os.path.exists(PROFILES_FILE):
        return []
    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _write_profiles(profiles: list):
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)

class ProfileModel(BaseModel):
    id: str
    name: str
    gender: str
    birth_date: str = ""
    birth_time: str = ""
    birth_place: str = ""
    lat: float = 0.0
    lon: float = 0.0

class PrasnaRequest(BaseModel):
    name: Optional[str] = "Valued Client"
    gender: Optional[str] = "Not Specified"
    query_text: Optional[str] = ""
    # Explicit Competition Mode Fields
    competition_team_a: Optional[str] = None
    competition_team_b: Optional[str] = None
    competition_team_a_captain: Optional[str] = None
    competition_team_b_captain: Optional[str] = None
    toss_winner: Optional[str] = None
    toss_decision: Optional[str] = None
    lat: float
    lon: float
    query_time: Optional[datetime] = None
    query_date_str: Optional[str] = None
    query_time_str: Optional[str] = None
    lang: str = "en"
    birth_date: Optional[date] = None
    birth_time: Optional[time] = None
    birth_place: str = "Unknown"
    analysis_mode: str = "prasna_only"
    location: Optional[str] = "Chennai"

@app.get("/")
def read_root():
    return {"message": "Jamakkal Prasna API is running"}

# ── Profile CRUD Endpoints ──────────────────────────────────────
@app.get("/profiles")
def get_profiles():
    return _read_profiles()

@app.post("/profiles")
def save_profile(profile: ProfileModel):
    profiles = _read_profiles()
    # Replace if same id exists, otherwise prepend
    profiles = [p for p in profiles if p["id"] != profile.id]
    profiles.insert(0, profile.model_dump())
    _write_profiles(profiles)
    return {"status": "ok"}

@app.delete("/profiles/{profile_id}")
def delete_profile(profile_id: str):
    profiles = _read_profiles()
    profiles = [p for p in profiles if p["id"] != profile_id]
    _write_profiles(profiles)
    return {"status": "ok"}

@app.post("/calculate")
def calculate_prasna(req: PrasnaRequest):
    try:
        query_time = req.query_time or datetime.now()
        
        # Override with manual strings if provided
        if req.query_date_str and req.query_time_str:
            try:
                dt_str = f"{req.query_date_str} {req.query_time_str}"
                # Handle potential formats like DD/MM/YYYY and 12-hour AM/PM times gracefully
                # ISO (YYYY-MM-DD) is sent by frontend. dateutil handles it best without dayfirst=True.
                query_time = dateutil.parser.parse(dt_str)
                print(f"DEBUG: Parsed query_time as {query_time} from input {dt_str}")
            except Exception as e:
                print(f"Error parsing manual query time '{dt_str}': {e}")
                
        jam_engine = JamakkalEngine(req.lat, req.lon, query_time)
        jam_data = jam_engine.compute_all()
        
        is_strict_comp = False
        if req.competition_team_a and req.competition_team_b:
            is_strict_comp = True
            qt = f"TEAM A : {req.competition_team_a}"
            if req.competition_team_a_captain:
                qt += f" ({req.competition_team_a_captain})"
            qt += f"\nTEAM B : {req.competition_team_b}"
            if req.competition_team_b_captain:
                qt += f" ({req.competition_team_b_captain})"
            req.query_text = qt
            
        jam_data['query_text'] = req.query_text
        jam_data['location'] = req.location or req.birth_place
        jam_data['birth_place'] = req.birth_place
        jam_data['is_strict_competition_mode'] = is_strict_comp
        jam_data['toss_winner'] = getattr(req, 'toss_winner', None)
        jam_data['toss_decision'] = getattr(req, 'toss_decision', None)
        
        natal_data = {}
        if req.analysis_mode == "prasna_with_natal" and req.birth_date and req.birth_time:
            natal_engine = NatalEngine({
                "name": req.name,
                "gender": req.gender,
                "birth_date": str(req.birth_date),
                "birth_time": str(req.birth_time),
                "birth_place": req.birth_place,
                "lat": req.lat,
                "lon": req.lon
            })
            natal_data = natal_engine.compute_all()
            
        pred_engine = PredictionEngine(jam_data, natal_data)
        full_data = pred_engine.generate_full_report_data(req.lang)
        full_data['query_text'] = req.query_text
        full_data['name'] = req.name
        full_data['gender'] = req.gender
        full_data['natal'] = natal_data
        full_data['query_time_str'] = query_time.strftime("%Y-%m-%d %H:%M:%S")
        full_data['analysis_mode'] = req.analysis_mode
        full_data['is_strict_competition_mode'] = is_strict_comp
        
        return full_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-pdf")
def generate_pdf(report_data: Dict[str, Any]):
    try:
        filename = f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        output_path = os.path.join(os.getcwd(), filename)
        
        gen = PremiumPDFGenerator(report_data, output_path)
        gen.generate()
        
        with open(output_path, "rb") as f:
            content = f.read()
            
        # Optional: cleanup file after reading
        # os.remove(output_path)
        
        return Response(
            content=content,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9999)
