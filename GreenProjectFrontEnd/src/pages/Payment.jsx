import React, {useEffect, useState} from 'react';
import {useLocation, useNavigate} from "react-router-dom";
import {createPayment} from "../services/PaymentService.js";
import {IYZICO_RESPONSE_CODE} from "../constants/PaymentResponseCode.js";
import {taxes} from "../constants/Taxes.js";


const Payment = () => {

    const location = useLocation();
    const navigaste  = useNavigate();

    const [paymentAmount, setPaymentAmount] = useState({});

    const [total, setTotal] = useState(0);
    const [selectedAddressId, setSelectedAddressId] = useState(null);
    const addresses = [
        {
            id: 1,
            title: "Ev",
            details: "İstanbul, Beşiktaş, Barbaros Bulvarı No:10"
        },
        {
            id: 2,
            title: "İş",
            details: "İstanbul, Levent, Büyükdere Cad. No:50"
        },
    ];

    useEffect(() => {

        const incomingValues = {
            KDV: taxes.KDV,
            subTotal: parseInt(location.state.subTotal),
            Quantity: 0,
        };


        const totalWithoutQuantity = Object.entries(incomingValues)
            .filter(([key]) => key !== 'Quantity') // Quantity'yi toplamdan çıkar
            .reduce((acc, [_, value]) => acc + value, 0);

        // State'i güncelle
        setPaymentAmount({
            ...incomingValues,
            Total: totalWithoutQuantity,
        });

    }, []);

    console.log(location.state);
    const [formData, setFormData] = useState({
        fullName: '',
        email: '',
        phone: '',
        cardNumber: '',
        cardName: '',
        expiryDate: '',
        cvv: '',
        address: '',
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleCreatePayment = async () => {
        const paymentRequest = {
            customerId: 1, // ya da giriş yapan kullanıcıdan alınan ID
            email: formData.email,
            phone: formData.phone,
            address: formData.address,
            basketId: location.state.basketId,
            basketItems: location.state.basket,
            checkOutRequest: {
                fullName: formData.fullName,
                cardNumber: formData.cardNumber,
                cvv: formData.cvv,
                amount:paymentAmount.Total,
                cardOwnerName: formData.cardName,
                expiryDate: formData.expiryDate,
            }

        };
        const response = await createPayment(paymentRequest);
        if(response.data.responseCode == IYZICO_RESPONSE_CODE.Approved ){
            navigaste("/PaymentSuccess",{ replace: true })
        }else{
            console.log("ÖDEME HATASI")
        }

    }

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4">
                <div className="flex flex-col items-center mb-10">
                    <h2 className="text-3xl font-bold text-gray-900 mb-2">Ödeme</h2>
                    <div className="h-1 w-20 bg-green-500 rounded-full"></div>
                </div>


                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Sol Taraf - Ödeme Formu */}
                    <div className="lg:col-span-2 space-y-6">
                        {/* Kişisel Bilgiler */}
                        <div className="bg-white rounded-2xl shadow-sm p-8 hover:shadow-md transition-shadow">
                            <div className="flex items-center mb-6">
                                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-3">
                                    <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                    </svg>
                                </div>
                                <h3 className="text-xl font-semibold text-gray-900">Kişisel Bilgiler</h3>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-gray-700">Ad Soyad</label>
                                    <input
                                        type="text"
                                        name="fullName"
                                        value={formData.fullName}
                                        onChange={handleInputChange}
                                        className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                                        placeholder="John Doe"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-gray-700">E-posta</label>
                                    <input
                                        type="email"
                                        name="email"
                                        value={formData.email}
                                        onChange={handleInputChange}
                                        className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                                        placeholder="john@example.com"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-gray-700">Telefon</label>
                                    <input
                                        type="tel"
                                        name="phone"
                                        value={formData.phone}
                                        onChange={handleInputChange}
                                        className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                                        placeholder="+90 555 123 4567"
                                    />
                                </div>
                            </div>

                        </div>
                        {/*ADRES SEÇİM ALANI*/}
                        <div className="bg-white rounded-2xl shadow-sm p-8 hover:shadow-md transition-shadow mb-6">
                            <div className="flex items-center mb-6">
                                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-3">
                                    <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                                    </svg>
                                </div>
                                <h3 className="text-xl font-semibold text-gray-900">Adres Seçimi</h3>
                            </div>

                            <div className="space-y-4">
                                {addresses.map((address) => (
                                    <label
                                        key={address.id}
                                        className="flex items-start space-x-4 border rounded-xl p-4 cursor-pointer hover:shadow-md transition-shadow"
                                    >
                                        <input
                                            type="radio"
                                            name="address"
                                            value={address.details}
                                            checked={selectedAddressId === address.id}
                                            onChange={handleInputChange}
                                            className="mt-1 h-5 w-5 text-green-600"
                                        />
                                        <div>
                                            <p className="font-medium text-gray-800">{address.title}</p>
                                            <p className="text-sm text-gray-600">{address.details}</p>
                                        </div>
                                    </label>
                                ))}
                            </div>
                        </div>

                        {/* Ödeme Bilgileri */}
                        <div className="bg-white rounded-2xl shadow-sm p-8 hover:shadow-md transition-shadow">
                            <div className="flex items-center mb-6">
                                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-3">
                                    <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                                    </svg>
                                </div>
                                <h3 className="text-xl font-semibold text-gray-900">Ödeme Bilgileri</h3>
                            </div>

                            <div className="space-y-6">
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-gray-700">Kart Numarası</label>
                                    <input
                                        type="text"
                                        name="cardNumber"
                                        value={formData.cardNumber}
                                        onChange={handleInputChange}
                                        className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                                        placeholder="1234 5678 9012 3456"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-gray-700">Kart Üzerindeki İsim</label>
                                    <input
                                        type="text"
                                        name="cardName"
                                        value={formData.cardName}
                                        onChange={handleInputChange}
                                        className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                                        placeholder="JOHN DOE"
                                    />
                                </div>
                                <div className="grid grid-cols-2 gap-6">
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium text-gray-700">Son Kullanma Tarihi</label>
                                        <input
                                            type="text"
                                            name="expiryDate"
                                            value={formData.expiryDate}
                                            onChange={handleInputChange}
                                            className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                                            placeholder="MM/YY"
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium text-gray-700">CVV</label>
                                        <input
                                            type="text"
                                            name="cvv"
                                            value={formData.cvv}
                                            onChange={handleInputChange}
                                            className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                                            placeholder="123"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Sağ Taraf - Sipariş Özeti */}
                    <div className="lg:col-span-1">
                        <div className="bg-white rounded-2xl shadow-sm p-8 sticky top-4 hover:shadow-md transition-shadow">
                            <div className="flex items-center mb-6">
                                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-3">
                                    <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                                    </svg>
                                </div>
                                <h3 className="text-xl font-semibold text-gray-900">Sipariş Özeti</h3>
                            </div>

                            <div className="space-y-4">
                                <div className="flex justify-between items-center py-4 border-b border-gray-100">
                                    <span className="text-gray-600">Ara Toplam</span>
                                    <span className="text-gray-900 font-medium">{paymentAmount.subTotal} TL</span>
                                </div>
                                <div className="flex justify-between items-center py-4 border-b border-gray-100">
                                    <span className="text-gray-600">Kargo</span>
                                    <span className="text-green-500 font-medium">Ücretsiz</span>
                                </div>
                                <div className="flex justify-between items-center py-4 border-b border-gray-100">
                                    <span className="text-gray-600">KDV</span>
                                    <span className="text-gray-900 font-medium">{paymentAmount.KDV} TL</span>
                                </div>
                                <div className="flex justify-between items-center py-4">
                                    <span className="text-gray-900 font-semibold">Toplam</span>
                                    <span className="text-2xl font-bold text-gray-900">{paymentAmount.Total} TL</span>
                                </div>
                            </div>

                            <button className="w-full mt-8 bg-green-500 hover:bg-green-600 text-white py-4 rounded-xl font-medium focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transform transition-all hover:scale-[1.01]"
                            onClick={handleCreatePayment}
                            >
                                Ödemeyi Tamamla
                            </button>

                            <div className="mt-6 space-y-4">
                                <div className="flex items-center">
                                    <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                                    </svg>
                                    <span className="text-sm text-gray-600">256-bit SSL Koruması</span>
                                </div>
                                <div className="flex items-center">
                                    <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                    </svg>
                                    <span className="text-sm text-gray-600">Güvenli Ödeme</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Payment;