from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, date, time
from typing import Optional, Dict, Any
import os

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

class PrasnaRequest(BaseModel):
    name: Optional[str] = "Valued Client"
    gender: Optional[str] = "Not Specified"
    query_text: Optional[str] = ""
    lat: float
    lon: float
    query_time: Optional[datetime] = None
    query_date_str: Optional[str] = None
    query_time_str: Optional[str] = None
    lang: str = "en"
    birth_date: Optional[date] = None
    birth_time: Optional[time] = None
    birth_place: str = "Unknown"

@app.get("/")
def read_root():
    return {"message": "Jamakkal Prasna API is running"}

@app.post("/calculate")
def calculate_prasna(req: PrasnaRequest):
    try:
        query_time = req.query_time or datetime.now()
        
        # Override with manual strings if provided
        if req.query_date_str and req.query_time_str:
            try:
                dt_str = f"{req.query_date_str} {req.query_time_str}"
                query_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            except Exception as e:
                print(f"Error parsing manual query time: {e}")
                
        jam_engine = JamakkalEngine(req.lat, req.lon, query_time)
        jam_data = jam_engine.compute_all()
        jam_data['query_text'] = req.query_text
        
        natal_data = {}
        if req.birth_date and req.birth_time:
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
    uvicorn.run(app, host="0.0.0.0", port=8999)
