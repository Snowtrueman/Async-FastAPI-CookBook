from typing import List
from sqlalchemy import select
from models import RecipeCategory, Recipes
from sqlalchemy.ext.asyncio import AsyncSession


async def get_(category_id: int, session: AsyncSession) -> RecipeCategory:
    """
    Returns Category by ID.
    Args:
        category_id: Category ID.
        session: AsyncSession instance.

    Returns:
        RecipeCategory object.
    """

    category = await session.execute(select(RecipeCategory).where(RecipeCategory.id == category_id))
    return category.scalar()


async def get_all_cats(session: AsyncSession) -> List[RecipeCategory]:
    """
    Returns all existing categories.
    Args:
        session: AsyncSession instance.

    Returns:
        List of RecipeCategory objects.
    """

    cats = await session.execute(select(RecipeCategory))
    return cats.scalars().all()


async def get_all_by_cat(category: int, session: AsyncSession) -> List[Recipes]:
    """
    Returns all recipes in required category.
    Args:
        category: Category ID.
        session: AsyncSession instance.

    Returns:
        List of Recipe objects.
    """

    recipes = await session.execute(select(Recipes.id, Recipes.title, RecipeCategory.title.label("category"),
                                           Recipes.cooking_time, Recipes.views).join(RecipeCategory)
                                    .where(Recipes.category == category)
                                    .order_by(Recipes.views.desc(), Recipes.cooking_time))
    return recipes.all()


async def delete_cat(category_id: int, session: AsyncSession) -> RecipeCategory | None:
    """
    Delete category by ID.
    Args:
        category_id: Category ID.
        session: AsyncSession instance.

    Returns:
        Deleted category or None if category with provided ID not found.
    """

    category = await get_(category_id, session)
    if category:
        await session.delete(category)
        await session.commit()
        return category
    else:
        return None


async def create_cat(title: str, session: AsyncSession) -> RecipeCategory | None:
    """
    Creates new category with provided title.
    Args:
        title: The title of new category.
        session: AsyncSession instance.

    Returns:
        RecipeCategory object or None if category with provided title already exists.
    """

    exists = await session.execute(select(RecipeCategory).where(RecipeCategory.title.ilike(title)))
    if exists.scalar():
        return None
    else:
        category = RecipeCategory(title=title)
        session.add(category)
        await session.commit()
        return category


async def update_cat(title: str, category_id: int, session: AsyncSession) -> RecipeCategory | None:
    """
    Updates title of existing category.
    Args:
        title: The category new title.
        category_id: Category ID.
        session: AsyncSession instance.

    Returns:
        RecipeCategory object or None if category with provided ID not found.
    """

    category = await get_(category_id, session)
    if category:
        category.title = title
        await session.commit()
        return category
    else:
        return None
