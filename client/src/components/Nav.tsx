import SearchIcon from "@mui/icons-material/Search";
import Corona from "../svgs/corona";
import Name from "./Name";
import { InputBase } from "@mui/material";

const Nav = () => (
  <div className="border-2 bg-white px-16 py-2 flex items-center justify-start">
    <div className="font-bold w-16">
      <Corona />
    </div>
    <Name />
    <div className="ml-auto">
      <SearchIcon />
      <InputBase
        placeholder="Search…"
        inputProps={{ "aria-label": "search" }}
      />
    </div>
  </div>
);

export default Nav;
