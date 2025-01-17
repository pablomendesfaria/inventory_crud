from controller.routes import router
from fastapi import FastAPI
from models.database import Base, engine

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix='/api', tags=['inventory'])
