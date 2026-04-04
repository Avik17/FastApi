from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age:int
    weight:int

patient1={"name":'Rohit',"age":"30","weight":76}

def getinfo(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)

getinfo(Patient(**patient1))    