import { useState } from "react";
import "./style.css";
import { core } from "../../api";

function Page() {
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
      .then(() => {})
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
                htmlFor="exampleInputEmail1"
                className="form-label form-text"
              >
                Feed Url
              </label>
              <input
                type="text"
                className="form-control"
                id="exampleInputEmail1"
                aria-describedby="emailHelp"
                value={feedUrl}
                onChange={(e) => setFeedUrl(e.target.value)}
                required
              />
            </div>
            <div className="mb-3">
              <label
                htmlFor="exampleInputPassword1"
                className="form-label form-text"
              >
                Webhook Url
              </label>
              <input
                type="text"
                className="form-control"
                id="exampleInputPassword1"
                value={webhookUrl}
                onChange={(e) => setWebhookUrl(e.target.value)}
                required
              />
            </div>
            <div className="text-end">
              <button type="submit" className="btn btn-primary">
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
