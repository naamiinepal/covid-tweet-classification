import React from 'react'

const Title = ({text}:{text:string}) => {
    return (
        <div className='text-2xl font-bold  text-primary'>
            {text}
        </div>
    )
}

export default Title
