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
import PrivateRoute from "./components/PrivateRoute";



function App() {
  return (
    <>
    <UserProvider>
    <BrowserRouter>
    <Routes>
    <Route path="/" element={<Home />} />
            <Route path="/Login" element={<Login />} />
            <Route path="/Signup" element={<Signup />} />
            <Route path="/404" element={<ErrorPage />} /> {/* 404 error page route */}

            {/* Public route, accessible by anyone */}
            <Route path="/dashboard" element={<PrivateRoute element={<Dashboard />} />} />
            <Route path="/Vaults" element={<PrivateRoute element={<VaultsPage />} />} />
            <Route path="/Folders" element={<PrivateRoute element={<VaultsFolders />} />} />
            <Route path="/Share" element={<PrivateRoute element={<SharePage />} />} />
            <Route path="/Profile" element={<PrivateRoute element={<Profile />} />} />

            {/* If no route matches, show 404 */}
            <Route path="*" element={<ErrorPage />} />
    </Routes>
    </BrowserRouter>
    </UserProvider>
    </>
  )
}

export default App