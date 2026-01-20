from fastapi import APIRouter, Depends, HTTPException
from pyexpat.errors import messages
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database.data import AsyncSessionLocal
from models.School import School
from schema.SchoolSchema import SchoolCreate, SchoolResponse,SchoolWithStudents

router = APIRouter(
    prefix="/school",
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








