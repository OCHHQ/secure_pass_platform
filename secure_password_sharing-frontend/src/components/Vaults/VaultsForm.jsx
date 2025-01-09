
import PropTypes from 'prop-types';
import { useState } from 'react';
import {createVault} from '../api/api';

const VaultsForm = ({userID = "", setVaultForm}) => {

  const [isLoading, setIsLoading] = useState(false);

  const [vaultsData, setVaultsData] = useState({
    folder_name: "",
    name: "",
    description: "",
    username: "",
    password: "",
    confirmPassword: "",
  });

 const handleSubmit = async (e) => {
     e.preventDefault();
     setIsLoading(true);
 
     if (vaultsData.password !== vaultsData.confirmPassword) {
      alert("password incompatible");
       setIsLoading(false);
       return;
     }
 
     createVault(userID, vaultsData);
      setIsLoading(false);
      setVaultForm(false);

   };
 
   const handleChange = (e) => {
     const { name, value } = e.target;
     setVaultsData({ ...vaultsData, [name]: value });
   };

  return (
    <div className='fixed top-0 left-0 w-full h-full bg-[#7A4FE7] backdrop-blur-sm bg-opacity-10 z-40'>
    <div className=' fixed w-full md:w-1/2 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-[#F9F6F3] p-4 border-4 rounded-xl border-[#7A4FE7] shadow-lg z-50'>
                <h1 className="text-2xl font-medium text-center py-4">Create Vault</h1>
                <form onSubmit={handleSubmit} className="flex flex-col gap-4" >
                    <input onChange={handleChange} type="text" placeholder="Folder Name" name="folder_name" value={vaultsData.folderName} className="border-2 border-gray-400 placeholder:font-medium hover:border-indigo-600 focus:outline-indigo-600 active:scale-[0.98] bg-transparent rounded-lg p-4" />
                    <input onChange={handleChange} type="text" placeholder="Vault Name" name="name" value={vaultsData.name} required className="border-2 border-gray-400 placeholder:font-medium hover:border-indigo-600 focus:outline-indigo-600 active:scale-[0.98] bg-transparent rounded-lg p-4" />
                    <input onChange={handleChange} type="text" placeholder="Description" name="description" value={vaultsData.description} className="border-2 border-gray-400 placeholder:font-medium hover:border-indigo-600 focus:outline-indigo-600 active:scale-[0.98] bg-transparent rounded-lg p-4" />
                    <input onChange={handleChange} type="text" placeholder="Username" name="username" required value={vaultsData.username} className="border-2 border-gray-400 placeholder:font-medium hover:border-indigo-600 focus:outline-indigo-600 active:scale-[0.98] bg-transparent rounded-lg p-4" />
                    <input onChange={handleChange} type="password" placeholder="Password" name="password" required value={vaultsData.password} className="border-2 border-gray-400 placeholder:font-medium hover:border-indigo-600 focus:outline-indigo-600 active:scale-[0.98] bg-transparent rounded-lg p-4" />
                    <input onChange={handleChange} type="password" placeholder="Confirm Password" name="confirmPassword" required value={vaultsData.confirmPassword} className="border-2 border-gray-400 placeholder:font-medium hover:border-indigo-600 focus:outline-indigo-600 active:scale-[0.98] bg-transparent rounded-lg p-4" />
                    <div className='flex flex-wrap gap-4 justify-center'>
                    <button className="w-1/4 bg-[#7A4FE7] text-white p-2 rounded-lg" type='submit'>
                    {isLoading?
                    <div className='flex gap-2'>
                    <p>Creating...</p>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-[#7A4FE7]"></div>
                    </div>
                    :
                    <p className='text-xl font-semibold'>Create</p>
                    } 
                     </button>
                    <button className="w-1/4 bg-[#7A4FE7] text-white p-2 rounded-lg" onClick={() => setVaultForm(false)}>Cancel</button>
                    </div>
                </form>
            </div>
      </div>
  )
}
VaultsForm.propTypes = {
  setVaultForm: PropTypes.func.isRequired,
  userID: PropTypes.string.isRequired,
};

export default VaultsForm;