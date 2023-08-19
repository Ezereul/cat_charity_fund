from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class DonationCRUD(CRUDBase):
    async def get_by_user(
            self,
            session: AsyncSession,
            user: User,
    ):
        donations = await session.scalars(
            select(self.model).where(self.model.user_id == user.id)
        )
        return donations.all()

    async def get_opened_donations(
            self,
            session: AsyncSession,
    ) -> List[Donation]:
        donations = await session.scalars(
            select(self.model).where(self.model.fully_invested == False) # noqa
        )
        return donations.all()


donation_crud = DonationCRUD(Donation)
