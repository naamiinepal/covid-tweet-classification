import Name from "./Name";
import TULogo from "../images/TULogo.png"
import NaamiiLogo from "../images/naamii-logo.png"
import { NavLink } from "react-router-dom";

const Nav = () => {
    return (
        <div>
        <div className='border-t-2 bg-white px-16 py-2 flex items-center justify-between'>
            <div className='font-bold w-14'>
            {/* <Corona /> */}
            <img alt="TU-Logo" src={TULogo} />

            </div>
            <Name />
                        <div className='w-14'>
            <img alt="NAAMII-Logo" src={NaamiiLogo} />
            </div>
        </div>
        <div  className='border-b-2 bg-white px-16 flex items-center justify-between'>
            <NavLink to="/" className={({ isActive }) =>
              isActive ? "text-primary underline" : "text-primary"
            }
 >Home</NavLink> 
            <NavLink to="/about" className={({ isActive }) =>
              isActive ? "text-primary underline" : "text-primary"
            }>About</NavLink> 
            <NavLink to="/ap" className={({ isActive }) =>
              isActive ? "text-primary underline" : "text-primary"
            }>Admin</NavLink> 

        </div>
        </div>

    )
}

export default Nav
