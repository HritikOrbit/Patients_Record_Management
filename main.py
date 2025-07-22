from fastapi import FastAPI, Path, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Patient, Base
from schemas import PatientCreate, PatientUpdate, PatientResponse

app = FastAPI()

#create tables in database
Base.metadata.create_all(bind = engine)

# Dependency to get db session

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message" : "A fully fuctional API to manage your patient records"}


# @app.get("/view", response_model=list[PatientResponse])
# def view(db:Session = Depends(get_db)):
#     patients = db.query(Patient).all()
#     return [PatientResponse.from_orm_patient(p) for p in patients]


@app.get("/patient/{patient_id}", response_model=PatientResponse)
def view_patient(
    patient_id: str = Path(..., description= "ID of the patient"),
    db: Session = Depends(get_db),
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail = "Patient not found")
    return PatientResponse.from_orm_patient(patient)

@app.get("/sort", response_model=list[PatientResponse])
def sort_patient(
    sort_by: str = Query(..., description= "Sort by height, weight, or bmi"),
    order: str = Query("asc", description= "Order: asc or desc"),
    db: Session = Depends(get_db),
):
    if sort_by not in ["height", "weight", "bmi"]:
        raise HTTPException(status_code=400, detail= "Invalid field.... !!")
    
    patients = db.query(Patient).all()
    patient_objs = [PatientResponse.from_orm_patient(p) for p in patients]

    reverse = order == "desc"
    sorted_patients = sorted(patient_objs, key= lambda x: getattr(x, sort_by), reverse = reverse)


    return sorted_patients

@app.post("/create", status_code=201)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    if db.query(Patient).filter(Patient.id == patient.id).first():
        raise HTTPException(status_code=400, detail="Patient already exists")
    

    db_patient = Patient(**patient.model_dump())

    bmi = PatientResponse.calculate_bmi(patient.height, patient.weight)
    verdict = PatientResponse.get_verdict(bmi)
    db_patient.bmi = bmi
    db_patient.verdict = verdict
    
    db.add(db_patient)
    db.commit()
    return {"message": "Patient created successfully...."}


@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, update: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail= "Patient not found")
    
    update_data = update.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(patient, key, value)

    bmi = PatientResponse.calculate_bmi(patient.height, patient.weight)
    verdict = PatientResponse.get_verdict(bmi)
    patient.bmi = bmi
    patient.verdict = verdict

    db.commit()
    return {"message": "Patient update successfully"}


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail= "Patient not found")
    
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}


    