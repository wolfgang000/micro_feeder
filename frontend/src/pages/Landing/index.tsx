import "./style.css";
import env from "../../env";
import googleLogo from "../../assets/google.svg";

function Landing() {
  return (
    <div>
      <nav className="navbar navbar-light bg-light static-top">
        <div className="container">
          <a className="navbar-brand" href="#!">
            Micro feeder
          </a>
          <a
            className="btn btn-primary"
            href={`${env.backend_url}/web/auth/login`}
          >
            Log in
          </a>
        </div>
      </nav>

      <a
        className="btn btn-light btn-google"
        role="button"
        id="loginWithGoogleButton"
        href={`${env.backend_url}/web/auth/login`}
      >
        <img src={googleLogo} className="google-logo-btn" alt="logo" />
        Sign in with Google
      </a>
    </div>
  );
}

export default Landing;
