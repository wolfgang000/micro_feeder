import "./style.css";

function Page() {
  const data = {
    subscription_id: 1234,
    new_entries: [
      {
        id: "https://abcnews.go.com/US/wireStory/microsoft-moves-closer-completing-69-billion-activision-takeover-101302097",
        link: "https://abcnews.go.com/US/wireStory/microsoft-moves-closer-completing-69-billion-activision-takeover-101302097",
        summary:
          "A U.S. appeals court has rejected a bid by federal regulators to block Microsoft from closing its $68.7 billion deal to buy video game maker Activision Blizzard",
        title:
          "Microsoft moves closer to completing $69 billion Activision takeover after court rebuffs regulators",
        published_at: "Tue, 11 Jul 2023 21:42:24 -0400",
      },
    ],
  };
  var textedJson = JSON.stringify(data, undefined, 4);

  return (
    <div className="container">
      <div className="card">
        <div className="card-body">
          <div className="container">
            <h3>RSS Feed</h3>
            The feed url should point to a valid RSS feed, this feed is going to
            be checked every 5 minutes to look for new entries, if new entries
            are found then a webhook event with the new events is going to be
            triggered.
            <h3 className="pt-2">Webhook events</h3>
            Requests are sent as POSTs with{" "}
            <code>Content-Type: application/json</code>:
            <pre className="code-block">
              <code>{textedJson}</code>
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Page;
