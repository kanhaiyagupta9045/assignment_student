from fastapi import FastAPI,HTTPException,Query,Path
from typing import Optional
from dotenv import load_dotenv
from bson.objectid import ObjectId
from databases.mongo_conn import student_collection
from models.student_model import CreateStudentRequest,CreateStudentResponse,ListStudent,ListStudentsResponse,FetchStudentResponse,UpdateStudentRequest,DeleteStudentResponse
load_dotenv()


app = FastAPI()

@app.get("/home")
def read_root():
    return {"Hello": "World"}




@app.post("/students", response_model=CreateStudentResponse, status_code=201)
async def create_student(student: CreateStudentRequest):
    student_data = student.dict()

    try:
       
        result = student_collection.insert_one(student_data)
        return {"id": str(result.inserted_id)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while inserting student: {e}")
    


@app.get("/students", response_model=ListStudentsResponse)
async def list_students(
    country: Optional[str] = Query(None, description="Filter by country"),
    age: Optional[int] = Query(None, description="Filter by age >= specified value"),
):
    try:
        filters = {}
        if country is not None:
            filters["address.country"] = country
        if age is not None:
            filters["age"] = {"$gte": age}
        students = list(student_collection.find(filters))
        student_list = [{"name": student["name"], "age": student["age"]} for student in students]

        return {"data": student_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while fetching students: {e}")
    



@app.get("/students/{id}", response_model=FetchStudentResponse)
async def fetch_student(id: str = Path(..., description="ID of the student")):
    try:
        student = student_collection.find_one({"_id": ObjectId(id)})

        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return FetchStudentResponse(
            name=student["name"],
            age=student["age"],
            address=student["address"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching student: {e}")



@app.patch("/students/{id}", response_model=FetchStudentResponse, status_code=200)
async def update_student(id: str = Path(..., description="ID of the student"), student: UpdateStudentRequest = None):
    try:
        update_data = student.dict(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

       
        result = student_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        updated_student = student_collection.find_one({"_id": ObjectId(id)})
        return FetchStudentResponse(
            name=updated_student["name"],
            age=updated_student["age"],
            address=updated_student["address"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating student: {e}")
    

@app.delete("/students/{id}", response_model=DeleteStudentResponse)
async def delete_student(id: str = Path(..., description="ID of the student")):
    try:
        
        result = student_collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {"message": "Student deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting student: {e}")
