from datetime import date

from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class FlightsModel(Base):
    __tablename__ = "flights"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(nullable=False)
    flt: Mapped[int] = mapped_column(nullable=False)
    depdate: Mapped[date] = mapped_column(nullable=False)
    dep: Mapped[str] = mapped_column(nullable=False)
