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
import { columns } from "../../constants";
import Tweet from "./Tweet";
// const buttonRef = React.createRef();

const TweetCollectionAdminPanel = ({ action }) => {
  const [dataList, setDataList] = useState([]);
  const [offset, setOffset] = useState(0);
  const [minority, setMinority] = useState(true);
  const [offsetTemp, setOffsetTemp] = useState(offset);
  const [reload, setReload] = useState(true);

  useEffect(() => {
    axios
      .get(
        `${action === "verify" ? "pseudo_tweets" : "tweets"}
          /?offset=${offset}&limit=10&minority=${minority}`
      )
      .then((data) => data.data)
      .then((data) => {
        console.log(data);
        setDataList(data);
      });
  }, [offset, minority, reload, action]);

  return (
    <div className=" mt-10 w-11/12 mx-auto ">
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
            <col width="6%" />
            <col width="80%" />
            <col width="2%" />
            <col width="2%" />
            <col width="2%" />
            <col width="2%" />
            <col width="2%" />
            <col width="2%" />
            <col width="2%" />
            <col width="2%" />
          </colgroup>
          <TableHead>
            <TableRow>
              {columns.map((column, index) => {
                return (
                  <TableCell key={index} sx={{ width: 50, fontWeight: "bold" }}>
                    {column.headerName}
                  </TableCell>
                );
              })}
            </TableRow>
          </TableHead>
          <TableBody>
            {dataList.map((row, index) => (
              <Tweet
                key={index}
                row={{ ...row }}
                action={action}
                verified={!!row["verified_at"]}
              />
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default TweetCollectionAdminPanel;
