// Desc: FoldersPage component
//       This component is a placeholder for the FoldersPage component.
import { useEffect, useState } from "react"
import { useUser } from "../Context/UserContext"
import Footer from "../Footer/Footer"
import Header from "../Header/Header"
import VaultsFolders from "../Vaults/VaultsFolders"
import {getFolders} from '../api/api'
const FoldersPage = () => {

    const {user} = useUser ();
    const {id} = user;

    const [folders, setFolders] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchFolders = async () => {
            try {
                const folders = await getFolders(id);
                setFolders(folders);
                setIsLoading(false);
            } catch (error) {
                console.error("Error fetching folders:", error);
                setIsLoading(false);
            }
        };
        fetchFolders();
    }
    , [id]);

  return (
    <>
    <Header />
    <div className="block md:p-20 pt-10 bg-[#F9F6F3]">
    <div className=''>
                    <h1 className="text-3xl text-center font-semibold my-8">Welcome to your Folders</h1>
    </div>
        {isLoading ? (
            <p>Loading...</p>
        ) : (
            <VaultsFolders folders= {folders} setFolders={setFolders}/>
        )}
      
    </div>
    <Footer />
    </>
  )
}

export default FoldersPage