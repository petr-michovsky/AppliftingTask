# ----------------------------------------------------- #
# ------ This file contains tests for api routes ------ #
# ----------------------------------------------------- #


def test_create_product(app, session):
    # Test data to send in the POST request
    product_data = {
        'name': 'Test Product',
        'description': 'A product for testing'
    }

    with app.test_client() as client:
        response = client.post('create-product', json=product_data)

    assert response.status_code == 201
    json_data = response.get_json()
    assert 'product_id' in json_data
    assert json_data['message'] == 'Product created and registered successfully'


def test_create_product_missing_data(app):
    # Missing 'name' and 'description'
    product_data = {}

    with app.test_client() as client:
        response = client.post('create-product', json=product_data)

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['error'] == 'Missing name or description'


def test_get_products(app, sample_product):
    with app.test_client() as client:
        response = client.get('get-products')

    assert response.status_code == 200
    products = response.get_json()
    assert len(products) == 1
    assert products[0]['name'] == sample_product.name
    assert products[0]['description'] == sample_product.description


def test_delete_product(app, sample_product):
    product_id = str(sample_product.id)
    data = {'product_id': product_id}

    with app.test_client() as client:
        response = client.delete('delete-product', json=data)

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == f'Product {product_id} deleted successfully'


def test_delete_product_missing_id(app):
    # Missing product_id
    data = {}

    with app.test_client() as client:
        response = client.delete('delete-product', json=data)

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['error'] == 'Missing product_id'


def test_delete_product_invalid_id(app):
    # Invalid product_id format
    data = {'product_id': 'invalid-uuid'}

    with app.test_client() as client:
        response = client.delete('delete-product', json=data)

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['error'] == 'Invalid product_id format'


def test_update_product(app, sample_product):
    updated_data = {
        'product_id': str(sample_product.id),
        'name': 'Updated Product',
        'description': 'Updated description'
    }

    with app.test_client() as client:
        response = client.put('update-product', json=updated_data)

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == 'Product updated successfully'
    assert json_data['name'] == 'Updated Product'
    assert json_data['description'] == 'Updated description'


def test_update_product_missing_id(app):
    # Missing product_id
    updated_data = {'name': 'Updated Product'}

    with app.test_client() as client:
        response = client.put('update-product', json=updated_data)

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['error'] == 'Missing product_id'


def test_get_offers(app, sample_product):
    offer_data = {
        'product_id': str(sample_product.id)
    }

    with app.test_client() as client:
        response = client.post('get-offers', json=offer_data)

    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data['offers'], list)