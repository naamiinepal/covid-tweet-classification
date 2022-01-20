// import './App.css';
import React from 'react';
import TweetCollection from './components/CSVReader';
import { LineChart } from './components/LineChart';
import Nav from './components/Nav';
import Purpose from './components/Purpose';

function App() {
  return (
    <div className='bg-blue-50 pb-16'>
      <Nav />
      <div className='mt-3'>
      <Purpose />
      <LineChart />
      <TweetCollection />

      </div>
      
      {/* <DataGridDemo /> */}
    </div>
  );
}

export default App;
