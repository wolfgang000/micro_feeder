import { useEffect, useState } from "react";
import "./style.css";
import { core } from "../../api";

function Page() {
  const [subscriptions, setSubscriptions] = useState([] as any[]);

  useEffect(() => {
    core.getSubscriptionas().then((subscriptions) => {
      setSubscriptions(subscriptions);
    });
  }, []);

  return (
    <div className="container">
      <table className="table">
        <thead>
          <tr>
            <th scope="col">Feed Url</th>
            <th scope="col">Webhook Url</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          {subscriptions.map((subscription, index) => (
            <tr key={index}>
              <td>{subscription.feed_url}</td>
              <td>{subscription.webhook_url}</td>
              <td>
                <button
                  type="button"
                  className="btn btn-danger"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Page;
