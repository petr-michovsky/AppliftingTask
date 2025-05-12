# ----------------------------------------------------- #
# --------- This file handles background tasks -------- #
# ----------------------------------------------------- #
from uuid import UUID
from models import Product, Offer, db
from utility_funcs import get_offers_for_product
import json

def update_product_offers(app):
    with app.app_context():
        all_ids = Product.get_all_ids()

        if not all_ids:
            print("No products found in the database")
            return

        all_offers = {}

        for product_id in all_ids:
            response = get_offers_for_product(product_id) # Querying all offers for a given product
            all_offers[product_id] = response.text

        for product_id, offers in all_offers.items():
            # print(f"Offers for product {product_id}:")

            try:
                offers_data = json.loads(offers)

                for offer_data in offers_data:
                    offer_id = UUID(offer_data['id'])
                    price = offer_data['price']
                    items_in_stock = offer_data['items_in_stock']

                    # print(f"Offer ID: {offer_id}, Price: {price}, Items in stock: {items_in_stock}")

                    existing_offer = db.session.query(Offer).filter_by(id=offer_id, product_id=product_id).first()

                    if existing_offer:
                        existing_offer.price = price
                        existing_offer.items_in_stock = items_in_stock

                    else:
                        offer = Offer(
                            id=offer_id,
                            price=price,
                            items_in_stock=items_in_stock,
                            product_id=product_id
                        )

                        db.session.add(offer)

                db.session.commit()

            except json.JSONDecodeError:
                print(f"Error decoding JSON for product {product_id}: {offers}")



# Function to periodically delete out-of-stock offers
def delete_out_of_stock_offers(app):
    with app.app_context():
        out_of_stock_offers = db.session.query(Offer).filter(Offer.items_in_stock <= 0).all()

        if not out_of_stock_offers:
            print("No out-of-stock offers to delete.")
            return

        for offer in out_of_stock_offers:
            print(f"Deleting offer {offer.id} (Product {offer.product_id}) with 0 items in stock.")
            db.session.delete(offer)

        db.session.commit()
        print(f"Deleted {len(out_of_stock_offers)} out-of-stock offers.")
