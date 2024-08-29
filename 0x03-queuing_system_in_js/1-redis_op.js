import { createClient } from "redis";

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
function displaySchoolValue(schoolName) {
  client.get(schoolName, (err, reply) => {
    if (err) throw err;
    console.log(reply);
  });
}

displaySchoolValue("Holberton");
setNewSchool("HolbertonSanFrancisco", "100");
displaySchoolValue("HolbertonSanFrancisco");
