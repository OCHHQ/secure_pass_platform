import { useState } from "react";
import PropTypes from "prop-types";
import { FaKey, FaPlus } from "react-icons/fa";
import { deleteVaultById, updateVault,createShare } from "../api/api";

const Vaults = ({ userID = " ", listVaults = [], setVaultForm}) => {
  const [showPassword, setShowPassword] = useState(false);
  const [Vaults, setVaults] = useState(listVaults);
  const [showConfirm, setShowConfirm] = useState(false);
  const [vault, setVault] = useState(null);
  const [vaultEdit, setVaultEdit] = useState(false);
  const [vaultShare, setVaultShare] = useState(false);
  const [duration, setDuration] = useState(0);

  const deleteVault = (id) => {
    setVaults(Vaults.filter((vault) => vault.id !== id));
    deleteVaultById(userID, id);
  };

  const handleDeleteClick = (id) => {
    setVault(id);
    setShowConfirm(true);
  };

  const confirmDelete = () => {
    if (vault !== null) {
      deleteVault(vault);
      setVault(null);
      setShowConfirm(false);
    }
  };
  const editVault = (vault) => {
    setVault(vault);
    setVaultEdit(true);
  };

  const saveVault = (id, data) => {
    const updatedVaults = Vaults.map((vault) => {
      if (vault.id === id) {
        return { ...vault, ...data };
      }
      return vault;
    });
    setVaults(updatedVaults);
    updateVault(userID, id, data);
    setVaultEdit(false);
    setVault(null);
  };

  const Cancel = () => {
    setVault(null);
    setVaultEdit(false);
    setVaultShare(false);
    setShowConfirm(false);
  };

  const Share = (vault) => {
    setVault(vault);
    setVaultShare(true);
  };

  const Generate = (vault, userID, duration) => {
    const date = new Date();
    const expiry = new Date(date.getTime() + duration * 3600000).toISOString().split('T')[0];
    const shareData = {
        id: Math.random().toString(36).substr(2, 9),
        username: vault.username,
        password: vault.password,
        expiry: expiry,
        
  };
    createShare(userID, vault.id, shareData);
    setVaultShare(false);
    setVault(null);
    }

  return (
    <>
      <div className="flex flex-col justify-center ">
        <div className="flex flex-col gap-4 ">
          {Vaults.length > 0 ? (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2 md:p-8 p-4 rounded-3xl shadow-2xl">
                {Vaults.map((vault) => (
                  <div
                    key={vault.id}
                    className="flex flex-col justify-between border-2 border-gray-300 rounded-lg p-4"
                  >
                    <h2 className="text-lg md:text-2xl lg:text-3xl font-medium text-center p-2 md:p-4 lg:p-8">
                      {vault.name}
                    </h2>
                    <div className="flex flex-col border-t-2 border-[#E5E5E5]">
                      <span className="p-2">
                        <h3 className="text-left text-xs md:text-sm lg:text-base">
                          {vault.username}
                        </h3>
                      </span>
                      <span className="p-2">
                        <input
                          type={showPassword === vault.id ? "text" : "password"}
                          readOnly
                          onClick={() =>
                            setShowPassword(
                              showPassword === vault.id ? false : vault.id
                            )
                          }
                          value={vault.password}
                          className="border-0 bg-transparent w-full focus:border-0"
                        />
                      </span>
                    </div>
                    <div className="flex flex-row md:flex-row md:justify-around md:gap-4 justify-center gap-2">
                      <button
                        className="w-1/2 bg-blue-500 text-white p-2 rounded-lg text-xs md:text-sm lg:text-base"
                        onClick={() => editVault(vault)}
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDeleteClick(vault.id)}
                        className="w-1/2 bg-red-500 text-white p-2 rounded-lg text-xs md:text-sm lg:text-base"
                      >
                        Delete
                      </button>
                      <button
                        className="w-1/2 bg-indigo-600 text-white p-2 rounded-lg text-xs md:text-sm lg:text-base"
                        onClick={() => Share(vault)}
                      >
                        Share
                      </button>
                    </div>
                  </div>
                ))}
              </div>
              <div className="flex flex-col gap-4">
                <button
                  className="my-8 bg-indigo-600 text-white self-center p-2 w-3/4 md:w-1/2 rounded-lg shadow-2xl text-xs md:text-sm lg:text-base"
                  onClick={() => setVaultForm(true)}
                >
                  Create Vault
                </button>
              </div>
            </>
          ) : (
            <div className="flex flex-col gap-4 w-full h-screen p-8">
              <p className="text-sm md:text-lg font-medium text-left mt-4 md:w-1/2">
                When you save something in PassShare, it appears here.
                Passwords, You save it, the vault stores it
              </p>
              <button
                className="p-4 md:p-8 rounded-lg flex flex-row justify-around border-2 shadow-2xl mt-20 w-full md:w-8/12 bg-[#F9F6F3]"
                onClick={() => setVaultForm(true)}
              >
                <FaKey className="inline-block mr-2 text-blue-500 self-center" />{" "}
                <span className="w-3/4 text-center md:text-left">
                  {" "}
                  <h2 className="text-sm md:text-lg lg:text-2xl text-[#007AFF] font-bold">
                    Add your first password
                  </h2>
                  <p className="hidden md:block text-xs md:text-sm lg:text-lg md:font-semibold">
                    Every great PassShare experience starts with just one
                    password. Try it!
                  </p>
                </span>
                <FaPlus className="inline-block ml-2 text-blue-500 self-center" />
              </button>
            </div>
          )}
        </div>
      </div>

      {showConfirm && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-8 font-semibold text-xl rounded-lg shadow-xl">
            <p>Are you sure you want to delete this vault?</p>
            <div className="flex  gap-2 mt-4">
              <button
                onClick={confirmDelete}
                className="bg-red-500 w-1/2 text-white p-2 rounded-lg"
              >
                Yes
              </button>
              <button
                onClick={Cancel}
                className="bg-[#7A4FE7] w-1/2 text-white p-2 rounded-lg"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
      {vaultEdit && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <form className="bg-white p-8 font-semibold text-xl rounded-lg shadow-xl ">
            <label htmlFor="username" className="p-4">
              Username:
            </label>
            <input
              type="text"
              name="username"
              id="username"
              value={vault?.username || ""}
              onChange={(e) => setVault({ ...vault, username: e.target.value })}
            />
            <label htmlFor="password" className="p-4">
              Password:
            </label>
            <input
              type="text"
              name="password"
              id="password"
              value={vault?.password || ""}
              onChange={(e) => setVault({ ...vault, password: e.target.value })}
            />
            <div className="flex  gap-2 mt-4">
              <button
                onClick={() => saveVault(vault.id, vault)}
                className="bg-red-500 w-1/2 text-white p-2 rounded-lg"
              >
                Save
              </button>
              <button
                onClick={Cancel}
                className="bg-[#7A4FE7] w-1/2 text-white p-2 rounded-lg"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}
      {vaultShare && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="p-4 font-semibold text-xl rounded-lg shadow-xl bg-white">
            <p className="p-4">Share this vault with another user</p>
            <label htmlFor="Duratation" className="p-4">
              Duratation:
            </label>
            <input
              type="number"
              placeholder="Set Duratation"
              id="Duratation"
              name="Duratation"
              className="p-2 border-2 border-gray-300 rounded-lg"
              min={0}
              onChange={(e) => setDuration(e.target.value)}
            />
            <div className="flex  gap-2 mt-4">
              <button
                onClick={() => Generate(vault, userID, duration)}
                className="bg-indigo-600 w-1/2 text-white p-2 rounded-lg"
              >
                Generate
              </button>
              <button
                onClick={Cancel}
                className="bg-[#7A4FE7] w-1/2 text-white p-2 rounded-lg"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

Vaults.propTypes = {
  setVaultForm: PropTypes.func.isRequired,
  listVaults: PropTypes.array.isRequired,
  userID: PropTypes.string.isRequired,
};

export default Vaults;
