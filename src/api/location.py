from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.database import get_db
from src.repositories.location import LocationRepository
from src.schemas.location import Location, LocationCreate, LocationUpdate
from src.api.dependencies import get_current_user, get_current_admin

from src.use_cases.location.get_all_locations import GetAllLocationsUseCase
from src.use_cases.location.get_location_by_id import GetLocationByIdUseCase
from src.use_cases.location.create_location import CreateLocationUseCase
from src.use_cases.location.update_location import UpdateLocationUseCase
from src.use_cases.location.delete_location import DeleteLocationUseCase

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/", response_model=List[Location], summary="Get All Locations")
async def get_locations(session: AsyncSession = Depends(get_db)):
    repo = LocationRepository(session)
    return await GetAllLocationsUseCase(repo).execute()

@router.post("/", response_model=Location, status_code=status.HTTP_201_CREATED, summary="Create Location")
async def create_location(
    loc_in: LocationCreate, 
    session: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    repo = LocationRepository(session)
    return await CreateLocationUseCase(repo).execute(loc_in)

@router.get("/{id}", response_model=Location, summary="Get Location By Id")
async def get_location(id: int, session: AsyncSession = Depends(get_db)):
    repo = LocationRepository(session)
    return await GetLocationByIdUseCase(repo).execute(id)

@router.patch("/{id}", response_model=Location, summary="Update Location")
async def update_location(
    id: int, 
    loc_in: LocationUpdate, 
    session: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    repo = LocationRepository(session)
    return await UpdateLocationUseCase(repo).execute(id, loc_in)

@router.delete("/{id}", status_code=status.HTTP_200_OK, summary="Delete Location")
async def delete_location(
    id: int, 
    session: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    repo = LocationRepository(session)
    return await DeleteLocationUseCase(repo).execute(id)