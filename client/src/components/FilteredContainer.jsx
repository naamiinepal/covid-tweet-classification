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
        <div className="text-white w-2/12 text-lg font-bold">View Data Of</div>
        <div className="mx-2 w-2/12 flex items-center ">
          <div className="text-white text-base font-semibold">Year: </div>
          <Select
            sx={{ backgroundColor: "white", minWidth: "5em", marginLeft: "1%" }}
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
        </div>
        <div className="mx-2 flex items-center w-2/12">
          <div className="text-white text-base font-semibold">Month: </div>

          <Select
            labelId="minority"
            id="minority-select"
            sx={{
              backgroundColor: "white",
              marginLeft: "1%",
              minWidth: "5em",
            }}
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
        </div>
        <Button
          variant="contained"
          //   color="success"
          size="large"
          sx={{ backgroundColor: "#247890" }}
          onClick={submitFilter}
        >
          Filter
        </Button>
      </div>
      <LineChart />
      <Tweets />
    </div>
  );
};

export default FilteredContainer;
