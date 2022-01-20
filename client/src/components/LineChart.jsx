import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import { baseAddress } from '../constants';
// import faker from 'faker';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Chart.js Line Chart',
    },
  },
};

const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];

export const data = {
  labels,
  datasets: [
    // {
    //   label: 'Dataset 1',
    //   data: labels.map((lab,index) => index),
    //   borderColor: 'rgb(255, 99, 132)',
    //   backgroundColor: 'rgba(255, 99, 132, 0.5)',
    // },
    {
      label: 'Dataset 2',
      data: labels.map((lab,index) => index),
      borderColor: 'rgb(53, 162, 235)',
      backgroundColor: 'rgba(53, 162, 235, 0.5)',
    },
  ],
};

const fetchLabels = (month)=>{
let covid_stats = []
let vaccination = []
let covid_politics= []
let humour= []
let lockdown= []
let civic_views= []
let life_during_pandemic= []
let covid_waves_and_variants= []
let misinformation= []
let finalData = {}
return axios.get(`/tweets/overview`).then((data)=>data.data).then((data)=>{
  finalData["labels"] = data.map((datum)=> datum.created_at)
  covid_stats = data.map(datum=> datum.covid_stats)
  vaccination = data.map(datum=> datum.vaccination)
  covid_politics = data.map(datum=> datum.covid_politics)
  humour = data.map(datum=> datum.humour)
  lockdown = data.map(datum=> datum.lockdown)
  civic_views = data.map(datum=> datum.civic_views)
  life_during_pandemic = data.map(datum=> datum.life_during_pandemic)
  covid_waves_and_variants = data.map(datum=> datum.covid_waves_and_variants)
  misinformation = data.map(datum=> datum.misinformation)
  finalData["datasets"]=[{
    label: 'Covid Stats',
    data: covid_stats,
    borderColor: 'rgb(53, 162, 235)',
    backgroundColor: 'rgba(53, 162, 235, 0.5)',
  },
  {
    label: 'Vaccination',
    data: vaccination,
    borderColor: 'rgb(53, 162, 35)',
    backgroundColor: 'rgba(53, 162, 35, 0.5)',
  },
  {
    label: 'Covid Politics',
    data: covid_politics,
    borderColor: 'rgb(53, 225, 235)',
    backgroundColor: 'rgba(53, 225, 235, 0.5)',
  },
  {
    label: 'Humour',
    data: humour,
    borderColor: 'rgb(153, 162, 235)',
    backgroundColor: 'rgba(153, 162, 235, 0.5)',
  },{
    label: 'Lockdown',
    data: lockdown,
    borderColor: 'rgb(253, 162, 235)',
    backgroundColor: 'rgba(253, 162, 235, 0.5)',
  },{
    label: 'Civic Views',
    data: civic_views,
    borderColor: 'rgb(3, 33, 235)',
    backgroundColor: 'rgba(3, 33, 235, 0.5)',
  },{
    label: 'Life during Pandemic',
    data: life_during_pandemic,
    borderColor: 'rgb(53, 12, 235)',
    backgroundColor: 'rgba(53, 12, 235, 0.5)',
  },{
    label: 'Covid Waves and Variants',
    data: covid_waves_and_variants,
    borderColor: 'rgb(53, 162, 23)',
    backgroundColor: 'rgba(53, 162, 23, 0.5)',
  },
  {
    label: 'Misinformation',
    data: misinformation,
    borderColor: 'rgb(53, 16, 23)',
    backgroundColor: 'rgba(53, 16, 23, 0.5)',
  },]
  console.log(finalData)
  return finalData
}).catch((error)=>{
  console.log(error)
})
console.log(finalData)
}
export function LineChart() {
const [labels, setLabels] = useState({})
  useEffect(async ()=>{
  const label2 = await fetchLabels()
    setLabels(label2)
  },[])
  return (
  <div>
  {labels.labels && <Line options={options} data={labels} />}
  </div>
  );
}
