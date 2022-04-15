import { Button, MenuItem, Select } from "@mui/material";
import { useFilter } from "./FilterProvider";
import LineChart from "./LineChart";
import Tweets from "./Tweets";
import { months } from "../constants";
import { useState } from "react";
const FilteredContainer = () => {
  const { year, setYear, month, setMonth } = useFilter();
  const [yearTemp, setYearTemp] = useState(year);
  const [monthTemp, setMonthTemp] = useState(month);
  const submitFilter = () => {
    setYear(yearTemp);
    setMonth(monthTemp);
  };
  return (
    <div>
      <div className="flex mt-2 items-center ml-16 pl-2 w-11/12 py-1 bg-primary">
        <div className="text-white text-lg font-bold ">Filter Options</div>
        <Select
          sx={{ backgroundColor: "white", marginX: "2%" }}
          labelId="minority"
          id="minority-select"
          value={yearTemp}
          label="Year"
          onChange={(event) => {
            setYearTemp(`${event.target.value}`);
          }}
        >
          <MenuItem value="none">All</MenuItem>
          <MenuItem value={2021}>{2021}</MenuItem>
          <MenuItem value={2022}>{2022}</MenuItem>
        </Select>
        <Select
          labelId="minority"
          id="minority-select"
          sx={{ backgroundColor: "white" }}
          value={monthTemp}
          label="Month"
          onChange={(event) => {
            setMonthTemp(`${event.target.value}`);
          }}
        >
          <MenuItem value="none">All</MenuItem>
          {months.map((mon, idx) => (
            <MenuItem value={idx + 1}>{mon}</MenuItem>
          ))}
        </Select>
        <Button variant="outlined" color="secondary" onClick={submitFilter}>
          Filter
        </Button>
      </div>
      <LineChart />
      <Tweets />
    </div>
  );
};

export default FilteredContainer;
