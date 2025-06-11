import React, {useState} from 'react';

const Register = () => {
    const [username, setUsername] = useState('tarikhamarat');
    const [password, setPassword] = useState('güçlüŞifre123');
    const [errorMessage, setErrorMessage] = useState('');
    const handleRegister = () => {

    }
    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-300">
            <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-md">
                <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">Kayıt Ol</h2>

                {errorMessage && (
                    <div className="mb-4 text-red-600 font-medium text-center">{errorMessage}</div>
                )}
                <div>
                    <label className="block text-sm font-medium text-gray-600 mb-1">Username</label>
                    <input
                        placeholder="example@site.com"
                        className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-600 mb-1">Şifre</label>
                    <input
                        type="password"
                        placeholder="••••••••"
                        className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-600 mb-1">Şifre</label>
                    <input
                        type="password"
                        placeholder="••••••••"
                        className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-600 mb-1">Şifre</label>
                    <input
                        type="password"
                        placeholder="••••••••"
                        className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>

                <button

                    className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition duration-200"
                    onClick={handleRegister}
                >
                    Kayıt Ol
                </button>


                <p className="text-sm text-center text-gray-600 mt-6">
                    Hesabın yok mu? <a href="/register" className="text-blue-500 hover:underline">Kayıt Ol</a>
                </p>
            </div>
        </div>
    );
};

export default Register;