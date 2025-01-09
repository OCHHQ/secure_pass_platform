import { FaEye, FaEdit, FaTrash, FaShare } from 'react-icons/fa';
import PropTypes from 'prop-types';

const VaultsFolders = ({folders = []}) => {
    
  return (
    <div>{folders.length > 0 && (
                <div className='flex flex-col gap-4 justify-center border-2 border-gray-300 rounded-lg p-4'>
                    <h2 className="text-3xl font-medium text-center">Folders</h2>
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
                                    <button className="active:scale-[.98] bg-indigo-600 text-white p-2 rounded-xl mt-4 hover:bg-indigo-500 lg:text-base md:text-sm text-xs flex items-center gap-2 font-medium">
                                        <FaEye /> View
                                    </button>
                                    <button className="active:scale-[.98] bg-green-500 text-white p-2 rounded-xl mt-4 hover:bg-green-400 lg:text-base md:text-sm text-xs flex items-center gap-2 font-medium">
                                        <FaEdit /> Edit
                                    </button>
                                    <button className="active:scale-[.98] bg-red-500 text-white p-2 rounded-xl mt-4 hover:bg-red-400 lg:text-base md:text-sm text-xs flex items-center gap-2 font-medium">
                                        <FaTrash /> Delete
                                    </button>
                                    <button className="active:scale-[.98] bg-indigo-600 text-white p-2 rounded-xl mt-4 hover:bg-indigo-500 lg:text-base md:text-sm text-xs flex items-center gap-2 font-medium">
                                        <FaShare /> Share
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}</div>
  )
}
VaultsFolders.propTypes = {
    folders: PropTypes.array.isRequired,
};


export default VaultsFolders