import { Button } from "@mui/material";
import { useFilter } from "./FilterProvider";
import LineChart from "./LineChart";
import Tweets from "./Tweets";
import { useEffect, useState } from "react";
import { DatePicker } from "@material-ui/pickers";
import moment from "moment";
const FilteredContainer = () => {
  const { startDate, setStartDate, endDate, setEndDate } = useFilter();
  const [selectedStartDate, handleStartDateChange] = useState(
    new Date(startDate)
  );
  const [selectedEndDate, handleEndDateChange] = useState(new Date(endDate));

  useEffect(() => {
    console.log(moment(selectedStartDate).format("YYYY-MM-DD"));
  }, [selectedStartDate]);
  const submitFilter = () => {
    setStartDate(moment(selectedStartDate).format("YYYY-MM-DD"));
    setEndDate(moment(selectedEndDate).format("YYYY-MM-DD"));
  };
  return (
    <div>
      <div className="flex mt-2 items-center ml-16 pl-2 w-11/12 py-1 bg-primary">
        <div className="text-white w-2/12 text-lg font-bold">View Data Of</div>
        <div className="mx-2 w-2/12 flex items-center ">
          <div className="text-white text-base font-semibold mr-2">From </div>
          <div className="bg-white">
            <DatePicker
              disableFuture
              // openTo="year"
              // className="text-2xl"
              // sx={{ color: "white" }}
              format="DD/MM/yyyy"
              label="Start Date"
              views={["year", "month", "date"]}
              value={selectedStartDate}
              onChange={handleStartDateChange}
            />
          </div>
        </div>
        <div className="mx-2 flex items-center w-2/12">
          <div className="text-white text-base font-semibold mr-2">To </div>
          <div className="bg-white">
            <DatePicker
              disableFuture
              // openTo="year"
              format="DD/MM/yyyy"
              label="End Date"
              views={["year", "month", "date"]}
              value={selectedEndDate}
              onChange={handleEndDateChange}
            />
          </div>
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
