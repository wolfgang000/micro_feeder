import { Link, Outlet, useNavigate } from "react-router-dom";
import "./style.css";
import { core } from "../../api";

function Page() {
  const navigate = useNavigate();

  const handleLogoutButtonClick = () => {
    core.logout().then(() => {
      navigate("/");
    });
  };

  return (
    <div>
      <nav className="navbar navbar-expand-md navbar-light bg-light fixed-top">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            MicroFeeder
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarCollapse"
            aria-controls="navbarCollapse"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarCollapse">
            <ul className="navbar-nav me-auto mb-2 mb-md-0"></ul>
            <div className="d-flex">
              <Link className="btn btn-light me-2" to="/docs/">
                Docs
              </Link>
              <div className="vr me-2"></div>
              <button
                onClick={handleLogoutButtonClick}
                data-testid="logoutButton"
                className="btn btn-secondary"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>
      <main>
        <Outlet />
      </main>
    </div>
  );
}

export default Page;
