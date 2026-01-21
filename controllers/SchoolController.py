from fastapi import APIRouter, Depends, HTTPException
from pyexpat.errors import messages
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database.data import AsyncSessionLocal
from models.School import School
from models.Student import Student
from schema.SchoolSchema import SchoolCreate, SchoolResponse,SchoolWithStudents
from schema.StudentSchema import StudentCreate, StudentUpdate , StudentResponse

router = APIRouter(
    prefix="api/schools",
    tags=["Schools"]
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/")
async def add_school(
    school: SchoolCreate,
    db: AsyncSession = Depends(get_db)
):
    new_school = School(
        name=school.name,
        founding_date=school.founding_date,
        address=school.address,
        city=school.city
    )
    db.add(new_school)
    await db.commit()
    await db.refresh(new_school)
    return { "messages" : "School added successfully ",
             "data" : new_school}

@router.get("/",response_model=list[SchoolResponse])
async  def get_schools(db: AsyncSession = Depends(get_db)):
    schools = await db.execute(select(School))
    return  schools.scalars().all()

@router.get("/{school_id}",response_model=SchoolResponse)
async def get_school(school_id: int,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(School).where(School.id == school_id))
    school = result.scalar_one_or_none()
    if school is None:
        raise HTTPException(status_code=404, detail="School not found")
    return school

@router.get("/{school_id}/students/",response_model=SchoolWithStudents)
async def get_school_with_students(school_id: int,db: AsyncSession = Depends(get_db)):
    result= await db.execute(select(School).where(
        School.id == school_id).options(selectinload(School.students)))

    school = result.scalar_one_or_none()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school

@router.delete("/{school_id}")
async def delete_school(school_id: int,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(School).where(School.id == school_id))
    school = result.scalar_one_or_none()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    await db.delete(school)
    await db.commit()
    return { "messages" : "School deleted successfully" }


@router.post("/{school_id}/students")
async def add_student(
    student: StudentCreate,
    school_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(School).where(School.id == school_id)
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
        school_id= school_id
    )
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return { "message": "Student added successfully" ,
             "student": new_student }


@router.get("/{school_id}/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id : int ,
                      school_id : int ,
                      db: AsyncSession = Depends(get_db)):
    students = await db.execute(select(Student).where(Student.id == student_id and  Student.school_id == school_id))
    return  students.scalars().all()



@router.put("/{school_id}/students/{student_id}", response_model=StudentResponse)
async def update_student(
        student_id : int ,
        school_id : int ,
        payload: StudentUpdate,
        db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id and Student.school_id == school_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(student, key, value)

    await db.commit()
    await db.refresh(student)
    return student


@router.delete("/{school_id}/students/{student_id}")
async def delete_student(
        student_id: int ,
        school_id : int ,
        db: AsyncSession = Depends(get_db)):
    students = await db.execute(select(Student).where(Student.id == student_id and Student.school_id == school_id))
    student = students.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await db.delete(student)
    await db.commit()
    return { "message": "Student deleted successfully" }






