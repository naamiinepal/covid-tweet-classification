import {
  Button,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
} from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";
import Tweet from "./Tweet";
// const buttonRef = React.createRef();

const TweetCollectionAdminPanel = () => {
  const [dataList, setDataList] = useState([]);
  const [offset, setOffset] = useState(0);
  const [minority, setMinority] = useState(true);
  const [offsetTemp, setOffsetTemp] = useState(offset);
  const [reload, setReload] = useState(true);
  const columns = [
    { field: "verify", headerName: "Verify" },
    {
      field: "text",
      headerName: "text",
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
      .get(`/tweets/pseudo/?offset=${offset}&limit=10&minority=${minority}`)
      .then((data) => data.data)
      .then((data) => {
        console.log(data);
        setDataList(data);
      });
  }, [offset, minority, reload]);

  return (
    <div className=" mt-10 w-11/12 mx-auto h-96">
      <div className="w-3/12 flex justify-between items-end mb-3">
        <div>
          <InputLabel id="minority">Minority</InputLabel>
          <Select
            labelId="minority"
            id="minority-select"
            value={minority}
            label="Minority"
            onChange={(event) => {
              setMinority(event.target.value);
            }}
          >
            <MenuItem value={true}>True</MenuItem>
            <MenuItem value={false}>False</MenuItem>
          </Select>
        </div>
        <TextField
          label={"Offset"}
          value={offsetTemp}
          type={"number"}
          onChange={(event) => {
            setOffsetTemp(event.target.value);
          }}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              setOffset(offsetTemp);
            }
          }}
        />
        <Button
          onClick={() => {
            setReload(!reload);
          }}
        >
          Refuel
        </Button>
      </div>

      <TableContainer component={Paper} sx={{ height: 500 }}>
        <Table stickyHeader sx={{ minWidth: 650 }} aria-label="simple table">
          <colgroup>
            <col width={"6%"} />
            <col width={"80%"} />
            <col width={"2%"} />
            <col width={"2%"} />
            <col width={"2%"} />
            <col width={"2%"} />
            <col width={"2%"} />
            <col width={"2%"} />
            <col width={"2%"} />
            <col width={"2%"} />
          </colgroup>
          <TableHead>
            <TableRow>
              {columns.map((column, index) => {
                return (
                  <TableCell key={index} sx={{ width: 50 }}>
                    {column.headerName}
                  </TableCell>
                );
              })}
            </TableRow>
          </TableHead>
          <TableBody>
            {dataList.map((row, index) => (
              <Tweet key={index} row={{ ...row }} />
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default TweetCollectionAdminPanel;
