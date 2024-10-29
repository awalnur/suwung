import cProfile
from app.db.base import Base
from app.db.session import engine
from app.main import app

app = app


if __name__ == "__main__":
    import uvicorn

    Base.metadata.create_all(bind=engine)
    cProfile.run('uvicorn.run("main:app", host="0.0.0.0" , port=8000, reload=True)')
                # log_config=None