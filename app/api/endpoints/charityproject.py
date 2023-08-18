from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_charity_project_exists, check_charity_project_deletable, \
    check_charity_project_before_edit, check_charity_project_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charityproject_crud
from app.schemas.charityproject import CharityProjectDB, CharityProjectUpdate, CharityProjectCreate
from app.services.charityproject_investing import charity_project_investing


router = APIRouter(prefix='/charity_project', tags=['charity_projects'])


@router.get('/', response_model=List[CharityProjectDB])
async def get_all_projects(session: AsyncSession = Depends(get_async_session)):
    return await charityproject_crud.get_multi(session)


@router.delete('/{project_id}',
               response_model=CharityProjectDB,
               dependencies=[Depends(current_superuser)])
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(project_id, session)
    await check_charity_project_deletable(charity_project)

    return await charityproject_crud.remove(charity_project, session)


@router.post('/',
             response_model=CharityProjectDB,
             dependencies=[Depends(current_superuser)])
async def create_charity_project(
        obj_in: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    await check_charity_project_duplicate(obj_in.name, session)
    charity_project = await charityproject_crud.create(obj_in, session)
    await charity_project_investing(charity_project, session)



@router.patch('/{project_id}',
              response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)])
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession
):
    charity_project = await check_charity_project_exists(project_id, session)
    await check_charity_project_before_edit(charity_project, obj_in)
    pass
