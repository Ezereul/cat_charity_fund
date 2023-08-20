from datetime import datetime

from sqlalchemy import (
    ForeignKey, Column, Integer, Text, CheckConstraint, DateTime, Boolean
)

from app.core.db import Base


class Donation(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    close_date = Column(DateTime)
    __table_args__ = (
        CheckConstraint('full_amount > 0', name='full_amount_positive'),
        CheckConstraint('invested_amount >= 0',
                        name='invested_amount_positive'),
        CheckConstraint('invested_amount <= full_amount',
                        name='invested_amount_lte_full_amount'),
    )

    def __repr__(self):
        return (f"<Donation(user_id={self.user_id}, "
                f"comment='{self.comment}', "
                f"full_amount={self.full_amount}, "
                f"invested_amount={self.invested_amount}, "
                f"fully_invested={self.fully_invested})>")
