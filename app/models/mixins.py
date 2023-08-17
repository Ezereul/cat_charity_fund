from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Boolean


class CharityDonationMixin:
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    close_date = Column(DateTime)
