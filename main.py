from fastapi import FastAPI,HTTPException
import json
app=FastAPI()

@app.get('/about')
def about():
    return {"message":"hello baby"}

@app.get('/info/{patient_id}')
def info(patient_id:str):
    with open('patients.json') as file:
         data= json.load(file)
         for patient in data["patients"]:
            if patient_id == patient["patient_id"]:
                return patient
         raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/patients")
def get_patients(city: str = None, status: str = "active"):
    with open("patients.json") as file:
         data=json.load(file)
         patients=data["patients"]
         if city:
             patients=[p for p in patients if p.get("city","").lower()==city.lower()]
         if status:
             patients=[p for p in patients if p.get("status","").lower()==status.lower()] 
         if not patients:
             return HTTPException(status_code=404, detail="No Patient found")  
         
         return { "total": len(patients), "patients":patients}