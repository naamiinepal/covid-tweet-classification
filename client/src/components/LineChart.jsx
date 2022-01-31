import { useEffect, useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Line, Pie } from "react-chartjs-2";
import axios from "axios";
import { Card } from "@mui/material";
// import faker from 'faker';

ChartJS.register(
  ArcElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const options = {
  responsive: true,
  plugins: {
    legend: {
      position: "top",
    },
    title: {
      display: true,
      text: "Line Chart",
    },
  },
};

const optionsPie = {
  responsive: true,
  plugins: {
    legend: {
      // position: 'top',
      display: true,
    },
    title: {
      display: true,
      text: "Pie Chart",
    },
  },
};

const fetchLabels = async () =>
  axios
    .get(`/tweets/overview`)
    .then((data) => data.data)
    .then((data) => {
      const finalData = {};
      const covid_stats = data.map((datum) => datum.covid_stats);
      const vaccination = data.map((datum) => datum.vaccination);
      const covid_politics = data.map((datum) => datum.covid_politics);
      const humour = data.map((datum) => datum.humour);
      const lockdown = data.map((datum) => datum.lockdown);
      const civic_views = data.map((datum) => datum.civic_views);
      const life_during_pandemic = data.map(
        (datum) => datum.life_during_pandemic
      );
      const covid_waves_and_variants = data.map(
        (datum) => datum.covid_waves_and_variants
      );
      finalData["labels"] = data.map((datum) => datum.created_date);
      finalData["datasets"] = [
        {
          label: "Covid Stats",
          data: covid_stats,
          borderColor: "rgb(19, 138, 51)",
          backgroundColor: "rgba(19, 138, 51, 0.5)",
        },
        {
          label: "Vaccination",
          data: vaccination,
          borderColor: "rgb(255, 3, 226)",
          backgroundColor: "rgba(255, 3, 226, 0.5)",
        },
        {
          label: "Covid Politics",
          data: covid_politics,
          borderColor: "rgb(235, 128, 52)",
          backgroundColor: "rgba(235, 128, 52, 0.5)",
        },
        {
          label: "Humour",
          data: humour,
          borderColor: "rgb(195, 235, 52)",
          backgroundColor: "rgba(195, 235, 52, 0.5)",
        },
        {
          label: "Lockdown",
          data: lockdown,
          borderColor: "rgb(0, 174, 255)",
          backgroundColor: "rgba(0, 174, 255, 0.5)",
        },
        {
          label: "Civic Views",
          data: civic_views,
          borderColor: "rgb(255, 36, 3)",
          backgroundColor: "rgba(255, 36, 3, 0.5)",
        },
        {
          label: "Life during Pandemic",
          data: life_during_pandemic,
          borderColor: "rgb(255, 3, 129)",
          backgroundColor: "rgba(255, 3, 129, 0.5)",
        },
        {
          label: "Covid Waves and Variants",
          data: covid_waves_and_variants,
          borderColor: "rgb(255, 196, 3)",
          backgroundColor: "rgba(255, 196, 3, 0.5)",
        },
        {
          label: "Misinformation",
          data: misinformation,
          borderColor: "rgb(53, 16, 23)",
          backgroundColor: "rgba(53, 16, 23, 0.5)",
        },
      ];
      console.log(finalData);
      return finalData;
    })
    .catch((error) => {
      console.log(error);
    });

function LineChart() {
  const [labels, setLabels] = useState({});
  const [loading, setLoading] = useState(false);

  const [pieData, setPieData] = useState({ labels: [] });
  useEffect(() => {
    const pieLabels = [
      "Covid Stats",
      "Vaccination",
      "Covid Politics",
      "Humour",
      "Lockdown",
      "Civic Views",
      "Life During Pandemic",
      "Covid Waves and Variants",
      "Misinformation",
    ];
    fetchLabels().then((label2) => {
      if (label2.labels) {
        const dataTemp = label2.datasets.map((datum) =>
          datum.data.reduce((prev, curr) => prev + curr, 0)
        );
        setPieData({
          labels: pieLabels,
          datasets: [
            {
              label: "Pie Chart",
              data: dataTemp,
              backgroundColor: [
                "rgb(19, 138, 51)",
                "rgb(255, 3, 226)",
                "rgb(235, 128, 52)",
                "rgb(195, 235, 52)",
                "rgb(0, 174, 255)",
                "rgb(255, 36, 3)",
                "rgb(255, 3, 129)",
                "rgb(255, 196, 3)",
                "rgb(53, 16, 23)",
              ],
            },
          ],
        });
      }
      setLabels(label2);
      setLoading(true);
    });
  }, []);

  return (
    <div className="flex w-11/12 my-3 mx-16">
      {loading && (
        <Card className="flex-1">
          <Line options={options} data={labels} />
        </Card>
      )}
      {loading && (
        <Card className="w-1/3 ml-3">
          <Pie options={optionsPie} data={pieData} />
        </Card>
      )}
    </div>
  );
}

export { options, optionsPie };
export default LineChart;
