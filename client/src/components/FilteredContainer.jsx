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
    <>
      <Select
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
      <Button onClick={submitFilter}>Filter</Button>
      <LineChart />
      <Tweets />
    </>
  );
};

export default FilteredContainer;
