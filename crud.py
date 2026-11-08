from fastapi import FastAPI,HTTPException,Path,Query
from pydantic import BaseModel,field_validator,computed_field,Field,EmailStr
from fastapi.middleware.cors import CORSMiddleware #CORS - cross origin resource sharing
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=True,
    allow_credentials=True, #allow cokkies
    allow_headers=["*"] # authorization 
    allow_methods= True
)

# Method 1
@app.get('/') #Endpoint : where the message in the url will be displayed is known as endpoint
def greet():
    return {"Hii good morning bro"}


@app.get('/hello')
def home():
    return {"Hello harsh!"}

#Helper function1
def get_data():
    with open("students.json","r") as f:
        return json.load(f)

#Helper function2
def save_data(data):
    with open("students.json" ,"w") as file:
        json.dump(data, file, indent=4) #indent 4 keeps the file readable



@app.get('/student')
def student():
    return get_data()




#student_id is a endpoint
#Path Parameters
@app.get('/student/{student_id}')
def getvid(student_id : str = Path(..., description="This id of the student")):
    data = get_data()
    if student_id not in data:
        raise HTTPException(
            status_code = 404,
            detail = f"student of id '{student_id}' not found"
        )
    return data[student_id]


# http://127.0.0.1:8000/filter?course=Data Science
#Filteration using Query Parameters
@app.get('/filter')#endpoint created
def filter_student(course :str = None):#course is our query parameter 
    data = get_data()
    if course is None:
        return data

    filtered = {}#s001 = aarav ki details
    # course = course.lower()
    for id , info in data.items():
        
        if info["course"].lower() == course.lower():
            filtered[id] = info

    return filtered



# http://127.0.0.1:8000/sorting?sorting_by=marks,age,name&order=asc,desc
sort_fields = ["marks", "age", "name"]
sort_order = ["asc", "desc"]
@app.get('/sorting')
def sort_students(
    sorting_by : str,
    order : str
):
    #if the given sort_by input doesn't belongs to sort_fields
    if sorting_by not in sort_fields:
        raise HTTPException(
            status_code=404,
            detail= f"Invalid sorting_by given by the user choose from {sort_fields}"
        )
    #if the given order not in sort_order
    if order not in sort_order:
        raise HTTPException(
            status_code=404,
            detail=f"order must be from {sort_order}"
        )

    #STEP1: Turn the dictionary into list 
    data = get_data()
    student = []
    for id , info in data.items():
        info["id"] = id
        student.append(info)

    #STEP2: Sort the list by the choosen field
    reverse = (order == 'desc')
    sorted_students = sorted(student, key = lambda s:s[sorting_by], reverse=reverse)
    return sorted_students


# Method 2
""" 
  REQUEST BODY

  Post - data comes in the BODY(a JSON object sent with the request)
  When a function argument is a pydantic Model, FastAPI reads it from the body
  and validates automatically, Bad Data -> 422
   
"""
class Student(BaseModel):
    id      : str = Field(..., examples=["S001"])
    name    : str = Field(..., min_length=2, max_length=50)
    age     : int = Field(..., gt=0, le=100)
    course  : str = Field(..., max_length=50)
    marks   : int = Field(..., ge=0, le=100)
    email   : EmailStr

    #Custom Rule : Name must contain only letters and spaces
    @field_validator("name")#name=Kabir singh
    @classmethod
    def check_name(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters and spaces")
        
        return value.title()

    @computed_field
    @property
    def grade(self) -> str:
        if self.marks >= 90:
            return "A+"
        elif self.marks >= 80:
            return "A"
        elif self.marks >= 70:
            return "B"
        elif self.marks >= 60:
            return "C"
        else:
            return "F"

@app.post('/create', status_code=201)
def create_student(student: Student):
    data = get_data()
    data[student.id] = student.model_dump(exclude = {"id", "grade"})  
    save_data(data)

    return {"message" : "student created sucessfully", "student": student}




# Method 3
#Update any existing data
class StudentUpdate(BaseModel):
    name : str| None = Field(None , min_length=2,max_length=20)
    age  : int|None = Field(None , gt=0 , lt=100)
    course: str|None = Field(None, max_length=30)
    marks : int|None = Field(None, ge=0, le=100)
    email : EmailStr|None = None 


@app.put("/update/{student_id}")
def update_student(
    student_update : StudentUpdate,
    student_id : str = Path(...,description="The Id of the student",
    examples=["S001"])
):
    
    data = get_data()
    if student_id not in data:
        raise HTTPException(
            status_code=404,
            detail="The provided ID is not present in data"
        )

    #Step 1: The student as it is right now.
    existing = data[student_id]


    #Step2 : Only the fields the Client actually sent
    update = student_update.model_dump(exclude_unset=True)

    #step3: Copy the new value on the top of old value
    for key,value in update.items():
        existing[key] = value

    #step4: check the final student again
    student = Student(id=student_id , **existing)

    data[student_id] = student.model_dump(exclude=["id", "grade"])
    save_data(data)

    return{"message: student updated sucessfully"}




# Method 4
@app.delete("/delete/{student_id}")

def delete_student(

    student_id : str = Path(...,description="The id you wanna delete",
                            examples=["S001"])

):
    data = get_data()
    if student_id not in data:
        raise HTTPException(
            status_code=404,
            detail=f"the provided id {student_id} is not present"
        )
    
    del data[student_id]
    save_data(data)

    return {"message": f"student '{student_id}' deleted sucessfully"}