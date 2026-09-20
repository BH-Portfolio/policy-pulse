from sqlalchemy import String, Float, Integer
from sqlalchemy import CheckConstraint
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class RateRecord(Base):

    __tablename__ = "rate_records"

    __table_args__ = (
        UniqueConstraint("state", "sector", "period", name="uq_state_sector_period"),
        CheckConstraint("length(state) = 2", name="ck_state_two_letters"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    state: Mapped[str] = mapped_column(String(2))
    sector: Mapped[str] = mapped_column(String(10))
    period: Mapped[str] = mapped_column(String(10))
    price_cents_per_kwh: Mapped[float] = mapped_column(Float)
    sales_million_kwh: Mapped[float] = mapped_column(Float)

