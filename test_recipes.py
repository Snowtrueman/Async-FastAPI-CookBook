import json
import pytest
import crud_cats
import crud_recipes
from main import app
from models import Recipes
from starlette.testclient import TestClient


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


def test_create_recipe(test_app, monkeypatch):
    test_request_payload = {"title": "Category"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud_cats, "create_cat", mock_post)

    response = test_app.post("/categories/", content=json.dumps(test_request_payload), )

    test_request_payload = \
        {"title": "Title", "cooking_time": 5, "category": "1", "ingredients": "ingredients",
         "description": "description"}
    test_response_payload = \
        {"id": 1, "title": "Title", "cooking_time": 5, "category": "1",
         "ingredients": "ingredients", "description": "description", "views": 0}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud_recipes, "create", mock_post)

    response = test_app.post("/recipes/", content=json.dumps(test_request_payload), )

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_recipe_invalid_json(test_app):
    response = test_app.post("/recipes/",
                             content=json.dumps({"title": "Title", "cooking_time": 0, "category": "1",
                                                 "ingredients": "ingredients"}, ))
    assert response.status_code == 422


def test_read_recipe_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud_recipes, "get_", mock_get)

    response = test_app.get("/recipes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe with specified ID does not exist"

    response = test_app.get("/recipes/0")
    assert response.status_code == 422


def test_read_recipe(test_app, monkeypatch):
    test_data = \
        {"id": 1, "title": "Title", "cooking_time": 5, "category": "1",
         "ingredients": "ingredients", "description": "description", "views": 0}

    async def mock_get(id, session):
        r = Recipes(**test_data)
        return r

    monkeypatch.setattr(crud_recipes, "get_", mock_get)

    response = test_app.get("/recipes/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Title", "cooking_time": 5, "category": "Category",
                               "ingredients": "ingredients", "description": "description", "views": 0}


def test_read_all_recipes(test_app, monkeypatch):
    test_request_payload = \
        {"title": "Title_2", "cooking_time": 5, "category": "1", "ingredients": "ingredients",
         "description": "description"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud_recipes, "create", mock_post)

    response = test_app.post("/recipes/", content=json.dumps(test_request_payload), )

    test_response_payload = \
        [{"id": 2, "title": "Title_2", "cooking_time": 5, "category": "Category", "views": 0},
         {"id": 1, "title": "Title", "cooking_time": 5, "category": "Category", "views": 0},
         ]

    async def mock_get_all(session):
        return test_response_payload

    monkeypatch.setattr(crud_recipes, "get_all", mock_get_all)

    response = test_app.get("/recipes/")
    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_read_all_recipes_by_cat(test_app, monkeypatch):
    test_response_payload = \
        [{"id": 2, "title": "Title_2", "cooking_time": 5, "category": "Category", "views": 0},
         {"id": 1, "title": "Title", "cooking_time": 5, "category": "Category", "views": 0},
         ]

    async def mock_get_all(session):
        return test_response_payload

    monkeypatch.setattr(crud_recipes, "get_with_cat", mock_get_all)

    response = test_app.get("/categories/1")
    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_update_recipe(test_app, monkeypatch):
    test_data = \
        {"id": 1, "title": "New_title", "cooking_time": 5, "category": "1",
         "ingredients": "ingredients", "description": "description", "views": 0}

    async def mock_get(id, session):
        r = Recipes(**test_data)
        return r

    monkeypatch.setattr(crud_recipes, "get_", mock_get)

    async def mock_patch(id, payload):
        return 1

    monkeypatch.setattr(crud_recipes, "update_", mock_patch)

    response = test_app.patch("/recipes/1/", content=json.dumps({"title": "New_title"}))
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_recipe_invalid_path(test_app, monkeypatch):
    async def mock_get(id, session):
        return None

    monkeypatch.setattr(crud_recipes, "get_", mock_get)

    async def mock_patch(id, payload):
        return 1

    monkeypatch.setattr(crud_recipes, "update_", mock_patch)

    response = test_app.patch("/recipes/100/", content=json.dumps({"title": "New_category"}))
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe with specified ID does not exist"


def test_update_recipe_invalid_json(test_app, monkeypatch):
    test_data = \
        {"id": 1, "title": "New_title", "cooking_time": 5, "category": "1",
         "ingredients": "ingredients", "description": "description", "views": 0}

    async def mock_get(id, session):
        r = Recipes(**test_data)
        return r

    monkeypatch.setattr(crud_recipes, "get_", mock_get)

    async def mock_patch(id, payload):
        return 1

    monkeypatch.setattr(crud_recipes, "update_", mock_patch)
    response = test_app.patch("/recipes/1/", content=json.dumps({"title": ""}))
    assert response.status_code == 422


def test_delete_recipe(test_app, monkeypatch):
    test_data = \
        {"id": 1, "title": "New_title", "cooking_time": 5, "category": "1",
         "ingredients": "ingredients", "description": "description", "views": 0}
    r = Recipes(**test_data)
    async def mock_delete(id, session):
        return r

    monkeypatch.setattr(crud_recipes, "delete_", mock_delete)

    response = test_app.delete("/recipes/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_delete_recipe_invalid_id(test_app, monkeypatch):
    async def mock_get(id, session):
        return None

    monkeypatch.setattr(crud_recipes, "get_", mock_get)

    async def mock_delete(id):
        return 1

    monkeypatch.setattr(crud_recipes, "delete_", mock_delete)

    response = test_app.delete("/recipes/100/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe with specified ID does not exist"
