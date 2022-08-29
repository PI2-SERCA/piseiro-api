import pytest
from src.app import create_app
from src.model.cut import Cut
from src.model.room import Room


@pytest.fixture()
def app():
    app, _, _ = create_app(is_testing=True)
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here

    Cut.drop_collection()
    Room.drop_collection()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
