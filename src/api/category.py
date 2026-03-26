from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.repositories.category import CategoryRepository
from src.schemas.category import Category, CategoryCreate, CategoryUpdate

from src.use_cases.category.get_all_categories import GetAllCategoriesUseCase
from src.use_cases.category.get_category_by_id import GetCategoryByIdUseCase
from src.use_cases.category.create_category import CreateCategoryUseCase
from src.use_cases.category.update_category import UpdateCategoryUseCase
from src.use_cases.category.delete_category import DeleteCategoryUseCase

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[Category])
async def get_categories(session: AsyncSession = Depends(get_db)):
    repo = CategoryRepository(session)
    return await GetAllCategoriesUseCase(repo).execute()

@router.post("/", response_model=Category, status_code=201)
async def create_category(cat_in: CategoryCreate, session: AsyncSession = Depends(get_db)):
    repo = CategoryRepository(session)
    return await CreateCategoryUseCase(repo).execute(cat_in)

@router.get("/{id}", response_model=Category)
async def get_category(id: int, session: AsyncSession = Depends(get_db)):
    repo = CategoryRepository(session)
    return await GetCategoryByIdUseCase(repo).execute(id)

@router.patch("/{id}", response_model=Category)
async def update_category(id: int, cat_in: CategoryUpdate, session: AsyncSession = Depends(get_db)):
    repo = CategoryRepository(session)
    return await UpdateCategoryUseCase(repo).execute(id, cat_in)

@router.delete("/{id}")
async def delete_category(id: int, session: AsyncSession = Depends(get_db)):
    repo = CategoryRepository(session)
    return await DeleteCategoryUseCase(repo).execute(id)