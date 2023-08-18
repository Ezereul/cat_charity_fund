from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.models import User
from app.schemas.donation import DonationDB, DonationUser
from app.crud.donation import donation_crud


router = APIRouter(prefix='/donation', tags=['donations'])


@router.get('/',
            response_model=List[DonationDB],
            dependencies=[Depends(current_superuser)])
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    return await donation_crud.get_multi(session)


@router.get('/my', response_model=List[DonationDB])
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return await donation_crud.get_by_user(session, user)


@router.post('/',
             response_model=DonationUser)
async def create_donation(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    pass
