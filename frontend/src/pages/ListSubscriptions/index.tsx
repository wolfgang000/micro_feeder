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
      <ul>
        {subscriptions.map((subscription, index) => (
          <li key={index}>
            {subscription.webhook_url} - {subscription.feed_url}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Page;
