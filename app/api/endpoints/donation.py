from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charityproject import charityproject_crud
from app.models import User
from app.schemas.donation import DonationDB, DonationUser, DonationCreate
from app.crud.donation import donation_crud
from app.services.investing import distribute_investment

router = APIRouter()


@router.get('/',
            response_model=List[DonationDB],
            dependencies=[Depends(current_superuser)],
            response_model_exclude_none=True)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_multi(session)


@router.get('/my', response_model=List[DonationUser])
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return await donation_crud.get_by_user(session, user)


@router.post('/',
             response_model=DonationUser,
             response_model_exclude_none=True)
async def create_donation(
        obj_in: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    donation = await donation_crud.create(obj_in, session, user, False)
    opened_projects = await charityproject_crud.get_open_investments(session)
    changed_projects = distribute_investment(donation, opened_projects)

    session.add_all(changed_projects)
    await session.commit()
    await session.refresh(donation)
    return donation
