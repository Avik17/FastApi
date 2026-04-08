from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import json,os
from typing import List,Optional

app=FastAPI()

class Patient(BaseModel):
    patient_id: str
    name: str
    age: int
    gender: str
    city: str
    status: str = "active"

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    status: Optional[str] = None

class PatientResponse(BaseModel):
    patient_id: str
    name: str
    age: int
    city: Optional[str] = None
    status: Optional[str] = None
    doctor: Optional[str] = None

class PatientsListResponse(BaseModel):
    total: int
    patients: List[PatientResponse]    
   
@app.get('/about')
def about():
    return {"message":"hello baby"}

@app.get('/info/{patient_id}',response_model=PatientResponse)
def info(patient_id:str):
    with open('patients.json') as file:
         data= json.load(file)
         for patient in data["patients"]:
            if patient_id == patient["patient_id"]:
                return patient
         raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/patients",response_model=PatientsListResponse)
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
    
@app.put('/patients/{patient_id}')
def update(patient_id:str,patient:PatientUpdate):
    with open("patients.json") as file:
        data=json.load(file) 
    for p in data["patients"]:
        if patient_id==p["patient_id"]:
           if patient.name is not None:p["name"]=patient.name                           
           if patient.age is not None:p["age"]=patient.age                          
           if patient.gender is not None:p["gender"]=patient.gender         
           if patient.city is not None:p["city"]=patient.city
           if patient.status is not None:p["status"]=patient.status
           break
    else : raise HTTPException (status_code=404,detail="Patient does not exist") 
    
    temp_path = "patients.json.tmp"
    with open(temp_path, "w") as file:
        json.dump(data, file, indent=2)
    os.replace(temp_path, "patients.json")  
    return{"message":"Patient Details updated"}

    
@app.delete('/patients/{patient_id}')
def delete(patient_id:str):
    with open("patients.json") as file:
        data=json.load(file) 
    for index,p in enumerate(data["patients"]):
        if patient_id==p["patient_id"]:
           data["patients"].pop(index)
           data["total_patients"] = len(data["patients"])
           break
    else : raise HTTPException (status_code=404,detail="Patient does not exist") 
    
    temp_path = "patients.json.tmp"
    with open(temp_path, "w") as file:
        json.dump(data, file, indent=2)
    os.replace(temp_path, "patients.json")  
    return{"message":f"Patient {patient_id} Details updated"}
    
               
