import {Button, InputLabel, MenuItem, Select, TextField} from "@mui/material";
import React, {useState} from "react";
import {columns} from "../constants";

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
                    label="Topic"
                    onChange={(event) => {
                        setTopic(event.target.value);
                    }}
                >
                    <MenuItem value="none">All</MenuItem>
                    {columns
                        .filter(
                            (column) =>
                                column.field !== "verify" &&
                                column.field !== "text",
                        )
                        .map((column) => (
                            <MenuItem value={column.field}>
                                {column.label}
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
            )}{" "}
        </div>
    );
};

export default Selection;
