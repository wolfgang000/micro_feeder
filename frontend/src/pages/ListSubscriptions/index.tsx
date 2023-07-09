import { useEffect, useState } from "react";
import "./style.css";
import { core } from "../../api";
import { Link } from "react-router-dom";

function Page() {
  const [subscriptions, setSubscriptions] = useState([] as any[]);
  const [isFeachPromiseSettled, setIsFeachPromiseSettled] = useState(false);

  useEffect(() => {
    core
      .getSubscriptions()
      .then((subscriptions) => {
        setSubscriptions(subscriptions);
      })
      .finally(() => {
        setIsFeachPromiseSettled(true);
      });
  }, []);

  const SubscriptionsTable = () => {
    return (
      <div className="card">
        <div className="card-body">
          <h4>Subscriptions:</h4>
          <table className="table">
            <thead>
              <tr>
                <th scope="col">Feed Url</th>
                <th scope="col">Webhook Url</th>
              </tr>
            </thead>
            <tbody>
              {subscriptions.map((subscription, index) => (
                <tr key={index}>
                  <td>{subscription.feed_url}</td>
                  <td>{subscription.webhook_url}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  const noSubscriptionsFoundMessage = () => {
    return (
      <div className="card">
        <div className="card-body text-center">
          <h4 className="card-text">
            You don't have any subscriptions yet,{" "}
            <Link data-testid="makeSubscriptionLink" to="/subscriptions/add">
              make one
            </Link>
            .
          </h4>
          <p className="card-text">
            Need more info? check out the <Link to="/docs/">Docs</Link>.
          </p>
        </div>
      </div>
    );
  };

  const showSubscriptionsTableOrNotFoundMessage = () => {
    const component =
      subscriptions.length === 0
        ? noSubscriptionsFoundMessage()
        : SubscriptionsTable();

    return (
      <div>
        <div className="text-end pb-3">
          <Link
            data-testid="addSubscriptionLink"
            className="btn btn-primary"
            role="button"
            to="/subscriptions/add"
          >
            Add subscription
          </Link>
        </div>
        <div>{component}</div>
      </div>
    );
  };

  const subscriptionsTablePlaceholder = () => {
    return (
      <table className="table">
        <thead className="placeholder-glow">
          <tr>
            <th scope="col">
              <span className="placeholder col-2"></span>
            </th>
            <th scope="col">
              <span className="placeholder col-2"></span>
            </th>
          </tr>
        </thead>

        <tbody className="placeholder-glow">
          {Array.from(Array(8).keys()).map((_, index) => {
            return (
              <tr key={index}>
                <td>
                  <span className="placeholder col-10"></span>
                </td>
                <td>
                  <span className="placeholder col-10"></span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    );
  };

  return (
    <div className="container pt-4">
      {isFeachPromiseSettled
        ? showSubscriptionsTableOrNotFoundMessage()
        : subscriptionsTablePlaceholder()}
    </div>
  );
}

export default Page;
