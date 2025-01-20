import axios from 'axios';

export const API_URL = 'http://localhost:5000';

// Get all users
export const getUsers = async () => {
  const response = await axios.get(`${API_URL}/users`);
  return response.data;
};

export const getUserByEmail = async (email) => {
  const response = await axios.get(`${API_URL}/users`);
  const users = response.data;

  // Find user by email
  const user = users.find((user) => user.email === email);

  if (!user) {
    return null;
  }
  return user;
};

// Get a single user
export const getUser = async (userId) => {
  const response = await axios.get(`${API_URL}/users/${userId}`);
  return response.data || [];
};

// Update a user
export const updateUser = async (userId, updatedUserData) => {
  await axios.put(`${API_URL}/users/${userId}`, updatedUserData);
};

// Delete a vault by id and the endpoint is users
export const getVaultsByUser = async (userId) => {
  try {
    const response = await axios.get(`${API_URL}/users/${userId}`);
    return response.data.vaults || [];
  } catch (error) {
    console.error("Error fetching vaults:", error);
    throw error;
  }
};

// Delete a specific vault for a user
export const deleteVaultById = async (userId, vaultId) => {
  try {
    // Fetch the user's data
    const userResponse = await axios.get(`${API_URL}/users/${userId}`);
    const user = userResponse.data;

    // Filter out the vault to be deleted
    const updatedVaults = user.vaults.filter((vault) => vault.id !== vaultId);

    // Update the user's vaults
    await axios.put(`${API_URL}/users/${userId}`, {
      ...user,
      vaults: updatedVaults,
    });

    // Delete all shares for the vault if it exists
    const vault = user.vaults.find((vault) => vault.id === vaultId);
    if (vault.shares) {
      for (const share of vault.shares) {
        await deleteShare(userId, vaultId, share.id);
      }
    }
    // Delete vault from all folders
    const folders = await getFolders(userId);
    for (const folder of folders) {
      if (folder.vaultId.includes(vaultId)) {
        const updatedFolder = {
          ...folder,
          vaultId: folder.vaultId.filter((id) => id !== vaultId),
        };
        await updateFolder(userId, folder.id, updatedFolder);
      }
    }

    return updatedVaults;
  } catch (error) {
    console.error("Error deleting vault:", error);
    throw error;
  }
};

// Create a new vault for a user
export const createVault = async (userId, vaultData) => {
  try {
    // Fetch the user's data
    const userResponse = await axios.get(`${API_URL}/users/${userId}`);
    const user = userResponse.data;

    // Create a new vault
    const newVault = {
      id: Math.random().toString(36).substr(2, 9),
      ...vaultData,
    };

    // Update the user's vaults
    const updatedVaults = [...user.vaults, newVault];
    await axios.put(`${API_URL}/users/${userId}`, {
      ...user,
      vaults: updatedVaults,
    });

    return newVault;
  } catch (error) {
    console.error("Error creating vault:", error);
    throw error;
  }
};

// Update a vault for a user
export const updateVault = async (userId, vaultId, updatedVaultData) => {
  try {
    // Fetch the user's data
    const userResponse = await axios.get(`${API_URL}/users/${userId}`);
    const user = userResponse.data;

    // Find the vault to be updated
    const updatedVaults = user.vaults.map((vault) => {
      if (vault.id === vaultId) {
        return {
          ...vault,
          ...updatedVaultData,
        };
      }
      return vault;
    });

    // Update the user's vaults
    await axios.put(`${API_URL}/users/${userId}`, {
      ...user,
      vaults: updatedVaults,
    });

    return updatedVaults;
  } catch (error) {
    console.error("Error updating vault:", error);
    throw error;
  }
};

