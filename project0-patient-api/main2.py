from fastapi import FastAPI

app=FastAPI()

@app.get("/patients")
def get_patients(city: str = None, status: str = "active"):
    return {
        "filtering_by_city": city,
        "filtering_by_status": status
    }