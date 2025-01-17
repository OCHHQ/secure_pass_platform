import Header from "../Header/Header"
import Sidebare from "../Sidebar/Sidebar"
import Footer from "../Footer/Footer"
import { useUser } from "../Context/UserContext";
import { useEffect, useState } from "react";
import { getUser, updateUser } from "../api/api";
import { FaUserCircle } from "react-icons/fa";

function Profile() {
    const { user } = useUser();
    const { id } = user;
    const [userProfile, setUserProfile] = useState({});
    const [isLoading, setIsLoading] = useState(true);
    const [edit, setEdit] = useState(false);
    const [editPassword, setEditPassword] = useState(false);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const user = await getUser(id);
                setUserProfile(user);
                setIsLoading(false);
            } catch (error) {
                console.error("Error fetching user:", error);
                setIsLoading(false);
            }
        };
        fetchUser();
    }, [id]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setUserProfile((prevProfile) => ({
            ...prevProfile,
            [name]: value,
        }));
    };

    const handleSave = async () => {
        try {
            await updateUser(id, userProfile);
            setEdit(false);
            setEditPassword(false);
        } catch (error) {
            console.error("Error updating user:", error);
        }
    };

    return (
        <>
            <Header />
            <div className="flex bg-[#F9F6F3]">
                <Sidebare />
                <div id='Profile' className='block w-full pt-20 pl-8'>
                    <div className='h-full rounded-tl-3xl shadow-2xl p-8 bg-[#F9F6F3]'>
                        {isLoading ? (
                            <div className="flex justify-center items-center h-96">
                                <p className="text-center">Loading...</p>
                            </div>
                        ) : (edit ? (
                            <div className='flex flex-col gap-4 font-semibold'>
                                <label htmlFor="firstname"> Firstname:</label>
                                <input type="text" id="firstname" className="border-2 border-gray-300 p-2 rounded-lg" value={userProfile.firstname} name="firstname" onChange={handleChange} />
                                <label htmlFor="lastname"> Lastname:</label>
                                <input type="text" id="lastname" className="border-2 border-gray-300 p-2 rounded-lg" value={userProfile.lastname} name="lastname" onChange={handleChange} />
                                <label htmlFor="email"> Email:</label>
                                <input type="text" id="email" className="border-2 border-gray-300 p-2 rounded-lg" value={userProfile.email} name="email" onChange={handleChange} />
                                <div className="flex flex-col gap-4">
                                    {editPassword ? (
                                        <div>
                                            <label htmlFor="password"> Password:</label>
                                            <input type="text" id="password" className="border-2 border-gray-300 p-2 rounded-lg" value={userProfile.password} name="password" onChange={handleChange} />
                                        </div>
                                    ) : (
                                        <button className="bg-[#7A4FE7] hover:bg-blue-700 text-xl text-white font-bold py-2 px-4 rounded-full mt-10" onClick={() => setEditPassword(true)}>Edit password</button>
                                    )}
                                    <button className="bg-red-500 hover:bg-red-700 text-xl text-white font-bold py-2 px-4 rounded-full " onClick={() => { setEdit(false); setEditPassword(false); }}>Cancel</button>
                                    <button className="bg-blue-500 hover:bg-blue-700 text-xl text-white font-bold py-2 px-4 rounded-full" onClick={handleSave}>Save</button>
                                </div>
                            </div>
                        ) : (
                            <div className='flex flex-col gap-4 m-10'>
                                <div className="flex flex-col justify-center items-center">
                                    <FaUserCircle className="w-20 h-20 text-[#7A4FE7]" />
                                    <p className='text-xl font-semibold'>{userProfile.firstname + " " + userProfile.lastname} </p>
                                </div>
                                <div className="flex flex-col gap-4 shadow-2xl p-8 bg-[#F9F6F3] rounded-3xl">
                                    <p className='text-xl font-semibold'>Firstname: {userProfile.firstname}</p>
                                    <p className='text-xl font-semibold'>Lastname: {userProfile.lastname}</p>
                                    <p className='text-xl font-semibold'>Email: {userProfile.email}</p>
                                </div>
                                <button className="bg-blue-500 hover:bg-blue-700 text-xl text-white font-bold py-2 px-4 rounded-full w-1/2 self-center mt-10" onClick={() => setEdit(true)}>Edit</button>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
            <Footer />
        </>
    );
}

export default Profile;