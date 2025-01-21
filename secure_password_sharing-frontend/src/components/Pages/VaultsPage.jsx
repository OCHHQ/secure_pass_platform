import { useState, useEffect } from "react";
import { getVaultsByUser } from "../api/api";
import { useUser } from "../Context/UserContext";
import Footer from "../Footer/Footer";
import Header from "../Header/Header";
import Vaults from "../Vaults/Vaults";
import VaultsForm from "../Vaults/VaultsForm";

const VaultsPage = () => {
    const { user } = useUser();
    const { id } = user;
    const [vaultForm, setVaultForm] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [listVaults, setListVaults] = useState([]);

    const fetchVaults = async () => {
        setIsLoading(true);  // Set loading to true again while fetching data
        try {
            const vaults = await getVaultsByUser(id);
            setListVaults(vaults);
        } catch (error) {
            console.error("Error fetching vaults:", error);
        } finally {
            setIsLoading(false);  // Set loading to false once data is fetched
        }
    };

    useEffect(() => {
        fetchVaults(); // Initial fetch when the component mounts
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [id]);

    const addVaultToList = (newVault) => {
        setListVaults((prevList) => [...prevList, newVault]); // Add the new vault to the existing list
        fetchVaults();
    };

    return (
        <>
            <Header />
            <div id='Vaults' className='block md:p-20 pt-10 bg-[#F9F6F3]'>
                <div className=''>
                    <h1 className="text-3xl text-center font-semibold my-8">Welcome to your vaults</h1>
                </div>
                {isLoading ? (
                    <p>Loading...</p>
                ) : (
                    <Vaults userID={id} listVaults={listVaults} setVaultForm={setVaultForm}/>
                )}
                {vaultForm && <VaultsForm userID={id} setVaultForm={setVaultForm} addVaultToList={addVaultToList}  />}
            </div>
            <Footer />
        </>
    );
};

export default VaultsPage;