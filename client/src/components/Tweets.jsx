import { Card } from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import { useFilter } from "./FilterProvider";
import Selection from "./Selection";
import Tweet from "./Tweet";
import WordCloud from "./WordCloud";
const Tweets = () => {
  const [dataList, setDataList] = useState([]);
  const [offset, setOffset] = useState(0);
  const [topics, setTopics] = useState([]);
  const [reload, setReload] = useState(true);
  let { year, month } = useFilter();

  // const [description, setDescription] = useState("All tweets.");

  useEffect(() => {
    setDataList([]);
  }, [year, month, topics.length]);

  useEffect(() => {
    // let params = { offset: offset, limit: 10 };
    let params = new URLSearchParams([
      ["offset", offset],
      ["limit", 10],
    ]);
    if (year !== "none" && month !== "none") {
      params.append("month", `${year}-${month}`);
    }
    if (topics.length !== 0) {
      topics.forEach((topic) => {
        params.append("topics", topic);
      });
    }
    axios
      .get(`/tweets/`, {
        params,
      })
      .then((data) => data.data)
      .then((data) => {
        console.log(data);
        setDataList((dl) => [...dl, ...data]);
      });
  }, [offset, topics, topics.length, year, month]);
  // useEffect(() => {
  //   let params = new URLSearchParams([
  //     ["offset", 0],
  //     ["limit", 10],
  //   ]);
  //   if (year !== "none" && month !== "none") {
  //     params.append("month", `${year}-${month}`);
  //   }
  //   if (topics.length !== 0) {
  //     topics.forEach((topic) => {
  //       params.append("topics", topic);
  //     });
  //   }
  //   axios
  //     .get(`/tweets/`, {
  //       params,
  //     })
  //     .then((data) => data.data)
  //     .then((data) => {
  //       console.log(data);
  //       setDataList(data);
  //     });
  // }, [reload, topics.length, year, month]);

  // useEffect(() => {
  //   const current_descrip =
  //     topics !== "none"
  //       ? columns.filter((column) => column.field === topics)[0].description
  //       : "All tweets.";
  //   setDescription(current_descrip);
  // }, [reload, topics]);

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
          topic={topics}
          toggleReload={toggleReload}
          endUser={true}
          setTopic={setTopics}
        />
        <WordCloud />
        {/* <div className="text-base">{description}</div> */}
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
