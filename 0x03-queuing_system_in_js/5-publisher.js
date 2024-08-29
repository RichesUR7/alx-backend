import redis from "redis";

const client = redis.createClient();

client.on("connect", () => {
  console.log("Redis client connected to the server");
});

client.on("error", (err) => {
  console.error("Redis client not connected to the server:", err);
});

/**
 * Publishes a message to the specified channel after a delay.
 * @param {string} message - The message to publish.
 * @param {number} time - The delay in milliseconds before publishing the message.
 */
function publishMessage(message, time) {
  setTimeout(() => {
    console.log(`About to send ${message}`);
    client.publish("holberton school channel", message);
  }, time);
}

publishMessage("Holberton Student #1 starts course", 100);
publishMessage("Holberton Student #2 starts course", 200);
publishMessage("KILL_SERVER", 300);
publishMessage("Holberton Student #3 starts course", 400);
