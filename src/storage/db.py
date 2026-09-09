from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite://", echo=True)

with Session(engine) as session:
    