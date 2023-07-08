import { useState } from "react";
import "./style.css";
import { core } from "../../api";
import { useNavigate } from "react-router-dom";

function Page() {
  const navigate = useNavigate();
  const [feedUrl, setFeedUrl] = useState("");
  const [webhookUrl, setWebhookUrl] = useState("");

  const handleSubmit = (event: { preventDefault: () => void }) => {
    event.preventDefault();

    const payload = {
      feed_url: feedUrl,
      webhook_url: webhookUrl,
    };

    core
      .createSubscription(payload)
      .then(() => {
        navigate("/subscriptions");
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div className="container">
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
                className="form-control"
                id="createSubscriptionFeedUrlField"
                aria-describedby="emailHelp"
                value={feedUrl}
                onChange={(e) => setFeedUrl(e.target.value)}
                required
              />
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
                className="form-control"
                id="createSubscriptionWebhookUrlField"
                value={webhookUrl}
                onChange={(e) => setWebhookUrl(e.target.value)}
                required
              />
            </div>
            <div className="text-end">
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
