import { Card } from "@mui/material";
import axios from "axios";
import Title from "./Title";
import { useEffect, useState } from "react";
import ReactWordcloud from "react-wordcloud";
const options = {
  colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
  enableTooltip: true,
  deterministic: false,
  fontFamily: "impact",
  fontSizes: [5, 60],
  fontStyle: "normal",
  fontWeight: "normal",
  padding: 3,
  rotations: 3,
  rotationAngles: [0, 90],
  scale: "sqrt",
  spiral: "archimedean",
  transitionDuration: 1000,
};
const WordCloud = () => {
  const [words, setWords] = useState([]);
  // const [counts, setCounts] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let params = new URLSearchParams();
    params.append("month", "2021-09");
    // if (year !== "none" && month !== "none") {
    //   params.append("month", `${year}-${month}`);
    // }
    axios
      .get("/tweets_commons/", { params })
      .then((data) => data.data)
      .then((data) => {
        // console.log(data);
        let wordCount = data.map((datum) => {
          return { text: datum[0], value: datum[1] };
        });
        console.log(wordCount);
        setWords(wordCount);
        setLoading(true);
      });
  }, []);
  return (
    <div>
      {loading && (
        <Card className="p-3 h-96 mt-24 ml-2">
          <Title text={"Trending Words"}></Title>
          <ReactWordcloud options={options} words={words} />
        </Card>
      )}
    </div>
  );
};

export default WordCloud;
