import redis from "redis";

const client = redis.createClient();

client.on("error", (err) => {
  console.error("Redis client error:", err);
});

/**
 * Sets the values for various cities in the HolbertonSchools hash.
 * @param {string} key - The key of the hash.
 * @param {string} field - The field name.
 * @param {number} value - The value to set.
 */
function setHashValue(key, field, value) {
  client.hset(key, field, value, redis.print);
}

/**
 * Retrieves and displays all values in the hash.
 * @param {string} key - The key of the hash.
 */
function displayHashValues(key) {
  client.hgetall(key, (err, reply) => {
    if (err) {
      console.error("Error retrieving hash values:", err);
    } else {
      console.log(reply);
    }
    client.quit();
  });
}

setHashValue("HolbertonSchools", "Portland", 50);
setHashValue("HolbertonSchools", "Seattle", 80);
setHashValue("HolbertonSchools", "New York", 20);
setHashValue("HolbertonSchools", "Bogota", 20);
setHashValue("HolbertonSchools", "Cali", 40);
setHashValue("HolbertonSchools", "Paris", 2);

displayHashValues("HolbertonSchools");
