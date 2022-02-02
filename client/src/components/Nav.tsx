import Corona from "../svgs/corona";
import Name from "./Name";
   
const Nav = () => {
    return (
        <div className='border-2 bg-white px-16 py-2 flex items-center justify-start'>
            <div className='font-bold w-16'>
            <Corona />
            </div>
            <Name />
           
        </div>
    )
}

export default Nav