// Create a share for a vault
export const createShare = async (userId, vaultId, shareData) => {
  try {
    // Fetch the user's data
    const userResponse = await axios.get(`${API_URL}/users/${userId}`);
    const user = userResponse.data;

    // Find the vault to be shared
    const updatedVaults = user.vaults.map((vault) => {
      if (vault.id === vaultId) {
        return {
          ...vault,
          shares: [...(vault.shares || []), shareData],
        };
      }
      return vault;
    });

    // Update the user's vaults
    await axios.put(`${API_URL}/users/${userId}`, {
      ...user,
      vaults: updatedVaults,
    });

    return updatedVaults;
  } catch (error) {
    console.error("Error creating share:", error);
    throw error;
  }
};

// Delete a share for a vault
export const deleteShare = async (userId, vaultId, shareId) => {
  try {
    // Fetch the user's data
    const userResponse = await axios.get(`${API_URL}/users/${userId}`);
    const user = userResponse.data;

    // Find the vault to be updated
    const updatedVaults = user.vaults.map((vault) => {
      if (vault.id === vaultId) {
        return {
          ...vault,
          shares: vault.shares.filter((share) => share.id !== shareId),
        };
      }
      return vault;
    });

    // Update the user's vaults
    await axios.put(`${API_URL}/users/${userId}`, {
      ...user,
      vaults: updatedVaults,
    });
    return updatedVaults;
  } catch (error) {
    console.error("Error deleting share:", error);
    throw error;
  }
};

// Create a new folder for a user
export const createFolder = async (userId, folderData) => {
  try {
    // Fetch the user's data
    const userResponse = await axios.get(`${API_URL}/users/${userId}`);
    const user = userResponse.data;

    // Create a new folder
    const newFolder = {
      id: Math.random().toString(36).substr(2, 9),
      ...folderData,
    };

    // Update the user's folders
    const updatedFolders = [...user.folders, newFolder];
    await axios.put(`${API_URL}/users/${userId}`, {
      ...user,
      folders: updatedFolders,
    });

    return updatedFolders;
  } catch (error) {
    console.error("Error creating folder:", error);
    throw error;
  }
};

// Get all folders for a user
export const getFolders = async (userId) => {
  try {
    const response = await axios.get(`${API_URL}/users/${userId}`);
    return response.data.folders || [];
  } catch (error) {
    console.error("Error fetching folders:", error);
    throw error;
  }
};

// Get folder by id for a user
export const getFolderById = async (userId, folderId) => {
  try {
    const response = await axios.get(`${API_URL}/users/${userId}`);
    const user = response.data;

    // Find the folder by id
    const folder = user.folders.find((folder) => folder.id === folderId);

    return folder;
  } catch (error) {
    console.error("Error fetching folder:", error);
    throw error;
  }
};

// Delete a folder for a user
export const deleteFolderById = async (userId, folderId) => {
  try {
    // Fetch the user's data
    const userResponse = await axios.get(`${API_URL}/users/${userId}`);
    const user = userResponse.data;

    // Filter out the folder to be deleted
    const updatedFolders = user.folders.filter((folder) => folder.id !== folderId);

    // Update the user's folders
    await axios.put(`${API_URL}/users/${userId}`, {
      ...user,
      folders: updatedFolders,
    });

    return updatedFolders;
  } catch (error) {
    console.error("Error deleting folder:", error);
    throw error;
  }
};

// Update a folder for a user
export const updateFolder = async (userId, folderId, updatedFolderData) => {
  try {
    // Fetch the user's data
    const userResponse = await axios.get(`${API_URL}/users/${userId}`);
    const user = userResponse.data;

    // Find the folder to be updated
    const updatedFolders = user.folders.map((folder) => {
      if (folder.id === folderId) {
        return {
          ...folder,
          ...updatedFolderData,
        };
      }
      return folder;
    });

    // Update the user's folders
    await axios.put(`${API_URL}/users/${userId}`, {
      ...user,
      folders: updatedFolders,
    });

    return updatedFolders;
  } catch (error) {
    console.error("Error updating folder:", error);
    throw error;
  }
}
