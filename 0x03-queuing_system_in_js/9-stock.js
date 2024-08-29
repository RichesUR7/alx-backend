import express from "express";
import { createClient } from "redis";
import { promisify } from "util";

const app = express();
const client = createClient();
const PORT = 1245;

const getAsync = promisify(client.GET).bind(client);
const setAsync = promisify(client.SET).bind(client);

const listProducts = [
  {
    itemId: 1,
    itemName: "Suitcase 250",
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: "Suitcase 450",
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: "Suitcase 650",
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: "Suitcase 1050",
    price: 550,
    initialAvailableQuantity: 5,
  },
];

/**
 * Retrieves an item by its ID.
 * @param {number} id - The ID of the item.
 * @returns {Object|null} The item with the given ID, or null if not found.
 */
const getItemById = (id) => {
  return listProducts.find((item) => item.itemId === id);
};

/**
 * Sets the reserved stock for a given item in Redis.
 * @param {number} itemId - The ID of the item.
 * @param {number} stock - The stock to set.
 * @returns {Promise<void>}
 */
const reserveStockById = async (itemId, stock) => {
  await setAsync(`item.${itemId}`, stock);
};

/**
 * Retrieves the current reserved stock for a given item from Redis.
 * @param {number} itemId - The ID of the item.
 * @returns {Promise<number>} The current reserved stock.
 */
const getCurrentReservedStockById = async (itemId) => {
  const stock = await getAsync(`item.${itemId}`);
  return Number(stock) || 0;
};

// List all products
app.get("/list_products", (_, res) => {
  res.json(listProducts);
});

// Get product details including current stock
app.get("/list_products/:itemId(\\d+)", async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const productItem = getItemById(itemId);

  if (!productItem) {
    res.status(404).json({ status: "Product not found" });
    return;
  }

  try {
    const reservedStock = await getCurrentReservedStockById(itemId);
    const currentQuantity =
      productItem.initialAvailableQuantity - reservedStock;
    res.json({ ...productItem, currentQuantity });
  } catch (error) {
    res.status(500).json({ status: "Internal Server Error" });
  }
});

// Reserve a product
app.get("/reserve_product/:itemId(\\d+)", async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const productItem = getItemById(itemId);

  if (!productItem) {
    res.status(404).json({ status: "Product not found" });
    return;
  }

  try {
    const reservedStock = await getCurrentReservedStockById(itemId);

    if (reservedStock >= productItem.initialAvailableQuantity) {
      res.json({ status: "Not enough stock available", itemId });
      return;
    }

    await reserveStockById(itemId, reservedStock + 1);
    res.json({ status: "Reservation confirmed", itemId });
  } catch (error) {
    res.status(500).json({ status: "Internal Server Error" });
  }
});

// Reset product stock in Redis
const resetProductsStock = async () => {
  await Promise.all(
    listProducts.map((item) => setAsync(`item.${item.itemId}`, 0)),
  );
};

app.listen(PORT, async () => {
  await resetProductsStock();
  console.log(`API available on localhost port ${PORT}`);
});

export default app;
