import FilteredContainer from "./FilteredContainer";
import Nav from "./Nav";
import Purpose from "./Purpose";
// import Team from "./Team";

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
