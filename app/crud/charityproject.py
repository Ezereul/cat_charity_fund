from datetime import datetime
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CharityProjectCRUD(CRUDBase):
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

    async def get_project_by_name(
            self,
            name: str,
            session: AsyncSession
    ):
        project = await session.scalars(
            select(self.model).where(self.model.name == name)
        )
        return project.first()

    async def get_open_projects(
            self,
            session: AsyncSession
    ) -> List[CharityProject]:
        open_projects = await session.scalars(
            select(self.model).where(self.model.fully_invested == False)
        )
        return open_projects.all()


charityproject_crud = CharityProjectCRUD(CharityProject)
