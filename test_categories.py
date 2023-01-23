import json
import pytest
import crud_cats
from main import app
from models import RecipeCategory
from starlette.testclient import TestClient


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


def test_create_category(test_app, monkeypatch):
    test_request_payload = {"title": "Category"}
    test_response_payload = {"id": 1, "title": "Category"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud_cats, "create_cat", mock_post)

    response = test_app.post("/categories/", content=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_category_invalid_json(test_app):
    response = test_app.post("/categories/", content=json.dumps({"title": ""},))
    assert response.status_code == 422


def test_read_category_incorrect_id(test_app, monkeypatch):
    async def mock_get(id, session):
        return None

    monkeypatch.setattr(crud_cats, "get_", mock_get)

    response = test_app.get("/categories/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "There are no recipes in specified category"

    response = test_app.get("/categories/0")
    assert response.status_code == 422


def test_read_all_categories(test_app, monkeypatch):
    test_data = [
        {"id": 1, "title": "Category"},
    ]

    async def mock_get_all(session):
        return test_data

    monkeypatch.setattr(crud_cats, "get_all_cats", mock_get_all)

    response = test_app.get("/categories/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_category(test_app, monkeypatch):
    test_response_data = {"id": 1, "title": "New_category"}

    async def mock_get(id, session):
        r = RecipeCategory(**test_response_data)
        return r

    monkeypatch.setattr(crud_cats, "get_", mock_get)

    async def mock_patch(id, payload):
        return 1

    monkeypatch.setattr(crud_cats, "update_cat", mock_patch)

    response = test_app.patch("/categories/1/", content=json.dumps({"title": "New_category"}))
    assert response.status_code == 200
    assert response.json() == test_response_data


def test_update_category_invalid_path(test_app, monkeypatch):
    async def mock_get(id, session):
        return None

    monkeypatch.setattr(crud_cats, "get_", mock_get)

    async def mock_patch(id, payload):
        return 1

    monkeypatch.setattr(crud_cats, "update_cat", mock_patch)

    response = test_app.patch("/categories/100/", content=json.dumps({"title": "New_category"}))
    assert response.status_code == 404
    assert response.json()["detail"] == "Category with specified ID does not exist"


def test_update_category_invalid_json(test_app, monkeypatch):
    test_response_data = {"id": 1, "title": "New_category"}

    async def mock_get(id, session):
        r = RecipeCategory(**test_response_data)
        return r

    monkeypatch.setattr(crud_cats, "get_", mock_get)

    async def mock_patch(id, payload):
        return 1

    monkeypatch.setattr(crud_cats, "update_cat", mock_patch)
    response = test_app.patch("/categories/1/", content=json.dumps({"title": ""}))
    assert response.status_code == 422


def test_delete_category(test_app, monkeypatch):
    test_response_data = {"id": 1, "title": "Category"}
    r = RecipeCategory(**test_response_data)

    async def mock_delete(id, session):
        return r

    monkeypatch.setattr(crud_cats, "delete_cat", mock_delete)

    response = test_app.delete("/categories/1/")
    assert response.status_code == 200
    assert response.json() == test_response_data


def test_delete_category_invalid_id(test_app, monkeypatch):
    async def mock_get(id, session):
        return None

    monkeypatch.setattr(crud_cats, "get_", mock_get)

    async def mock_delete(id):
        return 1

    monkeypatch.setattr(crud_cats, "delete_cat", mock_delete)

    response = test_app.delete("/categories/100/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Category with specified ID does not exist"