import { Link } from "react-router-dom";
import { useState } from "react";
import { useUser } from "../Context/UserContext";
import { FaUserCircle } from "react-icons/fa";

function Header() {
  const {user} = useUser();
  const {isLoggedIn} = user;
  const [isOpen, setIsOpen] = useState(false);
  const { logout } = useUser();
  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      <nav
        aria-label="Global"
        className="flex justify-between items-center  w-full md:px-10 px-4 py-2 border-b-4 rounded-lg border-[#7A4FE7] fixed shadow-lg backdrop-blur-3xl bg-[#F9F6F3] z-30"
      >
        <div className="font-bold text-lg text-[#28243D]">
        <Link
            to="/dashboard"
            className="hover:text-white hover:bg-[#7A4FE7] p-2 hover:rounded-lg active:scale-[0.98]"
          >
            Pass-Share
          </Link>
        </div>
        {!isLoggedIn && ( <>
        <div className="hidden lg:flex space-x-8 font-bold text-[#28243D]">
          <a
            href="#Solutions"
            className="hover:text-white hover:bg-[#7A4FE7] p-2 hover:rounded-lg active:scale-[0.98]"
          >
            Solutions
          </a>
          <a
            href="#Features"
            className="hover:text-white hover:bg-[#7A4FE7] p-2 hover:rounded-lg active:scale-[0.98]"
          >
            Features
          </a>
          <a
            href="#Contact"
            className="hover:text-white hover:bg-[#7A4FE7] p-2 hover:rounded-lg active:scale-[0.98]"
          >
            Contact
          </a>
        </div>
        <div className="flex flex-row space-x-4">
          <div
            className={` md:${
              isOpen && "hidden"
            } hidden md:block lg:block border-2 font-medium border-[#7A4FE7] rounded-3xl px-4 py-1 self-center bg-[#7A4FE7] text-white hover:bg-white hover:text-[#7A4FE7] active:scale-[0.98]`}
          >
            <button className="">
              <Link to="/login">Login </Link>
              <Link to="/Signup">/ Sign Up</Link>
            </button>
          </div>
          <div className="lg:hidden self-center">
            {isOpen ? (<button
              onClick={handleToggle}
              className="border-2 font-medium border-[#7A4FE7] rounded-lg p-1 self-center bg-[#7A4FE7] text-white hover:bg-white hover:text-[#7A4FE7] active:scale-[0.98]"
            >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6 "
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>) : (<button
              onClick={handleToggle}
              className="border-2 font-medium border-[#7A4FE7] rounded-lg p-1 self-center bg-[#7A4FE7] text-white hover:bg-white hover:text-[#7A4FE7] active:scale-[0.98]"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6 "
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16m-7 6h7"
                />
              </svg>
            </button>)}
            
          </div>
        </div>
        </>
        )}
        {isLoggedIn && ( <>
        <div className="hidden lg:flex space-x-8 font-semibold text-[#28243D] ">
          <Link
            to="/Vaults"
            className="hover:text-white hover:bg-[#7A4FE7] p-2 hover:rounded-lg active:scale-[0.98]"
          >
            Vaults
          </Link>
          <Link
            to="/Folders"
            className="hover:text-white hover:bg-[#7A4FE7] p-2 hover:rounded-lg active:scale-[0.98]"
          >
            Folders
          </Link>
          <Link
            to="/Share"
            className="hover:text-white hover:bg-[#7A4FE7] p-2 hover:rounded-lg active:scale-[0.98]"
          >
            Share password
          </Link>
        </div>
        <div className="flex flex-row space-x-4">
        <div className={` md:${
              isOpen && "hidden"
            } hidden md:block `}>
                <Link to="/profile">
                    <FaUserCircle className="w-9 h-9 text-[#7A4FE7]" />
                </Link>
            </div>
          <div
            className={` md:${
              isOpen && "hidden"
            } hidden md:block border-2 font-medium border-[#7A4FE7] rounded-3xl px-4 py-1 self-center bg-[#7A4FE7] text-white hover:bg-white hover:text-[#7A4FE7] active:scale-[0.98]`}
          >
            <button>
              <Link to="/" onClick={logout} >logout</Link>
            </button>
          </div>
          <div className="lg:hidden self-center">
          {isOpen ? (<button
              onClick={handleToggle}
              className="border-2 font-medium border-[#7A4FE7] rounded-lg p-1 self-center bg-[#7A4FE7] text-white hover:bg-white hover:text-[#7A4FE7] active:scale-[0.98]"
            >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6 "
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>) : (<button
              onClick={handleToggle}
              className="border-2 font-medium border-[#7A4FE7] rounded-lg p-1 self-center bg-[#7A4FE7] text-white hover:bg-white hover:text-[#7A4FE7] active:scale-[0.98]"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6 "
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16m-7 6h7"
                />
              </svg>
            </button>)}
          </div>
        </div>
        </>
        )}
      </nav>
      {isOpen && isLoggedIn && (
        <div className="lg:hidden fixed top-0 right-0 mx-auto my-auto backdrop-blur-3xl flex flex-col   border-b-4 rounded-lg border-[#7A4FE7] shadow-lg p-8 z-20">
          <div
            onClick={handleToggle}
            className="flex flex-col items-center gap-8 font-semibold text-[#28243D] text-center mt-8"
          >
            <div className="flex items-center space-x-4">
                <Link to="/profile">
                    <FaUserCircle className="w-8 h-8 text-[#7A4FE7]" />
                </Link>
            </div>
            <Link
              to="/Vaults"
              className=" hover:text-white hover:bg-[#7A4FE7] p-2 hover:rounded-lg active:scale-[0.98]"
            >
              Vaults
            </Link>
            <Link
              to="/Folders"
              className=" hover:text-white hover:bg-[#7A4FE7] p-2 hover:rounded-lg active:scale-[0.98]"
            >
              Folders
            </Link>
            <Link
              to="/Share"
              className=" hover:text-white hover:bg-[#7A4FE7] p-2 hover:rounded-lg active:scale-[0.98]"
            >
              share password
            </Link>
            <div className="border-2 font-medium border-[#7A4FE7] rounded-3xl px-4 py-1 self-center bg-[#7A4FE7] text-white hover:bg-white hover:text-[#7A4FE7] active:scale-[0.98] ">
              <button className="">
                <Link to="/" onClick={logout }>logout </Link>
              </button>
            </div>
          </div>
        </div>
      )}
      {isOpen && !isLoggedIn && (
        <div className="lg:hidden fixed w-full top-0 right-0 mx-auto my-auto backdrop-blur-3xl flex flex-col   border-b-4 rounded-lg border-[#7A4FE7] shadow-lg p-8 z-20">
          <div onClick={handleToggle} className="flex flex-col items-center gap-8 font-semibold text-[#28243D] text-center mt-8">
          <a
            href="#Solutions"
            className=" hover:text-white hover:bg-[#7A4FE7] p-2 hover:rounded-lg active:scale-[0.98]"
          >
            Solutions 
          </a>
          <a
            href="#Manager"
            className=" hover:text-white hover:bg-[#7A4FE7] p-2 hover:rounded-lg active:scale-[0.98]"
          >
            Features
          </a>
          <a
            href="#Contact"
            className=" hover:text-white hover:bg-[#7A4FE7] p-2 hover:rounded-lg active:scale-[0.98]"
          >
            Contact
          </a>
          <div className="border-2 font-medium border-[#7A4FE7] rounded-3xl px-4 py-1 self-center bg-[#7A4FE7] text-white hover:bg-white hover:text-[#7A4FE7] active:scale-[0.98] ">
            <button className="">
              <Link to="/login">Login </Link>
              <Link to="/Signup" className="">/ Sign Up</Link>
            </button>
          </div>
          </div>
        </div>
      )}
    </>
  );
}

export default Header;
