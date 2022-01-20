import { Chip, Modal, Typography } from '@mui/material';
import { Box } from '@mui/system';
import { DataGrid } from '@mui/x-data-grid';
import React, { Component, useEffect, useState } from 'react';
import { CSVReader } from 'react-papaparse';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import axios from 'axios';
const buttonRef = React.createRef();


const TweetCollection = () => {
  const [dataList, setDataList] = useState([])
  const [selectedRow, setSelectedRow] = useState(undefined)
  const [modalDisplay, setModalDisplay] = useState(false)
  useEffect(() => {if(selectedRow){
    setModalDisplay(true)
  }
  }, [selectedRow])
  const columns = [
    {field:"id",headerName:"S.N"},
    {
        "field": "text",
        "headerName": "text",
        width:500,
    },
    {
        "field": "covid_stats",
        "headerName": "covid_stats"
    },
    {
        "field": "vaccination",
        "headerName": "vaccination"
    },
    {
        "field": "covid_politics",
        "headerName": "covid_politics"
    },
    {
        "field": "humour",
        "headerName": "humour"
    },
    {
        "field": "lockdown",
        "headerName": "lockdown"
    },
    {
        "field": "civic_views",
        "headerName": "civic_views"
    },
    {
        "field": "life_during_pandemic",
        "headerName": "life_during_pandemic"
    },
    {
        "field": "covid_waves_and_variants",
        "headerName": "covid_waves_and_variants"
    },
    {
        "field": "misinformation",
        "headerName": "misinformation"
    },
    {
        "field": "others",
        "headerName": "others"
    }
]
  useEffect(()=>{
    axios.get(`/tweets/?offset=1&limit=10`).then((data)=>data.data).then((data)=>setDataList(data))
  },[])

  return (
    <div>
      {/* <h5>Basic Upload</h5> */}
       
        <Modal
        open={modalDisplay}
        onClose={()=>setModalDisplay(false)}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={{position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'white',
  // border: '2px solid #000',
  boxShadow: 24,
  p: 4,}}>
    <Typography id="modal-modal-description" >
            {selectedRow && Object.keys(selectedRow).map((rowElement)=>{
              if(selectedRow[rowElement]==true){
                return (<Chip className='mr-1' label={rowElement} color='success' />)
              }else{
                return <></>
              }
            })}
          </Typography>
          <Typography id="modal-modal-title" sx={{ mt: 2 }} variant="h5" component="h2">
            {selectedRow && selectedRow.text}
          </Typography>
          
        </Box>
      </Modal>
<div className='w-11/12 mx-auto h-96'>
      <DataGrid
        rows={dataList}
        className='bg-blue-50'
        columns={columns}
        pageSize={100}
        rowsPerPageOptions={[100]}
        onRowDoubleClick={(params)=>{
          console.log(params)
          setSelectedRow(params.row)
          
        }}
        // checkboxSelection
        // disableSelectionOnClick
      />
    </div>
    </div>
  )
}

export default TweetCollection

