from fastapi import HTTPException

class GetCategoryByIdUseCase:
    def __init__(self, repo):
        self.repo = repo

    async def execute(self, cat_id: int):
        db_cat = await self.repo.get_by_id(cat_id)
        if not db_cat:
            raise HTTPException(status_code=404, detail="Category not found")
        return db_cat