// Desc: FoldersPage component
//       This component is a placeholder for the FoldersPage component.
import Footer from "../Footer/Footer"
import Header from "../Header/Header"
import VaultsFolders from "../Vaults/VaultsFolders"
const FoldersPage = () => {

    const folders = [
        {
            id: 1,
            name: "Social Media",
            description: "This is a social media folder",
            vaultId: [1, 4, 5]
        },
        {
            id: 2,
            name: "Work",
            description: "This is a work folder",
            vaultId: [1, 2, 3]
        },
        {
            id: 3,
            name: "Personal",
            description: "This is a personal folder",
            vaultId: [1,3, 5, 7]
        },
        {
            id: 4,
            name: "Social Media2",
            description: "This is a social media folder",
            vaultId: 2
        },
        {
            id: 5,
            name: "Work2",
            description: "This is a work folder",
            vaultId: 1
        },
        {
            id: 6,
            name: "Personal2",
            description: "This is a personal folder",
            vaultId: 1
        },
        {
            id: 7,
            name: "Social Media3",
            description: "This is a social media folder",
            vaultId: 1
        },
        {
            id: 8,
            name: "Work3",
            description: "This is a work folder",
            vaultId: 1
        },
        {
            id: 9,
            name: "Personal3",
            description: "This is a personal folder",
            vaultId: 1
        }


    ];
  return (
    <>
    <Header />
    <div className="flex flex-col items-center justify-center py-16">
      <VaultsFolders folders= {folders}/>
    </div>
    <Footer />
    </>
  )
}

export default FoldersPage