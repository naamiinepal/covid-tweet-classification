
import SearchIcon from '@mui/icons-material/Search';
import React from 'react'
import { styled, alpha } from '@mui/material/styles';

import Corona from '../svgs/corona'
import Name from './Name'
import { InputBase } from '@mui/material';
const Search = styled('div')(({ theme }) => ({
    position: 'relative',
    borderRadius: theme.shape.borderRadius,
    backgroundColor: alpha(theme.palette.common.white, 0.15),
    '&:hover': {
      backgroundColor: alpha(theme.palette.common.white, 0.25),
    },
    marginRight: theme.spacing(2),
    marginLeft: 0,
    width: '100%',
    [theme.breakpoints.up('sm')]: {
      marginLeft: theme.spacing(3),
      width: 'auto',
    },
  }));
  
   
const Nav = () => {
    return (
        <div className='border-2 bg-white px-16 py-2 flex items-center justify-start'>
            <div className='font-bold w-16'>
            <Corona />
            </div>
            <Name />
            
            <div className='ml-auto'>
              <SearchIcon />
              <InputBase  placeholder="Search…"
              inputProps={{ 'aria-label': 'search' }} />
        
            
          </div>
        </div>
    )
}

export default Nav
