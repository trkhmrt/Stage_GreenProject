import React, {useState, useEffect, useRef} from 'react';
import {addProductToBasket} from "../services/BasketService.js";
import {getAllProducts} from "../services/ProductService.js";
import {getAllCategories} from "../services/CategoryService.js";

const ProductLayout = () => {
    const [products, setProducts] = useState([]);
    const [filteredProducts, setFilteredProducts] = useState([]);
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('all');
    const [loading, setLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(1);
    const [expandedCategories, setExpandedCategories] = useState({});
    const [favorites, setFavorites] = useState(new Set());
    const [productsPerPage, setProductsPerPage] = useState(20);

    // Arama state'leri
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [isSearching, setIsSearching] = useState(false);
    const [showSearchResults, setShowSearchResults] = useState(false);

    // Basket işlemleri için state'ler
    const [isAddingToBasket, setIsAddingToBasket] = useState(false);
    const [notifications, setNotifications] = useState([]);
    const [addedToBasketProduct, setAddedToBasketProduct] = useState(null);

    // Kategori dropdown için ref
    const categoryRef = useRef(null);

    // Kategori dışına tıklama ile kapanma
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (categoryRef.current && !categoryRef.current.contains(event.target)) {
                setExpandedCategories({});
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const handleAddProductToBasket = async (productId) => {
        try {
            // Önce customerId kontrolü yap
            const customerId = localStorage.getItem("customerId");
            if (!customerId) {
                addNotification('Sepete ürün eklemek için giriş yapmanız gerekiyor.', 'error');
                return;
            }

            setIsAddingToBasket(true);

            const response = await addProductToBasket(productId);
            console.log('Ürün sepete eklendi:', response);

            // Ürün kartında bildirim göster
            setAddedToBasketProduct(productId);
            setTimeout(() => {
                setAddedToBasketProduct(null);
            }, 1500);

            // Başarı mesajı göster
            addNotification('Ürün sepete başarıyla eklendi!', 'success');

        } catch (error) {
            console.error('Sepete ekleme hatası:', error);

            // Hata mesajı göster
            let errorMessage = 'Ürün sepete eklenirken bir hata oluştu. Lütfen tekrar deneyin.';

            // Daha spesifik hata mesajları
            if (error.response?.status === 401) {
                errorMessage = 'Oturum süreniz dolmuş. Lütfen tekrar giriş yapın.';
            } else if (error.response?.status === 404) {
                errorMessage = 'Ürün bulunamadı.';
            } else if (error.response?.status === 500) {
                errorMessage = 'Sunucu hatası. Lütfen daha sonra tekrar deneyin.';
            }

            addNotification(errorMessage, 'error');
        } finally {
            setIsAddingToBasket(false);
        }
    }

    // Gelişmiş bildirim sistemi
    const addNotification = (message, type = 'info') => {
        const id = Date.now() + Math.random();
        const notification = {
            id,
            message,
            type,
            timestamp: Date.now()
        };

        setNotifications(prev => {
            const newNotifications = [...prev, notification];
            // Maksimum 3 bildirim göster
            if (newNotifications.length > 3) {
                return newNotifications.slice(-3);
            }
            return newNotifications;
        });

        // 4 saniye sonra bildirimi kaldır
        setTimeout(() => {
            removeNotification(id);
        }, 4000);
    };

    const removeNotification = (id) => {
        setNotifications(prev => prev.filter(n => n.id !== id));
    };

    // Arama fonksiyonu
    const handleSearch = (query) => {
        setSearchQuery(query);
        setIsSearching(true);

        if (query.trim() === '') {
            setSearchResults([]);
            setShowSearchResults(false);
            setIsSearching(false);
            return;
        }

        // Harf harf arama - ürün adında, açıklamasında ve kategorisinde ara
        const results = products.filter(product => {
            const searchLower = query.toLowerCase();
            const productName = product.productName?.toLowerCase() || '';
            const productDesc = product.productDescription?.toLowerCase() || '';
            const categoryName = product.categoryName?.toLowerCase() || '';

            return productName.includes(searchLower) ||
                productDesc.includes(searchLower) ||
                categoryName.includes(searchLower);
        });

        setSearchResults(results);
        setShowSearchResults(true);
        setIsSearching(false);
    };

    // Arama sonucu seçildiğinde
    const handleSearchResultSelect = (product) => {
        setSearchQuery(product.productName);
        setShowSearchResults(false);
        // Ürünü filtrele ve göster
        setFilteredProducts([product]);
        setSelectedCategory('search');
        setCurrentPage(1);
    };

    // Arama temizleme
    const clearSearch = () => {
        setSearchQuery('');
        setSearchResults([]);
        setShowSearchResults(false);
        setFilteredProducts(products);
        setSelectedCategory('all');
        setCurrentPage(1);
    };

    useEffect(() => {
        const updateProductsPerPage = () => {
            if (window.innerWidth < 640) { // sm
                setProductsPerPage(12);
            } else if (window.innerWidth < 1024) { // lg
                setProductsPerPage(20);
            } else { // xl
                setProductsPerPage(30);
            }
        };

        updateProductsPerPage();
        window.addEventListener('resize', updateProductsPerPage);

        getProducts()
        getCategories()
        setLoading(false);

        return () => window.removeEventListener('resize', updateProductsPerPage);
    }, []);

    const getProducts = async () => {
        const response = await getAllProducts()
        console.log(response)
        setProducts(response)
        setFilteredProducts(response) // Başlangıçta tüm ürünleri göster
    }

    const getCategories = async () => {
        const categories = await getAllCategories()
        console.log(categories.data)
        setCategories(categories.data)
    }

    const newFilteredProducts = (categoryId, subcategoryId, subcategoryName) => {
        console.log(categoryId, subcategoryId)
        console.log(products)
        const filteredProducts = products.filter(product => product.subCategoryId === subcategoryId)
        console.log(filteredProducts)
        setSelectedCategory(subcategoryName)
        setFilteredProducts(filteredProducts);
        setCurrentPage(1); // Filtreleme yapıldığında ilk sayfaya dön
    }

    const indexOfLastProduct = currentPage * productsPerPage;
    const indexOfFirstProduct = indexOfLastProduct - productsPerPage;
    const currentProducts = filteredProducts.slice(indexOfFirstProduct, indexOfLastProduct);
    const totalPages = Math.ceil(filteredProducts.length / productsPerPage);

    const handleCategorySelected = (categoryId) => {
        console.log(categoryId)
        const newSelectedCategory = categories.filter(category => category.categoryId === categoryId);
        console.log(newSelectedCategory);
        newSelectedCategory.map(c => {
            c.subcategories.map(b => {
                console.log(b.id)
                console.log(b.name)
            })
        })
    }

    // Gelişmiş kategori açma/kapama fonksiyonu
    const toggleCategory = (categoryId) => {
        setExpandedCategories(prev => {
            const newState = { ...prev };

            // Eğer bu kategori zaten açıksa, kapat
            if (newState[categoryId]) {
                delete newState[categoryId];
            } else {
                // Diğer tüm kategorileri kapat
                Object.keys(newState).forEach(key => {
                    delete newState[key];
                });
                // Bu kategoriyi aç
                newState[categoryId] = true;
            }

            return newState;
        });
    };

    const handlePageChange = (pageNumber) => {
        setCurrentPage(pageNumber);
    };

    const toggleFavorite = (productId) => {
        setFavorites(prev => {
            const newFavorites = new Set(prev);
            if (newFavorites.has(productId)) {
                newFavorites.delete(productId);
            } else {
                newFavorites.add(productId);
            }
            return newFavorites;
        });
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="w-8 h-8 border-2 border-gray-300 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-gray-600">Ürünler yükleniyor...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Soft Minimal Arama Alanı */}
            <div className="mb-6 px-4">
                <div className="max-w-2xl mx-auto">
                    <div className="relative">
                        <input
                            type="text"
                            value={searchQuery}
                            onChange={(e) => handleSearch(e.target.value)}
                            placeholder="Ürün ara..."
                            className="w-full px-4 py-3 pl-12 bg-white border border-gray-200 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-300 transition-all duration-200 text-gray-700 placeholder-gray-400"
                        />

                        {/* Arama İkonu */}
                        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                            <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                            </svg>
                        </div>

                        {/* Temizleme Butonu */}
                        {searchQuery && (
                            <button
                                onClick={clearSearch}
                                className="absolute inset-y-0 right-0 pr-4 flex items-center"
                                aria-label="Aramayı temizle"
                            >
                                <div className="w-5 h-5 rounded-full flex items-center justify-center transition-all duration-200 hover:bg-gray-100">
                                    <svg className="w-3 h-3 text-gray-400 hover:text-gray-600 transition-colors duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"/>
                                    </svg>
                                </div>
                            </button>
                        )}
                    </div>

                    {/* Arama Sonuçları */}
                    {showSearchResults && searchResults.length > 0 && (
                        <div className="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                            {searchResults.map((product) => (
                                <button
                                    key={product.productId}
                                    onClick={() => handleSearchResultSelect(product)}
                                    className="w-full px-4 py-3 text-left hover:bg-gray-50 transition-colors duration-150 border-b border-gray-100 last:border-b-0"
                                >
                                    <div className="font-medium text-gray-900">{product.productName}</div>
                                    <div className="text-sm text-gray-500">{product.productDescription}</div>
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* Kategori Filtreleme */}
            <div className="mb-6 px-4" ref={categoryRef}>
                <div className="max-w-6xl mx-auto">
                    <div className="flex flex-wrap gap-2">
                        <button
                            onClick={() => {
                                setFilteredProducts(products);
                                setSelectedCategory('all');
                                setCurrentPage(1);
                            }}
                            className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                                selectedCategory === 'all'
                                    ? 'bg-blue-100 text-blue-700 border border-blue-200'
                                    : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
                            }`}
                        >
                            Tümü
                        </button>

                        {categories.map((category) => (
                            <div key={category.categoryId} className="relative">
                                <button
                                    onClick={() => toggleCategory(category.categoryId)}
                                    className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 flex items-center gap-1 ${
                                        selectedCategory === category.categoryName
                                            ? 'bg-blue-100 text-blue-700 border border-blue-200'
                                            : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
                                    }`}
                                >
                                    {category.categoryName}
                                    <svg className={`w-4 h-4 transition-transform duration-200 ${
                                        expandedCategories[category.categoryId] ? 'rotate-180' : ''
                                    }`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"/>
                                    </svg>
                                </button>

                                {expandedCategories[category.categoryId] && (
                                    <div className="absolute top-full left-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-10 min-w-48">
                                        {category.subcategories.map((subcategory) => (
                                            <button
                                                key={subcategory.id}
                                                onClick={() => newFilteredProducts(category.categoryId, subcategory.id, subcategory.name)}
                                                className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 transition-colors duration-150 border-b border-gray-100 last:border-b-0"
                                            >
                                                {subcategory.name}
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Ürün Listesi */}
            <div className="px-4 pb-8">
                <div className="max-w-7xl mx-auto">
                    {currentProducts.length === 0 ? (
                        <div className="text-center py-12">
                            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
                                </svg>
                            </div>
                            <h3 className="text-lg font-medium text-gray-900 mb-2">Ürün bulunamadı</h3>
                            <p className="text-gray-500">Arama kriterlerinize uygun ürün bulunamadı.</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-6">
                            {currentProducts.map((product, index) => (
                                <ProductCard
                                    key={product.productId}
                                    product={product}
                                    isFavorite={favorites.has(product.productId)}
                                    onToggleFavorite={() => toggleFavorite(product.productId)}
                                    onAddToBasket={handleAddProductToBasket}
                                    isAddingToBasket={isAddingToBasket}
                                    isAddedToBasket={addedToBasketProduct === product.productId}
                                />
                            ))}
                        </div>
                    )}

                    {/* Sayfalama */}
                    {totalPages > 1 && (
                        <div className="flex justify-center mt-8">
                            <div className="flex items-center space-x-2">
                                <button
                                    onClick={() => handlePageChange(currentPage - 1)}
                                    disabled={currentPage === 1}
                                    className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                                >
                                    Önceki
                                </button>

                                {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                                    <button
                                        key={page}
                                        onClick={() => handlePageChange(page)}
                                        className={`px-3 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
                                            currentPage === page
                                                ? 'bg-blue-600 text-white'
                                                : 'text-gray-700 bg-white border border-gray-300 hover:bg-gray-50'
                                        }`}
                                    >
                                        {page}
                                    </button>
                                ))}

                                <button
                                    onClick={() => handlePageChange(currentPage + 1)}
                                    disabled={currentPage === totalPages}
                                    className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                                >
                                    Sonraki
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Gelişmiş Bildirim Sistemi */}
            <div className="fixed bottom-4 right-4 z-50 space-y-3">
                {notifications.map((notification, index) => (
                    <div
                        key={notification.id}
                        className={`max-w-sm p-4 rounded-lg shadow-lg border-l-4 transform transition-all duration-500 ease-out ${
                            notification.type === 'success'
                                ? 'bg-green-50 border-green-400 text-green-800'
                                : notification.type === 'error'
                                    ? 'bg-red-50 border-red-400 text-red-800'
                                    : 'bg-blue-50 border-blue-400 text-blue-800'
                        }`}
                        style={{
                            transform: `translateY(${index * 90}px)`,
                            opacity: 1,
                            animation: 'slideInRight 0.3s ease-out'
                        }}
                    >
                        <div className="flex items-start">
                            <div className="flex-shrink-0">
                                {notification.type === 'success' ? (
                                    <svg className="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                                    </svg>
                                ) : notification.type === 'error' ? (
                                    <svg className="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
                                    </svg>
                                ) : (
                                    <svg className="w-5 h-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"/>
                                    </svg>
                                )}
                            </div>
                            <div className="ml-3 flex-1">
                                <p className="text-sm font-medium">{notification.message}</p>
                            </div>
                            <div className="ml-3 flex-shrink-0">
                                <button
                                    onClick={() => removeNotification(notification.id)}
                                    className="inline-flex text-gray-400 hover:text-gray-600 transition-colors duration-200"
                                >
                                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd"/>
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* CSS Animasyonları */}
            <style jsx>{`
                @keyframes slideInRight {
                    from {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }

                @keyframes fadeInOut {
                    0% {
                        opacity: 0;
                        transform: scale(0.8);
                    }
                    20% {
                        opacity: 1;
                        transform: scale(1);
                    }
                    80% {
                        opacity: 1;
                        transform: scale(1);
                    }
                    100% {
                        opacity: 0;
                        transform: scale(0.8);
                    }
                }
            `}</style>
        </div>
    );
};

// Soft Minimal ProductCard Bileşeni
const ProductCard = ({product, isFavorite, onToggleFavorite, onAddToBasket, isAddingToBasket, isAddedToBasket}) => {
    return (
        <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-all duration-300 group relative">
            {/* Ürün Görseli */}
            <div className="aspect-square bg-gray-100 relative overflow-hidden">
                <div className="w-full h-full flex items-center justify-center">
                    <svg className="w-16 h-16 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd"/>
                    </svg>
                </div>

                {/* Favori Butonu */}
                <button
                    onClick={() => onToggleFavorite(product.productId)}
                    className="absolute top-3 right-3 p-2 bg-white/80 backdrop-blur-sm rounded-full shadow-sm hover:bg-white transition-all duration-200 group/fav"
                >
                    <svg
                        className={`w-4 h-4 transition-all duration-200 ${
                            isFavorite
                                ? 'text-red-500 fill-current'
                                : 'text-gray-400 group-hover/fav:text-red-400'
                        }`}
                        fill={isFavorite ? 'currentColor' : 'none'}
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                    </svg>
                </button>

                {/* Sepete Eklendi Bildirimi */}
                {isAddedToBasket && (
                    <div className="absolute inset-0 bg-green-500/90 backdrop-blur-sm flex items-center justify-center z-10">
                        <div className="text-center text-white">
                            <svg className="w-8 h-8 mx-auto mb-2" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                            </svg>
                            <p className="text-sm font-medium">Sepete Eklendi</p>
                        </div>
                    </div>
                )}
            </div>

            {/* Ürün Bilgileri */}
            <div className="p-4">
                <h3 className="font-medium text-gray-900 mb-2 line-clamp-2 group-hover:text-blue-600 transition-colors duration-200">
                    {product.productName}
                </h3>

                <p className="text-sm text-gray-500 mb-3 line-clamp-2">
                    {product.productDescription}
                </p>

                <div className="flex items-center justify-between">
                    <div className="text-lg font-semibold text-gray-900">
                        ₺{product.productPrice?.toLocaleString()}
                    </div>

                    {/* Sepet Butonu */}
                    <button
                        onClick={() => onAddToBasket(product.productId)}
                        disabled={isAddingToBasket}
                        className={`p-2 rounded-full transition-all duration-200 ${
                            isAddingToBasket
                                ? 'bg-gray-100 cursor-not-allowed'
                                : 'bg-blue-50 hover:bg-blue-100 text-blue-600 hover:text-blue-700'
                        }`}
                        aria-label="Sepete ekle"
                    >
                        {isAddingToBasket ? (
                            <svg className="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                            </svg>
                        ) : (
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m6-5v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m8 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4.01"/>
                            </svg>
                        )}
                    </button>
                </div>
            </div>

            {/* CSS Animasyonu */}
            {isAddedToBasket && (
                <style jsx>{`
                    div {
                        animation: fadeInOut 1.5s ease-in-out;
                    }
                `}</style>
            )}
        </div>
    );
};

export default ProductLayout;