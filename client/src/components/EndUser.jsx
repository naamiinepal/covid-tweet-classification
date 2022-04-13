import LineChart from "./LineChart";
import Nav from "./Nav";
import Purpose from "./Purpose";
import Tweets from "./Tweets";

const EndUser = () => {
  return (
    <div>
      <Nav />
      <div className=" bg-blue-50">
        <Purpose />
        {/* <Worker /> */}
        <LineChart />
        <Tweets />
      </div>
    </div>
  );
};

export default EndUser;
