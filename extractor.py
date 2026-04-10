import os,anthropic,instructor
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List,Optional

load_dotenv()
client=instructor.from_anthropic(anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")))

text=[ """Patient Arjun Singh, 67yo male, admitted with chest pain.
    ECG confirmed acute MI. Started on aspirin 100mg daily,
    metoprolol 25mg twice daily. Critical condition.""",

    """Priya Sharma 31 years old. Came in for routine checkup.
    Mild migraine. Prescribed ibuprofen 400mg as needed. Stable.""",

    """Mohammed Irfan, twenty-five year old, breathing difficulty.
    Diagnosed asthma. Given salbutamol inhaler 100mcg when needed.
    Non-critical."""]

class Medicines(BaseModel):
    name:str
    dosage:str
    frequency:str


class Medical_Record(BaseModel):
    name:str
    age:int
    diagnosis:str
    medicine:List[Medicines]
    isCritical:bool

for patient in text:
    prompt=patient
    record=client.messages.create(messages=[{"role":"user","content":prompt}],response_model=Medical_Record,model="claude-haiku-4-5-20251001",
                                  max_tokens=1024)
    print(f"name:{record.name}")
    print(f"age:{record.age}")
    print(f"diagnosis:{record.diagnosis}")
    print(f"Critical:{record.isCritical}")
    print(f"  Medications:")
    for med in record.medicine:
        print(f"- {med.name} {med.dosage} {med.frequency}")

