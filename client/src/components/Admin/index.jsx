import { Outlet, Route, Routes } from "react-router";
import Nav from "../Nav";
import TweetCollectionAdminPanel from "./TweetCollectionAdminPanel";

const Admin = () => {
  return (
    <div>
      <Nav />
      {/* <TweetCollectionAdminPanel action="verify" /> */}
      <Outlet />
    </div>
  );
};

export default Admin;
