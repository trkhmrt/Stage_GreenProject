import React from 'react';
import Footer from "../components/Footer.jsx";
import Navbar from "../components/Navbar.jsx";
import {Outlet} from "react-router-dom";

const Layout = () => {
    return (
        <div className="flex flex-col min-h-screen">
            <Navbar />
            <main className="flex-grow">
                <Outlet/>
            </main>
            <Footer/>
        </div>
    );
};

export default Layout;