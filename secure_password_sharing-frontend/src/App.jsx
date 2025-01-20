import Login from "./components/Auth/Login"
import Home from  "./components/Pages/Home"
import Signup from "./components/Auth/Signup"
import { BrowserRouter , Route, Routes } from "react-router-dom"
import Dashboard from "./components/Pages/AppHome"
import VaultsPage from "./components/Pages/VaultsPage"
import VaultsFolders from "./components/Pages/FoldersPage"
import SharePage from "./components/Pages/SharePage"
import Profile from "./components/Pages/Profile"
import { UserProvider } from "./components/Context/UserContext"
import ErrorPage from "./components/error"



function App() {
  return (
    <>
    <UserProvider>
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home/>} />
      <Route path="/Login" element={<Login />} />
      <Route path="/Signup" element={<Signup/>} />
      <Route path="/dashboard" element={<Dashboard/>} />
      <Route path="/Vaults" element={<VaultsPage/>} />
      <Route path="/Folders" element={<VaultsFolders/>} />
      <Route path="/Share" element={<SharePage/>} />
      <Route path="/Profile" element={<Profile/>} />
      <Route path="*" element={<ErrorPage/>} />
    </Routes>
    </BrowserRouter>
    </UserProvider>
    </>
  )
}

export default App