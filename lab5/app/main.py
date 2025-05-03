from fastapi import FastAPI
from app.event_store import init_db
from app.routers import commands, queries

app = FastAPI(title="Balance CQRS+ES Service")
init_db()

app.include_router(commands.router)
app.include_router(queries.router)
