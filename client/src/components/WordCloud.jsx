import axios from "axios";
import { useEffect, useState } from "react";
import ReactWordcloud from "react-wordcloud";

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
        // data.sort((a, b) => b[1] - a[1]);
        // let wordsTemp = data.map((datum) => datum[0]);
        // let countTemp = data.map((datum) => datum[1]);
        // console.log(countTemp);
        // setWords(wordsTemp.slice(0, 10));
        // setCounts(countTemp.slice(0, 10));
      });
  }, []);
  return <div>{loading && <ReactWordcloud words={words} />}</div>;
};

export default WordCloud;
