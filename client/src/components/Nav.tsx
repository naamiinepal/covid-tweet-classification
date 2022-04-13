import Name from "./Name";
import TULogo from "../images/TULogo.png"
import NaamiiLogo from "../images/naamii-logo.png"

const Nav = () => {
    return (
        <div className='border-2 bg-white px-16 py-2 flex items-center justify-between'>
            <div className='font-bold w-14'>
            {/* <Corona /> */}
            <img alt="TU-Logo" src={TULogo} />

            </div>
            <Name />
                        <div className='w-14'>

            <img alt="TU-Logo" src={NaamiiLogo} />
            </div>
        </div>
    )
}

export default Nav
