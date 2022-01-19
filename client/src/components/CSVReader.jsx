import { Chip, Modal, Typography } from '@mui/material';
import { Box } from '@mui/system';
import { DataGrid } from '@mui/x-data-grid';
import React, { Component, useEffect, useState } from 'react';
import { CSVReader } from 'react-papaparse';
import FileUploadIcon from '@mui/icons-material/FileUpload';
const buttonRef = React.createRef();


const CSVReader1 = () => {
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
  const handleOpenDialog = (e) => {
    // Note that the ref is set async, so it might be null at some point
    if (buttonRef.current) {
      buttonRef.current.open(e);
    }
  };

  const handleOnFileLoad = (data) => {
    console.log('---------------------------');
    let dictData = data.slice(1).map((datum,index) => {return {
      id:index,
      text:datum.data[0],
      covid_stats:datum.data[1],
      vaccination:datum.data[2],
      covid_politics:datum.data[3],
      humour:datum.data[4],
      lockdown:datum.data[5],
      civic_views:datum.data[6],
      life_during_pandemic:datum.data[7],
      covid_waves_and_variants:datum.data[8],
      misinformation:datum.data[9],
      others:datum.data[10],

    }})
    setDataList(dictData)
    console.log(data)
    console.log('---------------------------');
  };

  const handleOnError = (err, file, inputElem, reason) => {
    console.log('---------------------------');
    console.log(err);
    console.log('---------------------------');
  };

  const handleOnRemoveFile = (data) => {
    console.log('---------------------------');
    console.log(data);
    console.log('---------------------------');
  };

  const handleRemoveFile = (e) => {
    // Note that the ref is set async, so it might be null at some point
    if (buttonRef.current) {
      buttonRef.current.removeFile(e);
    }
  };
  return (
    <div>
      {/* <h5>Basic Upload</h5> */}
        <CSVReader
          ref={buttonRef}
          onFileLoad={handleOnFileLoad}
          onError={handleOnError}
          noClick
          noDrag
          onRemoveFile={handleOnRemoveFile}
        >
          {({ file }) => (
            <aside
              style={{
                display: 'flex',
                flexDirection: 'row',
                marginBottom: 10,
              }}
            >
              <button
                type="button"
                onClick={handleOpenDialog}
                style={{
                  marginLeft:"60px"
                }}
              >
<FileUploadIcon/>              </button>
              {/* <div
                style={{
                  borderWidth: 1,
                  borderStyle: 'solid',
                  borderColor: '#ccc',
                  height: 45,
                  lineHeight: 2.5,
                  marginTop: 5,
                  marginBottom: 5,
                  paddingLeft: 13,
                  paddingTop: 3,
                  width: '60%',
                }}
              >
                {file && file.name}
              </div>
              <button
                style={{
                  borderRadius: 0,
                  marginLeft: 0,
                  marginRight: 0,
                  paddingLeft: 20,
                  paddingRight: 20,
                }}
                onClick={handleRemoveFile}
              >
                Remove
              </button> */}
            </aside>
          )}
        </CSVReader>
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
              if(selectedRow[rowElement]==="1"){
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

export default CSVReader1

