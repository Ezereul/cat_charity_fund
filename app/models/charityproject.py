from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.models.mixins import CharityDonationMixin


class CharityProject(CharityDonationMixin, Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
