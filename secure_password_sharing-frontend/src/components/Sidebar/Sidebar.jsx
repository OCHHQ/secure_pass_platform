import { FaTachometerAlt, FaFolder,FaLock, FaCog } from 'react-icons/fa';
import { Link } from "react-router-dom";

const menuItems = [
    {
        icons: <FaTachometerAlt size={30}/>,
        label: 'Dashboard',
        link: '/dashboard'
    },
    {
        icons: <FaFolder size={30}/>,
        label: 'Folders',
        list: [
            {
                label: 'Folders list',
                link: '/folders'
            },
            {
                label: 'Add Folder',
                link: '/folders'
            },
        ]
    },
    {
        icons: <FaLock size={30}/>,
        label: 'Vaults',
        list: [
            {
                label: 'Vaults list',
                link: '/vaults'
            },
            {
                label: 'Add Vault',
                link: '/vaults'
            },
        ]
    },
    {
        icons: FaCog({size: 30}),
        label: 'Settings',
        list: [
            {
                label: 'Profile',
                link: '/profile'
            },
            {
                label: 'Change Password',
                link: '/change-password'
            },
        ]
    }
]


function Sidebar() {
  return (
<aside className="md:flex hidden ">
    <div className="mt-14 flex flex-col w-64 h-screen bg-[#7A4FE7] text-white backdrop:blur-3xl">
        <div className="flex flex-col p-4 gap-4">
            {menuItems.map((item, index) => (
                <div key={index}>
                    <div className="flex items-center space-x-4 py-2">
                        <span>{item.icons}</span>
                        <span className='text-xl font-semibold hover:bg-white hover:text-gray-800 hover:rounded-xl hover:p-1 hover:font-semibold'><Link to={item.link}>{item.label}</Link></span>
                    </div>
                    {item.list && (
                        <div className="pl-12">
                            {item.list.map((subItem, index) => (
                                <div key={index} className="flex items-center space-x-4 py-2">
                                    <span className='hover:font-semibold hover:bg-white hover:text-gray-800 hover:rounded-xl hover:p-1'><Link to={subItem.link}>{subItem.label}</Link></span>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            ))}
        </div>
    </div>
</aside>
  )
}

export default Sidebar