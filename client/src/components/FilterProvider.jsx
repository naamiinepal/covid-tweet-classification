import moment from "moment";
import React, { useContext, useState } from "react";

let FilterContext = React.createContext();
const FilterProvider = ({ children }) => {
  const [startDate, setStartDate] = useState("2019-12-01");
  const [endDate, setEndDate] = useState(
    moment(new Date()).format("YYYY-MM-DD")
  );
  let value = { startDate, endDate, setStartDate, setEndDate };
  return (
    <FilterContext.Provider value={value}>{children}</FilterContext.Provider>
  );
};

export default FilterProvider;
export function useFilter() {
  return useContext(FilterContext);
}
