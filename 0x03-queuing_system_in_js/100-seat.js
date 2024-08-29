import express from "express";
import { createClient } from "redis";
import { promisify } from "util";
import kue from "kue";

const app = express();
const client = createClient();
const queue = kue.createQueue();
const PORT = 1245;

const getAsync = promisify(client.GET).bind(client);
const setAsync = promisify(client.SET).bind(client);

let reservationEnabled = true;

/**
 * Sets the number of available seats in Redis.
 * @param {number} number - The number of available seats.
 * @returns {Promise<void>}
 */
const reserveSeat = async (number) => {
  await setAsync("available_seats", number);
};

/**
 * Retrieves the current number of available seats from Redis.
 * @returns {Promise<number>} The current number of available seats.
 */
const getCurrentAvailableSeats = async () => {
  const seats = await getAsync("available_seats");
  return Number(seats) || 0;
};

reserveSeat(50);

// Get the number of available seats.
app.get("/available_seats", async (_, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

// Reserve a seat.
app.get("/reserve_seat", (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: "Reservation are blocked" });
    return;
  }

  const job = queue.create("reserve_seat").save((err) => {
    if (err) {
      res.json({ status: "Reservation failed" });
      return;
    }
    res.json({ status: "Reservation in process" });
  });

  job.on("complete", () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on("failed", (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err}`);
  });
});

// Process the queue.
app.get("/process", async (_, res) => {
  res.json({ status: "Queue processing" });

  queue.process("reserve_seat", async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();

    if (availableSeats <= 0) {
      reservationEnabled = false;
      done(new Error("Not enough seats available"));
      return;
    }

    await reserveSeat(availableSeats - 1);
    if (availableSeats - 1 === 0) {
      reservationEnabled = false;
    }
    done();
  });
});

app.listen(PORT, () => {
  console.log(`API available on localhost port ${PORT}`);
});

export default app;
