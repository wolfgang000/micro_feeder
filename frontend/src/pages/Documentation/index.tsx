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
    <div>
      <div className="container">
        <h3>Webhook events</h3>
        Requests are sent as POSTs with{" "}
        <code>Content-Type: application/json</code>:
        <pre className="code-block">
          <code>{textedJson}</code>
        </pre>
      </div>
    </div>
  );
}

export default Page;
