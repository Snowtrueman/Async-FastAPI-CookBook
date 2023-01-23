import models
import schemas
import uvicorn
from typing import List
from db import engine, async_session
from models import RecipeCategory, Recipes
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, HTTPException, Path, Body, Depends
from crud_recipes import get_with_cat, get_all, create, delete_, update_
from crud_cats import get_all_cats, get_all_by_cat, delete_cat, create_cat, update_cat

tags_metadata = [
    {
        "name": "Recipes",
        "description": "Operations with recipes.",
    },
    {
        "name": "Categories",
        "description": "Operations with categories.",
    },
]

description = """
CookBook API manages recipes divided by category and ordered by popularity(views).

## Recipes

You will be able to:

* View recipe by ID.
* View all recipes.
* View recipes by category.
* Update recipe by ID.
* Delete recipe by ID.
* Create new recipe.

## Categories

You will be able to:

* View all categories.
* Update category by ID.
* Delete category by ID.
* Create new category.
"""

app = FastAPI(title="CookBook", openapi_tags=tags_metadata, description=description)


async def get_session() -> AsyncSession:
    """
    Session getter.
    Returns:
        Asyncsession instance.
    """

    async with async_session() as session:
        yield session


@app.on_event("startup")
async def startup():
    """
    DB init.
    Returns:
        None.
    """

    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    """
    DB shutdown.
    Returns:
        None.
    """

    await engine.dispose()


# RECIPES ENDPOINTS


@app.get('/recipes/{recipe_id}', response_model=schemas.RecipeOut, tags=["Recipes"])
async def get_recipe(recipe_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_session)) -> Recipes:
    """
    Endpoint which returns recipe by provided ID.
    Args:
        recipe_id: Recipe ID.
        session: AsyncSession instance.

    Returns:
        Recipe object.
    """

    recipe = await get_with_cat(recipe_id, session)
    if recipe:
        updated_views = schemas.RecipeUpdate(id=recipe_id, views=recipe.views + 1)
        await update_recipe(updated_views, recipe_id, session)
        return recipe
    else:
        raise HTTPException(status_code=404, detail="Recipe with specified ID does not exist")


@app.get('/recipes/', response_model=List[schemas.RecipeOutList], tags=["Recipes"])
async def get_recipes(session: AsyncSession = Depends(get_session)) -> List[Recipes]:
    """
    Endpoint which returns all existing recipes.
    Args:
        session: AsyncSession instance.

    Returns:
        List of recipe objects.
    """

    recipes = await get_all(session)
    return recipes


@app.get('/categories/{category_id}', response_model=List[schemas.RecipeOutList], tags=["Recipes"])
async def get_recipe_by_category(category_id: int = Path(..., gt=0),
                                 session: AsyncSession = Depends(get_session)) -> List[Recipes]:
    """
    Endpoint which returns all existing recipes in provided category.
    Args:
        category_id: Category ID.
        session: AsyncSession instance.

    Returns:
        List of recipe objects.
    """

    recipes = await get_all_by_cat(category_id, session)
    if recipes:
        return recipes
    else:
        raise HTTPException(status_code=404, detail="There are no recipes in specified category")


@app.post('/recipes/', status_code=201, response_model=schemas.RecipeOut, tags=["Recipes"])
async def add_recipe(recipe: schemas.RecipeIn, session: AsyncSession = Depends(get_session)) -> Recipes:
    """
    Endpoint which creates a new recipe using provided data.
    Args:
        recipe: Data of new recipe serialized by RecipeIn schema.
        session: AsyncSession instance.

    Returns:
        Recipe object.
    """

    new_recipe = Recipes(**recipe.dict())
    recipe = await create(new_recipe, session)
    return recipe


@app.delete('/recipes/{recipe_id}', response_model=schemas.RecipeOut, tags=["Recipes"])
async def delete_recipe(recipe_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_session)) -> Recipes:
    """
    Endpoint which delete recipe by provided ID.
    Args:
        recipe_id: Recipe ID.
        session: AsyncSession instance.

    Returns:
        Recipe object.
    """

    deleted_recipe = await delete_(recipe_id, session)
    if deleted_recipe:
        return deleted_recipe
    else:
        raise HTTPException(status_code=404, detail="Recipe with specified ID does not exist")


@app.patch('/recipes/{recipe_id}', response_model=schemas.RecipeOut, tags=["Recipes"])
async def update_recipe(recipe: schemas.RecipeUpdate, recipe_id: int = Path(..., gt=0),
                        session: AsyncSession = Depends(get_session)) -> Recipes:
    """
    Endpoint which updated recipe with provided data by provided ID.
    Args:
        recipe: Data to be updated serialized by RecipeUpdate schema.
        recipe_id: Recipe ID.
        session: AsyncSession instance.

    Returns:
        Recipe object.
    """

    updated_recipe = await update_(recipe, recipe_id, session)
    if updated_recipe:
        return updated_recipe
    else:
        raise HTTPException(status_code=404, detail="Recipe with specified ID does not exist")


# CATEGORIES ENDPOINTS


@app.get('/categories/', response_model=List[schemas.BaseCategory], tags=["Categories"])
async def get_categories(session: AsyncSession = Depends(get_session)) -> List[RecipeCategory]:
    """
    Endpoint which returns all existing categories.
    Args:
        session: AsyncSession instance.

    Returns:
        List of recipeCategory objects.
    """

    recipes = await get_all_cats(session)
    return recipes


@app.delete('/categories/{category_id}', response_model=schemas.BaseCategory, tags=["Categories"])
async def delete_category(category_id: int = Path(..., gt=0),
                          session: AsyncSession = Depends(get_session)) -> RecipeCategory:
    """
    Endpoint which delete category by provided ID.
    Args:
        category_id: Category ID.
        session: AsyncSession instance.

    Returns:
        RecipeCategory object.
    """

    category = await delete_cat(category_id, session)
    if category:
        return category
    else:
        raise HTTPException(status_code=404, detail="Category with specified ID does not exist")


@app.post('/categories/', status_code=201, response_model=schemas.BaseCategory, tags=["Categories"],
          operation_id="CreateCategory")
async def create_category(title: str = Body(..., min_length=3, max_length=50, embed=True),
                          session: AsyncSession = Depends(get_session)) -> RecipeCategory:
    """
    Endpoint which creates new category by provided title.
    Args:
        title: Category title.
        session: AsyncSession instance.

    Returns:
        RecipeCategory object.
    """

    category = await create_cat(title, session)
    if category:
        return category
    else:
        raise HTTPException(status_code=400, detail="Category with specified name already exists")


@app.patch('/categories/{category_id}', response_model=schemas.BaseCategory, tags=["Categories"],
           operation_id="UpdateCategory")
async def update_category(category_id: int = Path(..., gt=0),
                          title: str = Body(..., min_length=3, max_length=50, embed=True),
                          session: AsyncSession = Depends(get_session)) -> RecipeCategory:
    """
    Endpoint which updates the category title.
    Args:
        category_id: Category ID.
        title: The new title.
        session: AsyncSession instance.

    Returns:
        RecipeCategory object.
    """

    category = await update_cat(title, category_id, session)
    if category:
        return category
    else:
        raise HTTPException(status_code=404, detail="Category with specified ID does not exist")


if __name__ == "__main__":
    uvicorn.run(app)
