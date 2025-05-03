from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, EventModel

# Создаём движок SQLite
engine = create_engine(
    "sqlite:///laba5.db",
    connect_args={"check_same_thread": False}
)

# Отключаем expire_on_commit, чтобы объекты не «протухали» после коммита
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def init_db():
    Base.metadata.create_all(bind=engine)

class EventStore:
    def __init__(self):
        self.Session = SessionLocal

    def append(self, aggregate_id: str, event_type: str, data: dict):
        db = self.Session()
        ev = EventModel(
            aggregate_id=aggregate_id,
            event_type=event_type,
            event_data=data
        )
        db.add(ev)
        db.commit()
        db.close()
        return ev

    def load(self, aggregate_id: str):
        db = self.Session()
        evs = (
            db.query(EventModel)
              .filter_by(aggregate_id=aggregate_id)
              .order_by(EventModel.id)
              .all()
        )
        db.close()
        return evs
