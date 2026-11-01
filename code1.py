from fastapi import FastAPI,HTTPException,Path
import json

app = FastAPI()
@app.get('/') #Endpoint : where the message in the url will be displayed is known as endpoint
def greet():
    return {"Hii good morning bro"}


@app.get('/hello')
def home():
    return {"Hello harsh! , kaise ho beta"}

def get_data():
    with open("students.json","r") as f:
        return json.load(f)

@app.get('/student')
def student():
    return get_data()

# student_id is a endpoint
@app.get('/student/{student_id}')
def getvid(student_id : str = Path(..., description="This id of the student")):
    data = get_data()
    if student_id not in data:
        raise HTTPException(
            status_code = 404,
            detail = f"student of id '{student_id}' not found"
        )
    return data[student_id]


@app.get('/filter')
def filter_student(course :str):
    data = get_data()
    if course not in data:
        return data

    filtered = {}
    for id , info in data:
        if info[course] == course:
            filtered[id] = info
            
