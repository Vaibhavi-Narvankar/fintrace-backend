from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables at startup
    Base.metadata.create_all(bind=engine)
    yield
    # (optional cleanup code here)


app = FastAPI(lifespan=lifespan)


app.include_router(router)

@app.get("/")
def test_db():
    try:
        connection = engine.connect()
        connection.close()
        return {"message": "DB connected successfully"}
    except Exception as e:
        return {"error": str(e)}

