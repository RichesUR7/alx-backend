import { createClient } from "redis";
import { promisify } from "util";

const redis = require("redis");
const client = createClient();

client.on("connect", () => console.log("Redis client connected to the server"));

client.on("error", (err) => {
  console.error("Redis client not connected to the server: ", err);
  client.quit();
});

/**
 * Function to set a new key-value pair in Redis and print a confirmation message
 * @function setNewSchool
 * @param {string} schoolName - The key to set in Redis
 * @param {string} value - The value to set in Redis
 */
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

/**
 * Function to get the value of a key in Redis and print it
 * @function displaySchoolValue
 * @param {string} schoolName - The key to get from Redis
 */
async function displaySchoolValue(schoolName) {
  const getAsync = promisify(client.get).bind(client);
  try {
    const reply = await getAsync(schoolName);
    console.log(reply);
  } catch (err) {
    console.error(err);
  }
}

displaySchoolValue("Holberton");
setNewSchool("HolbertonSanFrancisco", "100");
displaySchoolValue("HolbertonSanFrancisco");
