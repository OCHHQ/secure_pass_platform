import { useState, useEffect } from "react";
import { getVaultsByUser } from "../api/api";
import { useUser } from "../Context/UserContext";
import Footer from "../Footer/Footer";
import Header from "../Header/Header";
import Vaults from "../Vaults/Vaults";
import VaultsForm from "../Vaults/VaultsForm";


const VaultsPage = () => {
    const {user} = useUser ();
    const {id} = user;
    const [vaultForm, setVaultForm] = useState (false);
    const [isloading, setIsLoading] = useState(true);
    const [listVaults, setListVaults] = useState([]);

    useEffect(() => {
        const fetchVaults = async () => {
            try {
                const vaults = await getVaultsByUser(id);
                setListVaults(vaults);
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
        <Header/>
        <div id='Vaults' className='block md:p-20 pt-10 bg-[#F9F6F3]'>
            <div className=''>
                <h1 className=" text-3xl text-center font-semibold my-8">Welcome to your vaults</h1>
            </div>
            {isloading ? (
                <p>Loading...</p>
            ) : (
                <Vaults userID={id} listVaults={listVaults} setVaultForm={setVaultForm}/>
            )}
            {vaultForm && <VaultsForm userID ={id} setVaultForm={setVaultForm} />}
        </div>
        <Footer/>
        </>
    );
};

export default VaultsPage;