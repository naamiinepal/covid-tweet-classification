import {
  Box,
  Button,
  Checkbox,
  Chip,
  InputLabel,
  ListItemText,
  MenuItem,
  Select,
  TextField,
} from "@mui/material";
import React, { useState } from "react";
import { columns } from "../constants";

const Selection = ({
  offset,
  topic,
  setOffset,
  setTopic,
  toggleReload,
  endUser = false,
}) => {
  const [offsetTemp, setOffsetTemp] = useState(offset);
  return (
    <div className="w-5/12 flex justify-between items-end mb-3">
      <div className="w-1/2">
        <InputLabel id="minority">Topic</InputLabel>
        <Select
          labelId="minority"
          id="minority-select"
          value={topic}
          multiple
          renderValue={(selected) => (
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
              {selected.map((value) => (
                <Chip key={value} label={value} />
              ))}
            </Box>
          )}
          label="Topic"
          onChange={(event) => {
            const {
              target: { value },
            } = event;
            setTopic(typeof value === "string" ? value.split(",") : value);
          }}
        >
          <MenuItem value="none">All</MenuItem>
          {columns
            .filter(
              (column) => column.field !== "verify" && column.field !== "text"
            )
            .map((column) => (
              <MenuItem key={column.field} value={column.field}>
                <Checkbox checked={topic.indexOf(column.field) > -1} />
                <ListItemText primary={column.label} />
              </MenuItem>
            ))}
        </Select>
      </div>
      {!endUser && (
        <>
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
              toggleReload();
            }}
          >
            Refuel
          </Button>
        </>
      )}
    </div>
  );
};

export default Selection;
