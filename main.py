from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import json,os
app=FastAPI()

class Patient(BaseModel):
    patient_id: str
    name: str
    age: int
    gender: str
    city: str
    status: str = "active"


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
             raise HTTPException(status_code=404, detail="No Patient found")  
         
         return { "total": len(patients), "patients":patients}
    
@app.post('/patients')    
def add_patient(patient:Patient):
    with open("patients.json") as file:
         data=json.load(file)

    if patient.patient_id in [p["patient_id"] for p in data["patients"]]:
        raise HTTPException (status_code=400,detail="Patient already exists")
            
    data["patients"].append(patient.model_dump())
    data["total_patients"]=len(data["patients"])
    temp_path = "patients.json.tmp"
    with open(temp_path, "w") as file:
        json.dump(data, file, indent=2)
    os.replace(temp_path, "patients.json")
    
    return{"message":"Patient Created","patient":patient}
    
        
