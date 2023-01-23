import schemas
from typing import List
from sqlalchemy import update
from sqlalchemy import select, case
from models import Recipes, RecipeCategory
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all(session: AsyncSession) -> List[Recipes]:
    """
    Returns all existing recipes with category name.
    Args:
        session: AsyncSession instance.

    Returns:
        List of Recipe objects.
    """

    recipes = await session.execute(select(Recipes.id, Recipes.title,
                                           (case([
                                               (RecipeCategory.title is not None, RecipeCategory.title)
                                           ],
                                               else_=Recipes.category))
                                           .label(
                                               "category"),
                                           Recipes.cooking_time, Recipes.views).outerjoin(RecipeCategory)
                                    .order_by(Recipes.views.desc(), Recipes.cooking_time))
    return recipes.all()


async def get_(recipe_id: int, session: AsyncSession) -> Recipes:
    """
    Returns recipe by ID.
    Args:
        recipe_id: Recipe ID.
        session: AsyncSession instance.

    Returns:
        Recipe object.
    """

    recipe = await session.execute(select(Recipes).where(Recipes.id == recipe_id))
    return recipe.scalar()


async def get_with_cat(recipe_id: int, session: AsyncSession, ) -> Recipes:
    """
        Returns recipe by ID with category name.
    Args:
        recipe_id: Recipe ID.
        session: AsyncSession instance.

    Returns:
        Recipe object.
    """

    recipe = await session.execute(select(Recipes.id, Recipes.title,
                                          (case([
                                              (RecipeCategory.title is not None, RecipeCategory.title)
                                          ],
                                              else_=Recipes.category))
                                          .label(
                                              "category"),
                                          Recipes.cooking_time, Recipes.ingredients, Recipes.description, Recipes.views)
                                   .outerjoin(RecipeCategory)
                                   .where(Recipes.id == recipe_id))
    return recipe.one_or_none()


async def delete_(recipe_id: int, session: AsyncSession) -> Recipes | None:
    """
    Delete recipe by provided ID.
    Args:
        recipe_id: Recipe ID.
        session: AsyncSession instance.

    Returns:
        Deleted recipe or None if recipe with provided ID not found.
    """

    recipe = await get_(recipe_id, session)
    if recipe:
        await session.delete(recipe)
        await session.commit()
        return recipe
    else:
        return None


async def update_(recipe: schemas.RecipeUpdate, recipe_id: int, session: AsyncSession) -> Recipes | None:
    """
    Updates recipe data.
    Args:
        recipe: Data to update.
        recipe_id: Recipe ID.
        session: AsyncSession instance.

    Returns:
        Recipe object or None if recipe with provided ID not found.
    """

    new_data = recipe.dict(exclude_unset=True)
    current_recipe = await get_(recipe_id, session)
    if current_recipe:
        recipe_model = schemas.RecipeUpdate(**current_recipe.__dict__)
        new_recipe = recipe_model.copy(update=new_data)
        await session.execute(update(Recipes).where(Recipes.id == recipe_id).values(jsonable_encoder(new_recipe)))
        await session.commit()
        return await get_(recipe_id, session)
    else:
        return None


async def create(recipe: Recipes, session: AsyncSession) -> Recipes:
    """
    Creates new recipe.
    Args:
        recipe: Data of new recipe in recipe object.
        session: AsyncSession instance.

    Returns:
        Recipe object.
    """

    session.add(recipe)
    await session.commit()
    return recipe
