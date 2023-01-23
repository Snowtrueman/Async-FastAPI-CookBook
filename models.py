from db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Text, ForeignKey


class RecipeCategory(Base):
    """
    Model describing recipe category.
    """

    __tablename__ = "recipe_cat"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    recipes = relationship("Recipes", cascade="all", backref="recipe_cat")


class Recipes(Base):
    """
    Model describing recipe.
    """

    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    category = Column(Integer, ForeignKey("recipe_cat.id"))
    cooking_time = Column(Integer, index=True, nullable=False)
    ingredients = Column(Text, index=True, nullable=False)
    description = Column(Text, index=True, nullable=False)
    views = Column(Integer, index=True, default=0)

