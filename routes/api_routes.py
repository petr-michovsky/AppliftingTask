# ---------------------------------------------------------------- #
# ----- These routes handle the API inside the application  ------ #
# ---------------------------------------------------------------- #
from flask import Blueprint, request, jsonify
from models import db, Product
import uuid
from uuid import UUID
from utility_funcs import register_product

api_routes = Blueprint('api_routes', __name__)


@api_routes.route('/create-product', methods=["POST"])
def create_product():
    data = request.get_json()

    if not data or 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Missing name or description'}), 400

    product = Product(
        id=uuid.uuid4(),
        name=data['name'],
        description=data['description'],
    )

    # Register the product in the API
    try:
        response = register_product(product)

        if response.status_code == 201:
            # Only add the product to the database after successful registration
            db.session.add(product)
            db.session.commit()

            return jsonify({
                'message': 'Product created and registered successfully',
                'product_id': str(product.id),
                'name': product.name,
                'description': product.description
            }), 201

        else:
            return jsonify({'error': 'Failed to register product with external service'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_routes.route('/get-products', methods=["GET"])
def get_products():
    all_products = Product.query.all()
    products_list = [product.to_dict() for product in all_products]
    return jsonify(products_list)


@api_routes.route('/delete-product', methods=["DELETE"])
def delete_product():
    data = request.get_json()
    print(f"Received data: {data}")

    if not data or 'product_id' not in data:
        return jsonify({'error': 'Missing product_id'}), 400

    try:
        product_id = UUID(data['product_id'])
    except ValueError:
        return jsonify({'error': 'Invalid product_id format'}), 400

    product = Product.query.get(product_id)

    if not product:
        return jsonify({'error': 'Product not found'}), 404


    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': f'Product {product_id} deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_routes.route('/update-product', methods=["PUT"])
def update_product():
    data = request.get_json()

    if not data or 'product_id' not in data:
        return jsonify({'error': 'Missing product_id'}), 400

    try:
        product_id = UUID(data['product_id'])
    except ValueError:
        return jsonify({'error': 'Invalid product_id format'}), 400

    product = Product.query.get(product_id)

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    if 'name' in data:
        product.name = data['name']

    if 'description' in data:
        product.description = data['description']

    try:
        db.session.commit()

        return jsonify({
            'message': 'Product updated successfully',
            'product_id': str(product.id),
            'name': product.name,
            'description': product.description
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_routes.route('/get-offers', methods=["POST"])
def get_offers():
    data = request.get_json()

    if not data or 'product_id' not in data:
        return jsonify({'error': 'Missing product_id'}), 400

    try:
        product_id = UUID(data['product_id'])
    except ValueError:
        return jsonify({'error': 'Invalid product_id format'}), 400

    product = Product.query.get(product_id)

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    offers_list = [
        offer.to_dict() for offer in product.offers
        if offer.items_in_stock > 0  # Do not show out-of-stock offers
    ]

    return jsonify({'offers': offers_list}), 200
