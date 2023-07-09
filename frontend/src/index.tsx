import React from "react";
import ReactDOM from "react-dom/client";
import AuthRoot from "./pages/AuthRoot";
import Landing from "./pages/Landing";
import CreateSubscription from "./pages/CreateSubscription";
import ListSubscriptions from "./pages/ListSubscriptions";
import Documentation from "./pages/Documentation";
import reportWebVitals from "./reportWebVitals";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import "./index.css";

const router = createBrowserRouter([
  {
    path: "/subscriptions",
    element: <AuthRoot />,
    children: [
      {
        path: "add",
        element: <CreateSubscription />,
      },
      {
        path: "",
        element: <ListSubscriptions />,
      },
    ],
  },
  {
    path: "/docs/",
    element: <Documentation />,
  },
  {
    path: "/",
    element: <Landing />,
  },
]);

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
