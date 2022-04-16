import { useEffect, useRef, useState } from "react";
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
  Filler,
  BarElement,
} from "chart.js";
import { Line } from "react-chartjs-2";
import axios from "axios";
import { Card } from "@mui/material";
import { columns } from "../constants";
import zoomPlugin from "chartjs-plugin-zoom";
import { useFilter } from "./FilterProvider";
import BarChart from "./BarChart";

// import faker from 'faker';

ChartJS.register(
  ArcElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  BarElement,
  zoomPlugin,
  Tooltip,
  Legend,
  Filler
);

const options = {
  responsive: true,
  cubicInterpolationMode: "monotone",
  plugins: {
    legend: {
      position: "top",
    },
    tooltip: { cornerRadius: 0 },
    title: {
      display: true,
      text: "Line Chart",
    },

    zoom: {
      zoom: {
        wheel: {
          enabled: false,
        },
        drag: {
          enabled: false,
        },
        mode: "x",
      },
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: "Day",
      },
    },
    y: {
      stacked: true,
      title: {
        display: true,
        text: "Tweet Count",
      },
    },
  },
};

const optionsPie = {
  responsive: true,
  indexAxis: "y",
  maintainAspectRatio: false,

  // barThickness: 6,
  plugins: {
    legend: {
      // position: 'top',
      // display: true,
    },
    title: {
      display: true,
      text: "Bar Graph",
    },
  },
};

const fetchLabels = async (year, month) =>
  axios
    .get(`/pseudo_tweets/overview?all=true`)
    .then((data) => data.data)
    .then((data) => {
      const finalData = {};
      if (data) {
        console.log(data[0].created_date.substring(5, 7));

        if (year !== "none" && month !== "none") {
          data = data.filter(
            (datum) =>
              parseInt(datum.created_date.substring(0, 4)) === parseInt(year) &&
              parseInt(datum.created_date.substring(5, 7)) === parseInt(month)
          );
        }
      }

      const covid_stats = data.map((datum) => datum.covid_stats);
      const vaccination = data.map((datum) => datum.vaccination);
      const covid_politics = data.map((datum) => datum.covid_politics);
      const humour = data.map((datum) => datum.humour);
      const lockdown = data.map((datum) => datum.lockdown);
      const civic_views = data.map((datum) => datum.civic_views);
      const others = data.map((datum) => datum.others);
      const life_during_pandemic = data.map(
        (datum) => datum.life_during_pandemic
      );
      const covid_waves_and_variants = data.map(
        (datum) => datum.covid_waves_and_variants
      );
      const dataArrays = {
        covid_stats: covid_stats,
        vaccination: vaccination,
        covid_politics: covid_politics,
        humour: humour,
        lockdown: lockdown,
        civic_views: civic_views,
        life_during_pandemic: life_during_pandemic,
        covid_waves_and_variants: covid_waves_and_variants,
        others: others,
      };
      finalData["labels"] = data.map((datum) => datum.created_date);
      finalData["datasets"] = columns
        .filter(
          (column) => column.field !== "text" && column.field !== "verify"
        )
        .map((column) => {
          return {
            data: dataArrays[column.field],
            label: column.label,
            fill: true,
            borderColor: column.areaColor,
            backgroundColor: column.areaColor,
          };
        });

      console.log(finalData);
      return finalData;
    })
    .catch((error) => {
      console.log(error);
    });

function LineChart() {
  const [labels, setLabels] = useState({});
  const [loading, setLoading] = useState(false);
  const { year, month } = useFilter();
  const chartRef = useRef(null);
  // const [pieData, setPieData] = useState({ labels: [] });
  // const resetZoom = () => {
  //   chartRef.current.resetZoom();
  // };

  useEffect(() => {
    fetchLabels(year, month).then((label2) => {
      setLabels(label2);
      setLoading(true);
    });
  }, [year, month]);

  return (
    <div className="flex w-11/12 my-3 mx-16">
      {loading && (
        <Card className="flex-1">
          {/* <Button onClick={resetZoom}>Zoom Out</Button> */}
          <Line ref={chartRef} options={options} data={labels} />
        </Card>
      )}
      <BarChart />
    </div>
  );
}

export { options, optionsPie };
export default LineChart;
