from datetime import datetime, date

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)


class FlightsModel(Base):
    __tablename__ = "flights"

    file_name: Mapped[str] = mapped_column(nullable=False)
    flt: Mapped[int] = mapped_column(nullable=False)
    depdate: Mapped[date] = mapped_column(nullable=False)
    dep: Mapped[str] = mapped_column(nullable=False)
