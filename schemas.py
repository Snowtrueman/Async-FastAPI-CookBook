from pydantic import BaseModel, Field


class BaseRecipe(BaseModel):
    """
    Basic model for recipe serialization.
    """

    title: str = Field(..., min_length=3, max_length=50)
    cooking_time: int = Field(..., gt=0)
    ingredients: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3)


class RecipeOutList(BaseModel):
    """
    Model for serialization the outgoing recipes list.
    """

    title: str = Field(..., min_length=3, max_length=50)
    cooking_time: int = Field(..., gt=0)
    category: str | None = Field(...)
    views: int = Field(..., gte=0)
    id: int = Field(..., gt=0)

    class Config:
        orm_mode = True


class RecipeIn(BaseRecipe):
    """
    Model for serialization the input data when creating the new recipe.
    """

    category: int = Field(..., gt=0)

    class Config:
        orm_mode = True


class RecipeOut(BaseRecipe):
    """
    The outgoing recipe object serialization .
    """

    category: str | None = Field(...)
    views: int = Field(..., gte=0)
    id: int = Field(..., gt=0)

    class Config:
        orm_mode = True


class RecipeUpdate(BaseModel):
    """
    Model for serialization the input data when updating recipe.
    """

    title: str | None = Field(min_length=3, max_length=50)
    category: int | None = Field(gte=0)
    cooking_time: int | None = Field(gt=0)
    ingredients: str | None = Field(min_length=3)
    description: str | None = Field(min_length=3)

    class Config:
        orm_mode = True


class BaseCategory(BaseModel):
    """
    Basic model for recipe category serialization.
    """

    id: int = Field(..., gt=0)
    title: str = Field(min_length=3, max_length=50)

    class Config:
        orm_mode = True
