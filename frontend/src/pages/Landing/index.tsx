import "./style.css";
import env from "../../env";
import googleLogo from "../../assets/google.svg";
import rssLogo from "../../assets/logo-rss.svg";

function Landing() {
  return (
    <div>
      <nav className="navbar navbar-light static-top">
        <div className="container">
          <a className="navbar-brand fw-bold" href="#!">
            <img src={rssLogo} className="rss-logo-title" alt="logo" />
            MicroFeeder
          </a>
          <a
            className="btn btn-primary"
            href={`${env.backend_url}/web/auth/login`}
          >
            Log in
          </a>
        </div>
      </nav>

      <header className="masthead">
        <div className="container position-relative">
          <div className="row justify-content-center">
            <div className="col-xl-6">
              <div className="text-center">
                <h1 className="fw-bold">Feed to your servers the right data</h1>
                <h5 className="fw-normal">
                  Subscribe to RSS feeds and receive updates via webhooks.
                </h5>
                <div className="row pt-3">
                  <div className="col">
                    <a
                      className="btn btn-light btn-google"
                      role="button"
                      id="loginWithGoogleButton"
                      href={`${env.backend_url}/web/auth/login`}
                    >
                      <img
                        src={googleLogo}
                        className="google-logo-btn"
                        alt="logo"
                      />
                      Sign in with Google
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>
    </div>
  );
}

export default Landing;
