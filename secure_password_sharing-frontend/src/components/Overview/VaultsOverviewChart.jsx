import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { motion } from "framer-motion";

const vaultData = [
	{ month: "Jul", vaultsAccessed: 0 },
	{ month: "Aug", vaultsAccessed: 0 },
	{ month: "Sep", vaultsAccessed: 0 },
	{ month: "Oct", vaultsAccessed: 0 },
	{ month: "Nov", vaultsAccessed: 0 },
	{ month: "Dec", vaultsAccessed: 0 },
	{ month: "Jan", vaultsAccessed: 0 },
	{ month: "Feb", vaultsAccessed: 0 },
	{ month: "Mar", vaultsAccessed: 0 },
	{ month: "Apr", vaultsAccessed: 0 },
	{ month: "May", vaultsAccessed: 0 },
	{ month: "Jun", vaultsAccessed: 0 },
  ];

const VaultsOverviewChart = () => {
	return (
		<motion.div
			className=' bg-white bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-4 md:p-6 border border-gray-200 '
			initial={{ opacity: 0, y: 20 }}
			animate={{ opacity: 1, y: 0 }}
			transition={{ delay: 0.2 }}
		>
			<h2 className='text-lg font-medium mb-4 text-gray-800'>Vaults Overview</h2>

			<div className='h-80'>
				<ResponsiveContainer width={"100%"} height={"100%"}>
					<LineChart data={vaultData}>
						<CartesianGrid strokeDasharray='3 3' stroke='#4B5563' />
						<XAxis dataKey={"month"} stroke='#9ca3af' />
						<YAxis stroke='#9ca3af' />
						<Tooltip
							contentStyle={{
								backgroundColor: "rgba(31, 41, 55, 0.8)",
								borderColor: "#4B5563",
							}}
							itemStyle={{ color: "#E5E7EB" }}
						/>
						<Line
							type='monotone'
							dataKey='vaultsAccessed'
							stroke='#6366F1'
							strokeWidth={3}
							dot={{ fill: "#6366F1", strokeWidth: 2, r: 6 }}
							activeDot={{ r: 8, strokeWidth: 2 }}
						/>
					</LineChart>
				</ResponsiveContainer>
			</div>
		</motion.div>
	);
};
export default VaultsOverviewChart;