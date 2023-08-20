from datetime import datetime
from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.scalars(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.first()

    async def get_multi(
            self,
            session: AsyncSession,
    ):
        db_obj = await session.scalars(select(self.model))
        return db_obj.all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
            to_commit: bool = True
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(
            **obj_in_data, invested_amount=0, create_date=datetime.utcnow()
        )
        session.add(db_obj)
        if to_commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        if update_data.get('full_amount') and update_data.get('full_amount') == db_obj.invested_amount:
            setattr(db_obj, 'fully_invested', True)
            setattr(db_obj, 'close_date', datetime.utcnow())

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_open_investments(
            self,
            session: AsyncSession
    ):
        open_projects = await session.scalars(
            select(self.model).where(self.model.fully_invested == False) # noqa
        )
        return open_projects.all()
