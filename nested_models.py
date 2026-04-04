from pydantic import BaseModel


class Address(BaseModel):
      city:str
      pincode:int
      state:str
      
class Patient(BaseModel):
      name:str
      age:int
      address: Address
patient1_address={"city":"Patna","pincode":784000,"state":"Bihar"}
patient_name={"name":"Mokit","age":45,"address":patient1_address}


patient=Patient(**patient_name)
print(patient.name)
print(patient.age)
print(patient.address)



