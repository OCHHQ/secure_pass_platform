import { FaTrash} from 'react-icons/fa';
import PropTypes from 'prop-types';
import {deleteFolderById} from '../api/api';
import { useState } from 'react';
import { useUser } from '../Context/UserContext';

const VaultsFolders = ({folders = [],setFolders}) => {

    const {user} = useUser ();
    const {id} = user;

    const [showconfirmDelete, setShowConfirmDelete] = useState(false);
    const [folderToDelete, setFolderToDelete] = useState(null);

    const handleDeleteFolder = async (folderId) => {
        try {
            const updatedFolders = await deleteFolderById(id, folderId);
            setFolders(updatedFolders);
        } catch (error) {
            console.error("Error deleting folder:", error);
        }
    }
    
    
  return (
    <div className="flex flex-col justify-center ">
        <div className="flex flex-col gap-4 ">
        {folders.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2 md:p-8 p-4 rounded-3xl shadow-2xl">
                    <div className="flex gap-4 flex-wrap justify-center ">
                        {folders.map((folder) => (
                            <div
                                key={folder.id}
                                className="flex flex-col md:w-200 md:h-200 w-100 h-100 items-center border-2 border-gray-300 rounded-lg p-4"
                            >
                                <h3 className="md:text-3xl text-2xl font-medium p-4 md:p-8">{folder.name}</h3>
                                <p className="md:text-sm text-xs text-gray-600 p-2 md:p-4">{folder.description}</p>
                                <p className="md:text-sm text-xs text-gray-600">Number of Vaults: {folder.vaultId.length}</p>
                                <div className="flex gap-2">
                                    <button className="active:scale-[.98] bg-red-500 text-white p-2 rounded-xl mt-4 hover:bg-red-400 lg:text-base md:text-sm text-xs flex items-center gap-2 font-medium"
                                        onClick={() => {
                                            setShowConfirmDelete(true);
                                            setFolderToDelete(folder.id);
                                        }
                                    }>
                                        <FaTrash /> Delete
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )
            : (
                <div className="flex flex-col gap-4 w-full h-screen p-8">
                <p className="text-xl text-center">No folders found</p>
                </div>
            )}
        </div>
            {showconfirmDelete && (
                
                <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center">
                    
                    <div className="bg-white p-4 rounded-lg flex flex-col gap-4 items-center">
                        <h2 className="text-2xl font-medium">Are you sure you want to delete this folder?</h2>
                        <div className="flex gap-4">
                            <button className="bg-red-500 text-white p-2 rounded-lg" onClick={() => {
                                handleDeleteFolder(folderToDelete);
                                setShowConfirmDelete(false);
                            }}>Yes</button>
                            <button className="bg-green-500 text-white p-2 rounded-lg" onClick={() => {
                                setShowConfirmDelete(false);
                            }}>No</button>
                        </div>
                    </div>
                </div>
            )
                    }
        
        </div>
  )
}
VaultsFolders.propTypes = {
    folders: PropTypes.array.isRequired,
    setFolders: PropTypes.func.isRequired,
};


export default VaultsFolders