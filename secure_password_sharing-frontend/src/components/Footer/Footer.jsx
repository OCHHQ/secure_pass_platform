import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin } from 'react-icons/fa';

const Footer = () => {
    return (
        <footer className="bg-[#28243D] text-white py-8  bottom-0 w-full">
            <div className="container mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div className="footer-section">
                        <h4 className="text-lg font-semibold mb-2">About Us</h4>
                        <p>We are a company dedicated to secure password sharing.</p>
                    </div>
                    <div className="footer-section">
                        <h4 className="text-lg font-semibold mb-2">Contact Us</h4>
                        <p>Email: support@securepasswordsharing.com</p>
                        <p>Phone: +212 63723589</p>
                    </div>
                    <div className="footer-section">
                        <h4 className="text-lg font-semibold mb-2">More</h4>
                        <p>Privacy Policy</p>
                        <p>Terms of Service</p>
                    </div>
                </div>
                <div className="flex justify-center mt-8 space-x-4">
                    <FaFacebook className="text-2xl" />
                    <FaTwitter className="text-2xl" />
                    <FaInstagram className="text-2xl" />
                    <FaLinkedin className="text-2xl" />
                </div>
            </div>
            <div className="text-center mt-8 border-t-2 border-white">
                <p className='p-2'>&copy; 2024-2025 Secure Password Sharing. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default Footer;