import { useEffect, useState } from "react";
import { useUser } from "../Context/UserContext";
import Header from "../Header/Header";
import { getVaultsByUser } from "../api/api";

const SharePage = () => {
    const {user} = useUser ();
    const {id} = user;
    const [vaults, setVaults] = useState([]);

    const [isloading, setIsLoading] = useState(true);

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
        </>
    );
};

export default SharePage;