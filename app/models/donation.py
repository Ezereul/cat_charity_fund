from sqlalchemy import ForeignKey, Column, Integer, Text

from app.core.db import Base
from app.models.mixins import CharityDonationMixin


class Donation(CharityDonationMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
