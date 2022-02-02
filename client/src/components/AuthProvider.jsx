import axios from "axios";
import { useContext, useState } from "react";
import { createContext } from "react";
import { loggedInOrNot } from "./utility";

let AuthContext = createContext(null);

export default function AuthProvider({ children }) {
  let [user, setUser] = useState(loggedInOrNot());
  let signin = async (username, password, callback) => {
    const config = {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    };
    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);

    return axios
      .post("/auth/login", params, config)
      .then((data) => data.data)
      .then((data) => {
        sessionStorage.setItem("accessToken", data.access_token);
        setUser(loggedInOrNot());
        callback();
      });
  };

  let signout = (callback) => {
    return "Signed Out";
  };

  let value = { user, signin, signout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
