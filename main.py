from fastapi import FastAPI
from database.data import engine, Base
from controllers.SchoolController import router as school_router


app = FastAPI(title="School API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(school_router)


