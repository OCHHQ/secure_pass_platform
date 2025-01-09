/* eslint-disable react-refresh/only-export-components */
import { createContext, useState, useContext } from 'react';
import PropTypes from 'prop-types';


// Create the context
export const UserContext = createContext();

// Custom hook for easy access to the context
export const useUser = () => useContext(UserContext);

// UserProvider component to manage and provide the user state
export const UserProvider = ({ children }) => {
    const [user, setUser] = useState({
        id: '',
        email: '',
        password: '',
        isLoggedIn: false,
        Vaults:[],
        Folders:[],
        SharedVaults:[],
    });



    // Function to update the user information
    const login = (id, email, password) => {
        setUser({id, email, password, isLoggedIn: true });
    };

    const logout = () => {
        setUser({ id:'', email: '', password: '', isLoggedIn: false });
    };

    const addVault = (vault) => {
        setUser({ Vaults: [...user.Vaults, vault] });
    }

    const deleteVault = (id) => {
        setUser({ Vaults: user.Vaults.filter((vault) => vault.id !== id) });
        setUser({ SharedVaults: user.SharedVaults.filter((vault) => vault.id !== id) });
        setUser({ Folders: user.Folders.filter((vault) => vault.id !== id) });
    }
    const addFolder = (folder) => {
        setUser({ Folders: [...user.Folders, folder] });
    }
    const deleteFolder = (id) => {
        setUser({ Folders: user.Folders.filter((folder) => folder.id !== id) });
        setUser({ Vaults: user.Vaults.filter((folder) => folder.id !== id) });
        setUser({ SharedVaults: user.SharedVaults.filter((folder) => folder.id !== id) });
    }
    return (
        <UserContext.Provider value={{ user, setUser, login, logout, addVault, deleteVault, addFolder, deleteFolder }}>
            {children}
        </UserContext.Provider>
    );
};

UserProvider.propTypes = {
    children: PropTypes.node.isRequired,
};