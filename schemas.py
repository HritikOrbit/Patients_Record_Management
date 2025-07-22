from pydantic import BaseModel, Field
from typing import Optional, Literal

class PatientBase(BaseModel):
    id: str
    name: str
    city: str
    age: int = Field(..., gt=0, lt=120)
    gender: Literal["Male", "Female", "Others"]
    height: float = Field(..., gt = 0)
    weight: float = Field(..., gt = 0)


class PatientCreate(PatientBase):
    id: str
    

class PatientUpdate(BaseModel):
    name: Optional[str]
    city: Optional[str]
    age: Optional[int] = Field(None, gt = 0, lt = 120)
    gender: Optional[Literal["Male", "Female", "Others"]]
    height: Optional[float] = Field(None, gt = 0)
    weight: Optional[float] = Field(None, gt = 0)

class PatientResponse(BaseModel):
    id: str
    name: str
    city: str
    age: int
    gender: str
    height: float
    weight: float
    bmi: float
    verdict: str



    @staticmethod
    def calculate_bmi(height: float, weight: float) -> float:
        return round(weight / (height ** 2),2)
    
    @staticmethod
    def get_verdict(bmi: float) -> str:
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Normal"
        else:
            return "Obese"
        
    @classmethod
    def from_orm_patient(cls, patient):
        bmi = cls.calculate_bmi(patient.height, patient.weight)
        verdict = cls.get_verdict(bmi)
        return cls(
            id = patient.id,
            name = patient.name,
            city = patient.city,
            age = patient.age,
            gender = patient.gender,
            height = patient.height,
            weight = patient.weight,
            bmi = bmi,
            verdict = verdict

        )
