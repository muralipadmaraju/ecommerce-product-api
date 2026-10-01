from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Application configuration from environment variables
APP_ENV = os.getenv("APP_ENV", "development")
DB_HOST = os.getenv("DB_HOST", "localhost")
APP_PORT = int(os.getenv("APP_PORT", "8080"))

# In-memory product data
products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 75000,
        "category": "Electronics"
    },
    {
        "id": 2,
        "name": "Mobile Phone",
        "price": 30000,
        "category": "Electronics"
    }
]


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "UP",
        "environment": APP_ENV
    }), 200


@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products), 200


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next(
        (product for product in products if product["id"] == product_id),
        None
    )

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200


@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = ["name", "price", "category"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    new_id = max([product["id"] for product in products], default=0) + 1

    product = {
        "id": new_id,
        "name": data["name"],
        "price": data["price"],
        "category": data["category"]
    }

    products.append(product)

    return jsonify(product), 201


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = next(
        (product for product in products if product["id"] == product_id),
        None
    )

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    product["name"] = data.get("name", product["name"])
    product["price"] = data.get("price", product["price"])
    product["category"] = data.get("category", product["category"])

    return jsonify(product), 200


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    global products

    product = next(
        (product for product in products if product["id"] == product_id),
        None
    )

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    products = [
        product for product in products
        if product["id"] != product_id
    ]

    return jsonify({
        "message": "Product deleted successfully"
    }), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=APP_PORT
    )