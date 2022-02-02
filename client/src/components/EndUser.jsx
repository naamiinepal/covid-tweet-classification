import TweetCollection from "./CSVReader";
import LineChart from "./LineChart";
import Nav from "./Nav";
import Purpose from "./Purpose";

const EndUser = () => {
  return (
    <div className="bg-blue-50 pb-16">
      <Nav />
      <div className="mt-3">
        <Purpose />
        <LineChart />
        <TweetCollection />
      </div>

      {/* <DataGridDemo /> */}
    </div>
  );
};

export default EndUser;
