import Header from "../Header/Header";
import Footer from "../Footer/Footer";
import Sidebar from "../Sidebar/Sidebar";
import { motion } from "framer-motion";
import StatCard from "../StatCard/StatCard";
import { SiZap } from "react-icons/si";
import { FaFolderOpen } from "react-icons/fa";
import { FaShareAlt } from "react-icons/fa";
import VaultsOverviewChart from "../Overview/VaultsOverviewChart";
import { useUser } from "../Context/UserContext";
import { getUser} from "../api/api";
import { useEffect, useState } from "react";

function Dashboard() {

  const { user } = useUser();
  const {id} = user;
  const [vaultUser, setVaultUser] = useState({});


  useEffect(() => {
    async function fetchUser() {
      const user = await getUser(id);
      setVaultUser(user);
    }
    fetchUser();
  }, [id]);

  return (
    <>
      <Header></Header>
      <div className="flex  bg-[#F9F6F3]">
        <Sidebar></Sidebar>
        <div className="flex-grow mt-20 px-4 sm:px-6 lg:px-8  ">
          {/* STATS */}
          <motion.div
            className="grid grid-cols-1 gap-5 md:grid-cols-3 lg:grid-cols-4 mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1 }}
          >
            <StatCard
              name="Total Vaults"
              icon={SiZap}
              value={vaultUser.vaults?.length || 0}
              color="#6366F1"
            />
            <StatCard
              name="Total Folders"
              icon={FaFolderOpen}
              value={vaultUser.folders?.length || 0} 
              color="#8B5CF6"
            />
            <StatCard
              name="Total Shares"
              icon={FaShareAlt}
              value={vaultUser.sharedVaults?.length || 0}
              color="#EC4899"
            />
          </motion.div>
          
          {/* CHARTS */}
				<div className='grid grid-cols-1 '>
					<VaultsOverviewChart />
				</div>
        
        </div>
        
      </div>
      <Footer />
    </>
  );
}

export default Dashboard;
