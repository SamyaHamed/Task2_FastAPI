from fastapi import APIRouter, Depends, HTTPException
from pyexpat.errors import messages
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database.data import AsyncSessionLocal
from models.Student import Student
from models.School import  School
from schema.StudentSchema import StudentResponse, StudentCreate,StudentUpdate

router = APIRouter(
    prefix="/student",
    tags=["Students"]
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/")
async def add_student(
    student: StudentCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(School).where(School.id == student.school_id)
    )
    school = result.scalar_one_or_none()

    if not school:
        raise HTTPException(
            status_code=404,
            detail="School not found"
        )

    new_student = Student(
        first_name = student.first_name,
        last_name = student.last_name,
        birth_date = student.birth_date,
        school_id=student.school_id
    )
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return { "message": "Student added successfully" ,
             "student": new_student }


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id : int ,db: AsyncSession = Depends(get_db)):
    students = await db.execute(select(Student).where(Student.id == student_id))
    return  students.scalars().all()

@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
        student_id : int ,
        payload: StudentUpdate,
        db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(student, key, value)

    await db.commit()
    await db.refresh(student)
    return student

@router.delete("/{student_id}")
async def delete_student(student_id: int ,db: AsyncSession = Depends(get_db)):
    students = await db.execute(select(Student).where(Student.id == student_id))
    student = students.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await db.delete(student)
    await db.commit()
    return { "message": "Student deleted successfully" }







