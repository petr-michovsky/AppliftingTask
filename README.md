# Applifting Python Task API Explorer

Explore the available API endpoints and their functionalities below.

---

## Getting Started

To get started, select an API endpoint. The available options are:

- `/get-products`
- `/create-product`
- `/delete-product`
- `/update-product`
- `/get-offers`

---

## Request Methods

Each endpoint uses a specific HTTP method:

- `/get-products`: **GET**
- `/create-product`: **POST**
- `/delete-product`: **DELETE**
- `/update-product`: **PUT**
- `/get-offers`: **POST**

---

## `/get-products` Endpoint

Returns a list of all products in the database, along with associated offers.

**Example Response:**

```json
[
    {
        "description": "test desc",
        "id": "10cb8f1f-dc8e-49dd-8a69-63aeec326866",
        "name": "test",
        "offers": [
            {
                "id": "0ab364d2-8c4d-35fb-9109-15451e9d9034",
                "items_in_stock": 179,
                "price": 65826,
                "product_id": "10cb8f1f-dc8e-49dd-8a69-63aeec326866"
            },
            {
                "id": "0fc090f8-a6bc-ab12-ef5c-35cb07a1dd72",
                "items_in_stock": 595,
                "price": 61902,
                "product_id": "10cb8f1f-dc8e-49dd-8a69-63aeec326866"
            }
            ...
        ]
    }
]
```

- Offers are updated every 5 seconds.
- Out-of-stock offers are deleted every 5 seconds.

---

## `/create-product` Endpoint

Creates a new product and registers it using the Applifting microservice.

**Request Body:**

```json
{
  "name": "Product name here",
  "description": "Product description here"
}
```

**Example Response:**

```json
{
  "description": "Product description here",
  "message": "Product created and registered successfully",
  "name": "Product name here",
  "product_id": "2f865ad9-c18d-48e9-811d-9fc0622a5006"
}
```

- The `product_id` is a unique identifier for the new product.

---

## `/delete-product` Endpoint

Deletes a product and all associated offers.

**Request Body:**

```json
{
  "product_id": "2f865ad9-c18d-48e9-811d-9fc0622a5006"
}
```

**Example Response:**

```json
{
  "message": "Product 2f865ad9-c18d-48e9-811d-9fc0622a5006 deleted successfully"
}
```

- Confirms successful deletion.

---

## `/update-product` Endpoint

Updates a product's `name` and/or `description`.

**Request Body:**

```json
{
  "product_id": "2f865ad9-c18d-48e9-811d-9fc0622a5006",
  "name": "Updated Product Name",
  "description": "Updated product description"
}
```

**Example Response:**

```json
{
  "message": "Product updated successfully",
  "product_id": "2f865ad9-c18d-48e9-811d-9fc0622a5006",
  "name": "Updated Product Name",
  "description": "Updated product description"
}
```

- Fields `name` and `description` are optional and can be updated individually.

---

## `/get-offers` Endpoint

Returns available offers for a given product. Only in-stock offers are returned.

**Request Body:**

```json
{
  "product_id": "10cb8f1fdc8e49dd8a6963aeec326866"
}
```

**Example Response:**

```json
{
  "offers": [
    {
      "id": "31db745e-ef62-805c-d8a4-a97f52d0ee19",
      "items_in_stock": 371,
      "price": 62172,
      "product_id": "10cb8f1f-dc8e-49dd-8a69-63aeec326866"
    },
    {
      "id": "0ab364d2-8c4d-35fb-9109-15451e9d9034",
      "items_in_stock": 162,
      "price": 65193,
      "product_id": "10cb8f1f-dc8e-49dd-8a69-63aeec326866"
    }
    ...
  ]
}
```

- Offers with `items_in_stock = 0` are excluded.

---
