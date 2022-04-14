import FilteredContainer from "./FilteredContainer";
import LineChart from "./LineChart";
import Nav from "./Nav";
import Purpose from "./Purpose";
// import Team from "./Team";
import Tweets from "./Tweets";

const EndUser = () => {
  return (
    <div>
      <Nav />
      <div className=" bg-blue-50">
        <Purpose />
        {/* <Worker /> */}
        <FilteredContainer />
        {/* <Team /> */}
      </div>
    </div>
  );
};

export default EndUser;
