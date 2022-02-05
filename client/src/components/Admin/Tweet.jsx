import { Button, Checkbox, TableCell, TableRow } from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";
import { columns } from "../../constants";

const Tweet = ({ row, verified, action }) => {
  const [changedColumn, setChangedColumn] = useState({ ...row });
  const [isVerified, setIsVerified] = useState(verified);
  useEffect(() => {
    setChangedColumn({ ...row });
    setIsVerified(verified);
  }, [row, verified]);
  const modifySubmit = () => {
    let toSubmit = {};
    for (const prop in row) {
      toSubmit[prop] = changedColumn[prop];
    }
    let accessToken = sessionStorage.getItem("accessToken");
    axios
      .patch(`/tweets/${row.id}`, toSubmit, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then((data) => data.data)
      .then((data) => {
        setIsVerified(true);
      });
  };
  const verifySubmit = () => {
    let toSubmit = {};
    for (const prop in row) {
      if (row[prop] !== changedColumn[prop]) {
        toSubmit[prop] = changedColumn[prop];
      }
    }
    let accessToken = sessionStorage.getItem("accessToken");
    axios
      .patch(`/pseudo_tweets/${row.id}`, toSubmit, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then((data) => data.data)
      .then((data) => {
        setIsVerified(true);
      });
  };
  const handleChange = (event, column) => {
    let changeTemp = JSON.parse(JSON.stringify(changedColumn));
    changeTemp[column] = event.target.checked;
    console.log(changeTemp);
    setChangedColumn(changeTemp);
  };
  return (
    <TableRow
      key={row.id}
      sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
    >
      <TableCell align="right">
        {
          (action = "modify" ? (
            <Button variant="contained" onClick={modifySubmit}>
              "Modify"
            </Button>
          ) : (
            <>
              {isVerified ? (
                <Button
                  color="warning"
                  // variant="contained"
                  onClick={verifySubmit}
                >
                  "Verified"
                </Button>
              ) : (
                <Button variant="contained" onClick={verifySubmit}>
                  "Verify"
                </Button>
              )}
            </>
          ))
        }
      </TableCell>
      {columns
        .map((column) => column.field)
        .filter((datum) => datum !== "verify")
        .map((datum, index) => {
          if (datum === "text")
            return (
              <TableCell key={index} sx={{ fontSize: "1rem" }} align="left">{`${
                row[`${datum}`]
              }`}</TableCell>
            );
          else
            return (
              <TableCell key={index} align="right">
                <Checkbox
                  checked={changedColumn[`${datum}`]}
                  onChange={(event) => {
                    handleChange(event, datum);
                  }}
                />
              </TableCell>
            );
        })}
    </TableRow>
  );
};

export default Tweet;
