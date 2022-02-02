import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";
import Tweet from "./Tweet";
// const buttonRef = React.createRef();

const TweetCollectionAdminPanel = () => {
  const [dataList, setDataList] = useState([]);

  const columns = [
    { field: "verify", headerName: "Verify" },
    {
      field: "text",
      headerName: "text",
      width: 500,
    },
    {
      field: "covid_stats",
      headerName: "covid_stats",
    },
    {
      field: "vaccination",
      headerName: "vaccination",
    },
    {
      field: "covid_politics",
      headerName: "covid_politics",
    },
    {
      field: "humour",
      headerName: "humour",
    },
    {
      field: "lockdown",
      headerName: "lockdown",
    },
    {
      field: "civic_views",
      headerName: "civic_views",
    },
    {
      field: "life_during_pandemic",
      headerName: "life_during_pandemic",
    },
    {
      field: "covid_waves_and_variants",
      headerName: "covid_waves_and_variants",
    },
  ];
  useEffect(() => {
    axios
      .get(`/tweets/pseudo?offset=0&limit=10&minority=true`)
      .then((data) => data.data)
      .then((data) => {
        console.log(data);
        setDataList(data);
      });
  }, []);

  return (
    <div className="mt-10">
      {/* <h5>Basic Upload</h5> */}
      <div className="w-11/12 mx-auto h-96">
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                {columns.map((column, index) => {
                  return <TableCell key={index}>{column.headerName}</TableCell>;
                })}
              </TableRow>
            </TableHead>
            <TableBody>
              {dataList.map((row, index) => (
                <Tweet key={index} row={row} />
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>
    </div>
  );
};

export default TweetCollectionAdminPanel;
