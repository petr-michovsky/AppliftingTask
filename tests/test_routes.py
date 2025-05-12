# ----------------------------------------------------- #
# -------- This file contains tests for routes -------- #
# ----------------------------------------------------- #


def test_index_route(app):
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b"API Explorer" in response.data


def test_docs_route(app):
    with app.test_client() as client:
        response = client.get('/docs')
        assert response.status_code == 200
        assert b"Documentation" in response.data