import { Navigate } from "react-router-dom";
import PropTypes from 'prop-types';
import { useUser } from "./Context/UserContext";

const PrivateRoute = ({ element }) => {
  const { user } = useUser();
  if (user.isLoggedIn) {
    return element; // Render the protected page if the user is logged in
  } else {
    return <Navigate to="/" />; // Redirect to 404 page if not logged in
  }
};

PrivateRoute.propTypes = {
  element: PropTypes.element.isRequired,
};

export default PrivateRoute;