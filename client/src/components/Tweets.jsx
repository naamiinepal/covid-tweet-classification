import { Card } from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import { columns } from "../constants";
import { useFilter } from "./FilterProvider";
import Selection from "./Selection";
import Tweet from "./Tweet";
const Tweets = () => {
  const [dataList, setDataList] = useState([]);
  const [offset, setOffset] = useState(0);
  const [topic, setTopic] = useState("none");
  const [reload, setReload] = useState(true);
  let { year, month } = useFilter();

  const [description, setDescription] = useState("All tweets.");
  useEffect(() => {
    let params = { offset: offset, limit: 10 };
    if (year !== "none" && month !== "none") {
      params["month"] = `${year}-${month}`;
    }
    if (topic !== "none") {
      params["topics"] = topic;
    }
    axios
      .get(`/tweets/`, { params })
      .then((data) => data.data)
      .then((data) => {
        console.log(data);
        setDataList((dl) => [...dl, ...data]);
      });
  }, [offset, topic, year, month]);
  useEffect(() => {
    let params = { offset: 0, limit: 10 };
    if (topic !== "none") {
      params["topics"] = topic;
    }
    if (year !== "none" && month !== "none") {
      params["month"] = `${year}-${month}`;
    }
    axios
      .get(`/tweets/`, { params })
      .then((data) => data.data)
      .then((data) => {
        console.log(data);
        setDataList(data);
      });
  }, [reload, topic, year, month]);

  useEffect(() => {
    const current_descrip =
      topic !== "none"
        ? columns.filter((column) => column.field === topic)[0].description
        : "All tweets.";
    setDescription(current_descrip);
  }, [reload, topic]);

  const fetchData = () => {
    setOffset(offset + 10);
  };
  const toggleReload = () => {
    setReload(!reload);
  };

  return (
    <div className="w-11/12 items-stretch flex justify-between mx-auto ">
      <Card className="w-3/12 mr-3 p-3 h-96">
        <div className="font-bold text-center text-2xl text-primary">
          Filter
        </div>
        <Selection
          offset={offset}
          setOffset={setOffset}
          topic={topic}
          toggleReload={toggleReload}
          endUser={true}
          setTopic={setTopic}
        />
        <div className="text-base">{description}</div>
      </Card>
      <div className="w-3/4 overflow-y-auto">
        <InfiniteScroll
          dataLength={dataList.length} //This is important field to render the next data
          next={fetchData}
          height={384}
          hasMore={true}
          loader={<h4>Loading...</h4>}
          endMessage={
            <p style={{ textAlign: "center" }}>
              <b>Yay! You have seen it all</b>
            </p>
          }
        >
          {dataList.map((datum) => (
            <Tweet tweet={datum} key={datum.id} />
          ))}
        </InfiniteScroll>
      </div>
    </div>
  );
};

export default Tweets;
