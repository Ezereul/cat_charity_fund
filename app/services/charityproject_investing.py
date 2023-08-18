from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.crud.donation import donation_crud


async def charity_project_investing(
        charity_project: CharityProject,
        session: AsyncSession
):
    donations = await donation_crud.get_opened_donations(session)
    for donation in donations:
        free_amount = donation.full_amount - donation.invested_amount
        required_amount = charity_project.full_amount - charity_project.invested_amount
        if required_amount >= free_amount:
            charity_project.invested_amount += free_amount
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            donation.close_date = datetime.utcnow()
        else:
            pass
