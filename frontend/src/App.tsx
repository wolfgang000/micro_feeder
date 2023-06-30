import React from "react";
import logo from "./logo.svg";
import "./App.css";
import env from "./env";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="btn-google"
          id="loginWithGoogleButton"
          href={`${env.backend_url}/web/auth/login`}
        >
          Sign in with Google
        </a>
      </header>
    </div>
  );
}

export default App;
