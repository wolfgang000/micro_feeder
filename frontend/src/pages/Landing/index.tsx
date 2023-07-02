import "./style.css";
import env from "../../env";

function Landing() {
  return (
    <a
      className="btn-google"
      id="loginWithGoogleButton"
      href={`${env.backend_url}/web/auth/login`}
    >
      Sign in with Google
    </a>
  );
}

export default Landing;
