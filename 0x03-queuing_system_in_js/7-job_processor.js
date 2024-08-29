import kue from "kue";

const blacklistedNumbers = ["4153518780", "4153518781"];

const queue = kue.createQueue();

/**
 * Function to send a notification.
 * @param {string} phoneNumber - The phone number to send the notification to.
 * @param {string} message - The message to send.
 * @param {Object} job - The job object from Kue.
 * @param {Function} done - The callback function to call when the job is complete or has failed.
 */
function sendNotification(phoneNumber, message, job, done) {
  job.progress(0, 100);

  if (blacklistedNumbers.includes(phoneNumber)) {
    const errorMessage = `Phone number ${phoneNumber} is blacklisted`;
    return done(new Error(errorMessage));
  }

  job.progress(50, 100);
  console.log(
    `Sending notification to ${phoneNumber}, with message: ${message}`,
  );

  done(); // Mark as completed
}

// Process the queue with concurrency of 2 jobs at a time
queue.process("push_notification_code_2", 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});
