from pydantic import BaseModel

class CarBase(BaseModel):
    make: str
    model: str
    year: int
    plate_number: str

class CarCreate(CarBase):
    pass

class CarResponse(CarBase):
    id: int

    class Config:
        orm_mode = True
