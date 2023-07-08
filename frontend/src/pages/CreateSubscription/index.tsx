import { useState } from "react";
import "./style.css";
import { core } from "../../api";
import { Link, useNavigate } from "react-router-dom";

function Page() {
  const navigate = useNavigate();
  const [feedUrl, setFeedUrl] = useState("");
  const [webhookUrl, setWebhookUrl] = useState("");
  const [feedUrlErrors, setFeedUrlErrors] = useState([] as string[]);
  const [webhookUrlErrors, setWebhookUrlErrors] = useState([] as string[]);

  const handleSubmit = (event: { preventDefault: () => void }) => {
    event.preventDefault();

    setFeedUrlErrors((old) => {
      old.length = 0;
      return old;
    });

    setWebhookUrlErrors((old) => {
      old.length = 0;
      return old;
    });

    const payload = {
      feed_url: feedUrl,
      webhook_url: webhookUrl,
    };

    const handleFailedRequest = (failedRequest: {
      response: { data: any };
    }) => {
      const response = failedRequest.response.data;
      if (response.detail.feed_url) {
        setFeedUrlErrors((old) => [...old, ...response.detail.feed_url]);
      }
      if (response.detail.webhook_url) {
        setWebhookUrlErrors((old) => [...old, ...response.detail.webhook_url]);
      }
    };

    core
      .createSubscription(payload)
      .then(() => {
        navigate("/subscriptions");
      })
      .catch(handleFailedRequest);
  };

  return (
    <div className="container pt-4 create-subscription-container">
      <div className="card">
        <h5 className="card-header">Create a New Subscription</h5>
        <div className="card-body">
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label
                htmlFor="createSubscriptionFeedUrlField"
                className="form-label form-text"
              >
                Feed Url
              </label>
              <input
                type="text"
                className={`form-control ${
                  feedUrlErrors.length !== 0 ? "is-invalid" : ""
                }`}
                id="createSubscriptionFeedUrlField"
                aria-describedby="emailHelp"
                value={feedUrl}
                onChange={(e) => setFeedUrl(e.target.value)}
                required
              />
              {feedUrlErrors.map((error, index) => (
                <div
                  data-testid="feedUrlFieldError"
                  className="invalid-feedback"
                  key={index}
                >
                  {error}
                </div>
              ))}
            </div>
            <div className="mb-3">
              <label
                htmlFor="createSubscriptionWebhookUrlField"
                className="form-label form-text"
              >
                Webhook Url
              </label>
              <input
                type="text"
                className={`form-control ${
                  webhookUrlErrors.length !== 0 ? "is-invalid" : ""
                }`}
                id="createSubscriptionWebhookUrlField"
                value={webhookUrl}
                onChange={(e) => setWebhookUrl(e.target.value)}
                required
              />
              {webhookUrlErrors.map((error, index) => (
                <div
                  data-testid="webhookUrlFieldError"
                  className="invalid-feedback"
                  key={index}
                >
                  {error}
                </div>
              ))}
            </div>
            <div className="text-end">
              <Link
                id="createSubscriptionCancelButton"
                type="button"
                className="btn btn-secondary me-2"
                to=".."
                relative="path"
              >
                Cancel
              </Link>
              <button
                id="createSubscriptionSubmitButton"
                type="submit"
                className="btn btn-primary"
              >
                Create
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Page;
