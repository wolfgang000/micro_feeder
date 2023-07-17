import { useEffect, useState } from "react";
import "./style.css";
import { core } from "../../api";
import { Link } from "react-router-dom";

function Page() {
  const [subscriptions, setSubscriptions] = useState([] as Subscription[]);
  const [isFeachPromiseSettled, setIsFeachPromiseSettled] = useState(false);
  const [selectedSubscription, setSelectedSubscription] = useState({
    feed_url: "",
    webhook_url: "",
    id: 0,
  } as Subscription);

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

  const handleConfirmDeleteModalButtonClick = (subscription: any) => {
    setSelectedSubscription(subscription);
  };

  const handleDeleteButtonClick = (subscriptionId: number) => {
    setIsFeachPromiseSettled(false);
    core
      .deleteSubscription(subscriptionId)
      .then(() => {
        return core.getSubscriptions();
      })
      .then((subscriptions) => {
        setSubscriptions(subscriptions);
      })
      .finally(() => {
        setIsFeachPromiseSettled(true);
      });
  };

  const SubscriptionsTable = () => {
    return (
      <div>
        <div className="card">
          <div className="card-body">
            <h4>Subscriptions:</h4>
            <table data-testid="subscriptionsTable" className="table">
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
                        className="btn btn-danger btn-sm"
                        data-bs-toggle="modal"
                        data-bs-target="#confirmDeleteModal"
                        onClick={() =>
                          handleConfirmDeleteModalButtonClick(subscription)
                        }
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div
          className="modal fade"
          id="confirmDeleteModal"
          aria-labelledby="confirmDeleteModalLabel"
          aria-hidden="true"
        >
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title" id="confirmDeleteModalLabel">
                  Delete Subscription
                </h5>
                <button
                  type="button"
                  className="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div className="modal-body">
                <div className="pb-3">
                  Are you sure you want to delete this subscription?
                </div>
                <div>
                  <strong>{selectedSubscription.feed_url}</strong> →{" "}
                  <strong>{selectedSubscription.webhook_url}</strong>
                </div>
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  className="btn btn-danger"
                  data-bs-dismiss="modal"
                  onClick={() =>
                    handleDeleteButtonClick(selectedSubscription.id)
                  }
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
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
      <div className="placeholder-glow">
        <div className="text-end pb-3">
          <span className="placeholder col-2"></span>
        </div>
        <div className="text-start pb-3">
          <span className="placeholder col-2"></span>
        </div>
        <table className="table">
          <thead>
            <tr>
              <th scope="col">
                <span className="placeholder col-2"></span>
              </th>
              <th scope="col">
                <span className="placeholder col-2"></span>
              </th>
            </tr>
          </thead>

          <tbody>
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
      </div>
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
