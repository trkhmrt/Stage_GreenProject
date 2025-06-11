import React from 'react';

const PaymentSuccess = () => {
    return (
        <div className="flex flex-col items-center justify-center p-5">
            <h1>ÖDEME BAŞARILI</h1>
            <svg viewBox="0 0 1024 1024" className="icon w-24 h-24"  version="1.1" xmlns="http://www.w3.org/2000/svg"
                 fill="#000000">
                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                <g id="SVGRepo_iconCarrier">
                    <path d="M512 512m-448 0a448 448 0 1 0 896 0 448 448 0 1 0-896 0Z" fill="#4CAF50"></path>
                    <path
                        d="M738.133333 311.466667L448 601.6l-119.466667-119.466667-59.733333 59.733334 179.2 179.2 349.866667-349.866667z"
                        fill="#CCFF90"></path>
                </g>
            </svg>
        </div>
    );
};

export default PaymentSuccess;