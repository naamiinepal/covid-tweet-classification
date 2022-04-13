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
import {useEffect, useState} from "react";
import {columns} from "../../constants";
import Selection from "../Selection";
import Tweet from "./Tweet";
// const buttonRef = React.createRef();

const TweetCollectionAdminPanel = ({action}) => {
    const [dataList, setDataList] = useState([]);
    const [offset, setOffset] = useState(0);
    const [topic, setTopic] = useState("none");
    const [reload, setReload] = useState(true);

    useEffect(() => {
        axios
            .get(
                `/${
                    action === "verify" ? "pseudo_tweets" : "tweets"
                }/?offset=${offset}&limit=10${
                    topic !== `none` ? `&topics=${topic}` : ""
                }&maximize_labels=true`,
            )
            .then((data) => data.data)
            .then((data) => {
                console.log(data);
                setDataList(data);
            });
    }, [offset, topic, reload, action]);
    const toggleReload = () => {
        setReload(!reload);
    };
    return (
        <div className=" mt-10 w-11/12 mx-auto ">
            <Selection
                offset={offset}
                setOffset={setOffset}
                topic={topic}
                toggleReload={toggleReload}
                setTopic={setTopic}
            />
            <TableContainer component={Paper} sx={{height: 500}}>
                <Table
                    stickyHeader
                    sx={{minWidth: 650, borderSpacing: "0 20px"}}
                    aria-label="simple table"
                >
                    <colgroup>
                        <col width="80%" />
                        <col width="2%" />
                        <col width="2%" />
                        <col width="2%" />
                        <col width="2%" />
                        <col width="2%" />
                        <col width="2%" />
                        <col width="2%" />
                        <col width="2%" />
                        <col width="6%" />
                    </colgroup>
                    <TableHead>
                        <TableRow>
                            {columns
                                .filter((column) => column.field !== "others")
                                .map((column, index) => {
                                    return (
                                        <TableCell
                                            key={index}
                                            sx={{
                                                width: 50,
                                                fontWeight: "bold",
                                            }}
                                        >
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
                                row={{...row}}
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
