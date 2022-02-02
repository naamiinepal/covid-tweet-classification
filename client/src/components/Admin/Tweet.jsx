import { Button, Checkbox, TableCell, TableRow } from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";

const Tweet = ({ row }) => {
  const [changedColumn, setChangedColumn] = useState({ ...row });
  const [isVerified, setIsVerified] = useState(
    "verified_at" in Object.keys(row)
  );
  useEffect(() => {
    setChangedColumn({ ...row });
    setIsVerified("verified_at" in Object.keys(row));
  }, [row]);
  const verifySubmit = () => {
    let toSubmit = {};
    for (const prop in row) {
      if (row[prop] !== changedColumn[prop]) {
        toSubmit[prop] = changedColumn[prop];
      }
    }
    let accessToken = sessionStorage.getItem("accessToken");
    console.log(accessToken);
    axios
      .patch(`/tweets/pseudo/${row.id}`, toSubmit, {
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
        {isVerified ? (
          <Button color="success" onClick={verifySubmit}>
            {"Verified"}
          </Button>
        ) : (
          <Button variant="contained" onClick={verifySubmit}>
            {"Verify"}
          </Button>
        )}
      </TableCell>
      {Object.keys(row)
        .filter(
          (datum) =>
            datum !== "created_at" && datum !== "username" && datum !== "id"
        )
        .map((datum) => {
          if (datum === "text")
            return <TableCell align="left">{`${row[`${datum}`]}`}</TableCell>;
          else
            return (
              <TableCell align="right">
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
