import { Card } from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import { columns } from "../constants";
import Selection from "./Selection";
import Tweet from "./Tweet";
const Tweets = () => {
  const [dataList, setDataList] = useState([]);
  const [offset, setOffset] = useState(0);
  const [topic, setTopic] = useState("none");
  const [reload, setReload] = useState(true);
  const [description, setDescription] = useState("All tweets.");
  useEffect(() => {
    axios
      .get(
        `/tweets/?offset=${offset}&limit=10${
          topic !== `none` ? `&filter_topic=${topic}` : ""
        }`
      )
      .then((data) => data.data)
      .then((data) => {
        console.log(data);
        setDataList((dl) => [...dl, ...data]);
      });
  }, [offset, topic]);
  useEffect(() => {
    axios
      .get(
        `/tweets/?offset=${offset}&limit=10${
          topic !== `none` ? `&filter_topic=${topic}` : ""
        }`
      )
      .then((data) => data.data)
      .then((data) => {
        console.log(data);
        setDataList(data);
      });
  }, [offset, reload, topic]);

  useEffect(() => {
    setDescription(getDescription());
  }, [getDescription, reload, topic]);

  const getDescription = () =>
    topic !== "none"
      ? columns.filter((column) => column.field === topic)[0].description
      : "All tweets.";

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
