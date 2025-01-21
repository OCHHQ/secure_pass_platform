import { useEffect, useState } from "react";
import { useUser } from "../Context/UserContext";
import Header from "../Header/Header";
import { getVaultsByUser,deleteShare } from "../api/api";

const SharePage = () => {
    const {user} = useUser ();
    const {id} = user;
    const [vaults, setVaults] = useState([]);
    const [isloading, setIsLoading] = useState(true);
    const [showConfirm, setShowConfirm] = useState(false);
    const [confirm, setConfirm] = useState(false);
    const [idvault, setIdVault] = useState(null);
    const [idshare, setIdShare] = useState(null);

    useEffect(() => {
            const fetchVaults = async () => {
                try {
                    const vaults = await getVaultsByUser(id);
                    setVaults(vaults);
                    setIsLoading(false);
                } catch (error) {
                    console.error("Error fetching vaults:", error);
                    setIsLoading(false);
                }
            };
            fetchVaults();
        }, [id]);

    const handleDeleteClick = (idvault,idshare) => {
        console.log(idvault,idshare);
        setIdVault(idvault);
        setIdShare(idshare);
        setShowConfirm(true);
    }

    if (confirm) {
        deleteShare(id, idvault, idshare).then((updatedVaults) => {
            setVaults(updatedVaults);
        }).catch((error) => {
            console.error("Error updating vaults:", error);
        });
        setConfirm(false);
        setShowConfirm(false);
    }


    return (
        <>
            <Header />
            <div id='Share' className='block md:p-20 pt-10 bg-[#F9F6F3]'>
                <div className='flex flex-col gap-4 w-full h-screen p-4'>
                    <p className='text-3xl text-center font-semibold my-8'>List of shared vaults:</p>
                    <div className='flex flex-col gap-4 rounded-3xl shadow-2xl p-8 bg-[#F9F6F3]'>
                        {isloading ? (
                            <p>Loading...</p>
                        ) : (
                            <table className='min-w-full bg-[#F9F6F3] h-auto border-2 border-gray-300 rounded-xl p-4'>
                                <thead>
                                    <tr className="border-b text-center p-">
                                        <th className='py-4'>Username</th>
                                        <th className='py-4'>Password</th>
                                        <th className='py-4'>Expiry</th>
                                        <th className='py-4'>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {vaults.map((vault) =>
                                        vault.shares?.map((share) => (
                                            <tr key={share.id} className='border-b text-center'>
                                                <td className='py-2 px-4 text-blue-500'>{share.username}</td>
                                                <td className='py-2 px-4'>
                                                    <input
                                                        type="password"
                                                        value={share.password}
                                                        readOnly
                                                        className='bg-transparent border-none focus:outline-none hover:outline-none text-center'
                                                    />
                                                </td>
                                                <td className='py-2 px-4'>{share.expiry}</td>
                                                <td className='py-2 px-4'>
                                                    <button className='text-white bg-blue-500 hover:bg-blue-700 py-1 px-2 rounded-md'>
                                                        Copy
                                                    </button>
                                                    <button className='text-white bg-red-500 hover:bg-red-700 py-1 px-2 rounded-md'
                                                        onClick={() => handleDeleteClick(vault.id ,share.id)}
                                                    >
                                                        Delete
                                                    </button>
                                                </td>
                                            </tr>
                                        ))
                                    )}
                                </tbody>
                            </table>
                        )}
                    </div>
                </div>
            </div>
            {showConfirm && (
                <div className='fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 flex justify-center items-center'>
                    <div className='bg-white p-8 rounded-xl shadow-2xl'>
                        <p className="text-pretty font-semibold mb-4">Are you sure you want to delete this share?</p>
                        <button
                            className='w-1/2 text-white bg-red-500 hover:bg-red-700 py-1 px-2 rounded-md'
                            onClick={() => setShowConfirm(false)}
                        >
                            Cancel
                        </button>
                        <button
                            className='w-1/2 text-white bg-blue-500 hover:bg-blue-700 py-1 px-2 rounded-md'
                            onClick={() => setConfirm(true)}
                        >
                            Confirm
                        </button>
                    </div>
                </div>
            )   
            }
        </>
    );
};

export default SharePage;