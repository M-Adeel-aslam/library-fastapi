from fastapi import FastAPI
from routes import authentication, Works, supports, Joins
from database import create_all_tables

# lol
create_all_tables()
app = FastAPI()

app.include_router(authentication.router)
app.include_router(Works.router)
app.include_router(supports.router)
app.include_router(Joins.router)
