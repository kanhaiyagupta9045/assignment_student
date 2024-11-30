from pydantic import BaseModel, Field
from typing import Optional



class Address(BaseModel):
    city: str = Field(..., description="city")
    country: str = Field(..., description="country")



class CreateStudentRequest(BaseModel):
    name: str = Field(..., description="name")
    age: int = Field(..., description="age")
    address: Address = Field(..., description="address")



class CreateStudentResponse(BaseModel):
    id: str = Field(..., description="id")



class ListStudent(BaseModel):
    name: str = Field(..., description="name")
    age: int = Field(..., description="age")


class ListStudentsResponse(BaseModel):
    data: list[ListStudent] = Field(..., description="list of students")



class FetchStudentResponse(BaseModel):
    name: str = Field(..., description="name")
    age: int = Field(..., description="age")
    address: Address = Field(..., description="address")



class UpdateStudentRequest(BaseModel):
    name: Optional[str] = Field(None, description="updated_name")
    age: Optional[int] = Field(None, description="updated_age")
    address: Optional[Address] = Field(None, description="updated_address")



class DeleteStudentResponse(BaseModel):
    message: str = Field(..., description="status of deletion")
