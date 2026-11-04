"""
PYDANTIC FUNDAMENTALS'

mac :- pip3 install pydantic
win :- pip install pydantic
       uv add pydantic
"""

"""
STEP 1 - The Problem
A normal dictionary accepts ANYTHING. Nobody checks the data.
"""
bad_student = {
    "name"  :"",
    "age"   :"Twenty",
    "marks" :150,
    "email" :"not-an-email"
}
# print(bad_student)




from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field
"""
Step 2 - BASEMODEL + TYPE HINTS
we describe a student ONCE. Python checks every student against it.
"""
# class SimpleStudent(BaseModel): #Pydantic Model.
#     name : str
#     age  : int
#     marks : int

# s = SimpleStudent(name="Arav Sharma", age="21", marks=80)
# print(s.name, s.age, s.marks)



"""
Step 3 - FIELD() RULES
gt = greater than               lt = less than
ge = greater or equal           le = less or equal
"""
class RuleStudent(BaseModel):
    name    : str = Field(..., min_length=2, max_length=50)     #... = required
    age     : int = Field(..., gt=0, lt=100)                    #1 to 99
    marks   : int = Field(..., gt=0, le=100)                    #0 to 100
    course  : str = "Python"                                    #default value -> Python
    phone   : str | None = None                                 #Optional field can be empty

s = RuleStudent(name="Rohan Verma", age=21, marks=77)







"""
Step 4 - EMAILSTR
checks the text really looks like an email.
"""
class EmailStudent(BaseModel):
    name : str
    email : EmailStr

s = EmailStudent(name="Kabir Singh", email="kabirsingh@gmail.com")







"""
Step 5 - FINAL STUDENT MODEL
1. field_validator  -> our OWN custom rule.
2. computed_field   -> a value Pydantic calculates for US.
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

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age >= 60:
            return "old"
        elif self.age >= 40:
            return "adult"
        elif self.age >= 18:
            return "young"
        elif self.age >= 12:
            return "teenager"
        else:
            return "child"
        

    

s = Student(id="S001",
            name="aarav sharma",
            age = 11,
            course = "Python",
            marks=99,
            email="arav@gmail.com")


"""
Step 6 MODEL_DUMP()
turn a model back into Python dictionary (so that we can save it later)
"""
data = s.model_dump()
# print(data)


import json
"""
Step 7 - CHECK OUR REAL DATA (students.json)
Every student in our file will go through the Student Model
"""
with open("students.json", "r") as file:
    raw = json.load(file)

for student_id , info in raw.items():
    s = Student(id = student_id, **info)
    print(s.id, s.name, s.grade, s.email)
    
    