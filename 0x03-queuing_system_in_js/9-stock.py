import asyncio
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

import redis
from flask import Flask, Response, jsonify, make_response

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
client = redis.Redis()

Product = Dict[str, Any]

# Data: List of products
list_products: List[Product] = [
    {
        "itemId": 1,
        "itemName": "Suitcase 250",
        "price": 50,
        "initialAvailableQuantity": 4,
    },
    {
        "itemId": 2,
        "itemName": "Suitcase 450",
        "price": 100,
        "initialAvailableQuantity": 10,
    },
    {
        "itemId": 3,
        "itemName": "Suitcase 650",
        "price": 350,
        "initialAvailableQuantity": 2,
    },
    {
        "itemId": 4,
        "itemName": "Suitcase 1050",
        "price": 550,
        "initialAvailableQuantity": 5,
    },
]


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    return make_response(jsonify({"status": "Internal Server Error"}), 500)


def get_item_by_id(item_id: int) -> Optional[Product]:
    """
    Retrieve a product by its ID.

    Args:
        item_id (int): The ID of the product.

    Returns:
        Optional[Product]: The product with the given ID, or None if not found.
    """
    return next(
        (item for item in list_products if item["itemId"] == item_id),
        None
    )


def async_redis(method: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to run a Redis method asynchronously.

    Args:
        method (Callable[..., Any]): The Redis method to run asynchronously.

    Returns:
        Callable[..., Any]: The wrapped asynchronous function.
    """

    @wraps(method)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, method, *args, **kwargs)

    return wrapper


@async_redis
def reserve_stock_by_id(item_id: int, stock: int) -> None:
    """
    Reserve stock for a product by its ID.

    Args:
        item_id (int): The ID of the product.
        stock (int): The stock to reserve.
    """
    try:
        with client.pipeline() as pipe:
            try:
                pipe.watch(f"item.{item_id}")
                pipe.multi()
                pipe.set(f"item.{item_id}", stock)
                pipe.execute()
            except redis.WatchError:
                raise Exception(
                    "Race condition encountered during reservation")
    except redis.ConnectionError:
        raise ConnectionError("Failed to connect to Redis")


@async_redis
def get_current_reserved_stock_by_id(item_id: int) -> int:
    """
    Get the current reserved stock for a product by its ID.

    Args:
        item_id (int): The ID of the product.

    Returns:
        int: The current reserved stock.
    """
    stock = client.get(f"item.{item_id}")
    try:
        return int(stock) if stock else 0
    except (ValueError, TypeError):
        return 0


def validate_item_id(item_id: int) -> bool:
    return item_id > 0


@app.route("/list_products", methods=["GET"])
def list_products_route() -> Response:
    """
    List all products.

    Returns:
        Response: JSON response containing the list of all products.
    """
    if not list_products:
        return make_response(jsonify({"status": "No products available"}), 404)

    return jsonify(list_products)


@app.route("/list_products/<int:item_id>", methods=["GET"])
async def get_product_route(item_id: int) -> Response:
    """
    Get product details including current stock.

    Args:
        item_id (int): The ID of the product.

    Returns:
        Response: JSON response containing the product details
        and current stock.
    """
    if not validate_item_id(item_id):
        return make_response(jsonify({"status": "Invalid product ID"}), 400)

    product_item = get_item_by_id(item_id)
    if not product_item:
        return make_response(jsonify({"status": "Product not found"}), 404)

    try:
        reserved_stock = await get_current_reserved_stock_by_id(item_id)
        current_quantity = product_item["initialAvailableQuantity"] - \
            reserved_stock
        return jsonify({**product_item, "currentQuantity": current_quantity})
    except Exception:
        return make_response(jsonify({"status": "Internal Server Error"}), 500)


@app.route("/reserve_product/<int:item_id>", methods=["GET"])
async def reserve_product_route(item_id: int) -> Response:
    """
    Reserve a product.

    Args:
        item_id (int): The ID of the product.

    Returns:
        Response: JSON response containing the reservation status.
    """
    if not validate_item_id(item_id):
        return make_response(jsonify({"status": "Invalid product ID"}), 400)

    product_item = get_item_by_id(item_id)
    if not product_item:
        return make_response(jsonify({"status": "Product not found"}), 404)

    try:
        reserved_stock = await get_current_reserved_stock_by_id(item_id)
        if reserved_stock >= product_item["initialAvailableQuantity"]:
            return jsonify(
                {"status": "Not enough stock available", "itemId": item_id}
            )

        await reserve_stock_by_id(item_id, reserved_stock + 1)
        return jsonify({"status": "Reservation confirmed", "itemId": item_id})
    except Exception:
        return make_response(jsonify({"status": "Internal Server Error"}), 500)


async def reset_products_stock() -> None:
    """
    Reset the stock for all products in Redis.
    """
    await asyncio.gather(
        *(reserve_stock_by_id(item["itemId"], 0) for item in list_products)
    )


if __name__ == "__main__":
    asyncio.run(reset_products_stock())
    app.run(host="0.0.0.0", port=1245)
