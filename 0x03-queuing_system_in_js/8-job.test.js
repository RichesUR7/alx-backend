import { expect } from "chai";
import sinon from "sinon";
import kue from "kue";
import createPushNotificationsJobs from "./8-job";

describe("createPushNotificationsJobs", () => {
  const queue = kue.createQueue();

  beforeEach(() => {
    sinon.stub(queue, "create").callsFake((type, data) => {
      return {
        save: sinon.stub().yields(null),
        on: sinon.stub(),
      };
    });
  });

  afterEach(() => {
    sinon.restore();
  });

  it("should throw an error if jobs is not an array", () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw(
      "Jobs is not an array",
    );
  });

  it("should create jobs when given an array of job data", () => {
    const jobs = [
      {
        phoneNumber: "4153518780",
        message: "This is the code 1234 to verify your account",
      },
      {
        phoneNumber: "4153518781",
        message: "This is the code 4562 to verify your account",
      },
    ];

    createPushNotificationsJobs(jobs, queue);

    expect(queue.create.calledTwice).to.be.true;
    expect(queue.create.firstCall.args[0]).to.equal("push_notification_code_3");
    expect(queue.create.firstCall.args[1]).to.deep.equal(jobs[0]);
    expect(queue.create.secondCall.args[0]).to.equal(
      "push_notification_code_3",
    );
    expect(queue.create.secondCall.args[1]).to.deep.equal(jobs[1]);
  });
});
