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

    
    
    
