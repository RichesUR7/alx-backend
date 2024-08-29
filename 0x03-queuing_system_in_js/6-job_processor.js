import kue from "kue";

const queue = kue.createQueue();

/**
 * Function to send a notification.
 * @param {string} phoneNumber - The phone number to send the notification to.
 * @param {string} message - The message to send.
 */
function sendNotification(phoneNumber, message) {
  console.log(
    `Sending notification to ${phoneNumber}, with message: ${message}`,
  );
}

queue.process("push_notification_code", (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message);
  done();
});
