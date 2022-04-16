import axios from "axios";
import { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
const optionsBar = {
  responsive: true,
  // indexAxis: "y",
  maintainAspectRatio: false,

  // barThickness: 6,
  plugins: {
    legend: {
      // position: 'top',
      // display: true,
    },
    title: {
      display: true,
      text: "Trending Words",
    },
  },
};

const WordCloud = () => {
  const [words, setWords] = useState([]);
  const [counts, setCounts] = useState([]);

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
        data.sort((a, b) => b[1] - a[1]);
        let wordsTemp = data.map((datum) => datum[0]);
        let countTemp = data.map((datum) => datum[1]);
        console.log(countTemp);
        setWords(wordsTemp.slice(0, 10));
        setCounts(countTemp.slice(0, 10));
      });
  }, []);
  return (
    <div>
      <Bar
        options={optionsBar}
        data={{
          labels: words,
          datasets: [
            {
              label: "Total Word Count",
              data: counts,
              backgroundColor: "#247881",
            },
          ],
        }}
      />
    </div>
  );
};

export default WordCloud;
