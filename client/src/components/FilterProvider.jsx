import React, { useContext, useState } from "react";

let FilterContext = React.createContext();
const FilterProvider = ({ children }) => {
  const [year, setYear] = useState("none");
  const [month, setMonth] = useState("none");
  let value = { year, month, setYear, setMonth };
  return (
    <FilterContext.Provider value={value}>{children}</FilterContext.Provider>
  );
};

export default FilterProvider;
export function useFilter() {
  return useContext(FilterContext);
}
