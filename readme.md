# Async FastAPI CookBook

API для кулинарной книги. Позволяет управлять рецептами в кулинарной книге, а также их категориями. Рецепты ранжируются 
в зависимости от их популярности (количества просмотров).


### Recipes
Предоставляет возможность для:

+ Просмотра рецепта по ID;
+ Просмотра всех существующих рецептов;
+ Просмотра рецептов в конкретной категории;
+ Обновления рецепта по указанному ID;
+ Удаления рецепта по указанному ID;
+ Создания нового рецепта.
 
### Categories
Предоставляет возможность для:

+ View all categories;
+ Update category by ID;
+ Delete category by ID;
+ Create new category.

### Структура проекта
### main.py
+ Основной модуль проекта;
+ Содержит все эндпоинты.

### models.py
+ Содержит модели базы данных `Recipes` и `RecipeCategory`.

### schemas.py
+ Содержит сериализаторы данных.

### crud_cats.py
+ CRUD операции для модели `RecipeCategory`.

### crud_recipes.py
+ CRUD операции для модели `Recipes`.

### db.py
+ Создает соединение с БД;
+ Создает объект сессии.

### test_categories.py
+ Тесты для эндпоинтов, затрагивающих объекты категорий рецептов.

### test_recipes.py
+ Тесты для эндпоинтов, затрагивающих объекты рецептов.




# Async FastAPI CookBook

CookBook API manages recipes divided by category and ordered by popularity(views).

### Recipes
You will be able to:

+ View recipe by ID;
+ View all recipes;
+ View recipes by category;
+ Update recipe by ID;
+ Delete recipe by ID;
+ Create new recipe.
 
### Categories
You will be able to:

+ View all categories;
+ Update category by ID;
+ Delete category by ID;
+ Create new category.

### Project structure
### main.py
+ Main module;
+ Include all endpoints handlers;

### models.py
+ Contains models `Recipes` and `RecipeCategory`.

### schemas.py
+ Contains serialization schemas.

### crud_cats.py
+ CRUD operations for `RecipeCategory` objects.

### crud_recipes.py
+ CRUD operations for `Recipes` objects.

### db.py
+ Creates connection to database;
+ Creates session.

### test_categories.py
+ Tests for category endpoints.

### test_recipes.py
+ Tests for recipe endpoints.