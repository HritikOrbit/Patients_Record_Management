from sqlalchemy import Column, String, Integer, Float, Enum, VARCHAR
from database import Base
import enum


class GenderEnum(str, enum.Enum):
    male = 'Male'
    female = 'Female'
    others = 'Others'

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(VARCHAR(20), primary_key= True, index= True)
    name = Column(VARCHAR(100), nullable=False)
    city = Column(VARCHAR(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    bmi = Column(Float, nullable=True)  
    verdict = Column(String, nullable=True)

