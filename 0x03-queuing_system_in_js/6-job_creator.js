import kue from "kue";

const queue = kue.createQueue();

/**
 * Creates a job for push notifications.
 * @param {Object} jobData - The data for the job.
 * @param {string} jobData.phoneNumber - The phone number to send the notification to.
 * @param {string} jobData.message - The message to send.
 */
function createNotificationJob(jobData) {
  const job = queue.create("push_notification_code", jobData).save((err) => {
    if (err) {
      console.error("Notification job failed to create:", err);
    } else {
      console.log(`Notification job created: ${job.id}`);
    }
  });

  job.on("complete", () => {
    console.log("Notification job completed");
  });

  job.on("failed", () => {
    console.log("Notification job failed");
  });
}

const jobData = {
  phoneNumber: "+133309",
  message: "This is a test notification",
};

createNotificationJob(jobData);
