from datetime import datetime
from typing import Union, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, CharityProject


async def mark_as_fully_invested(investment_target: Union[CharityProject, Donation]):
    investment_target.fully_invested = True
    investment_target.close_date = datetime.utcnow()
    investment_target.invested_amount = investment_target.full_amount


async def distribute_investment(
        investment_source: Union[Donation, CharityProject],
        investment_targets: List[Union[Donation, CharityProject]],
        session: AsyncSession,
) -> Union[Donation, CharityProject]:
    for target in investment_targets:
        required_amount = target.full_amount - target.invested_amount
        available_amount = investment_source.full_amount - investment_source.invested_amount
        if required_amount > available_amount:
            target.invested_amount += available_amount
            await mark_as_fully_invested(investment_source)
            break
        else:
            investment_source.invested_amount += required_amount
            await mark_as_fully_invested(target)
    if investment_source.invested_amount == investment_source.full_amount:
        await mark_as_fully_invested(investment_source)
    await session.commit()
    await session.refresh(investment_source)
    return investment_source
