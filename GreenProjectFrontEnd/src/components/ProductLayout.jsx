import React, {useState, useEffect} from 'react';
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
    const handleAddProductToBasket = async (productId) => {
        const response = await addProductToBasket(productId);
    }


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

    // Kategori açma/kapama fonksiyonu
    const toggleCategory = (categoryId) => {
        setExpandedCategories(prev => ({
            ...prev,
            [categoryId]: !prev[categoryId]
        }));
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

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex flex-col md:flex-row gap-8">
                {/* Categories Sidebar */}
                <div className="w-full md:w-1/4">
                    <div
                        className="bg-white rounded-2xl shadow-lg p-6 sticky top-4 max-h-[calc(100vh-2rem)] overflow-y-auto">
                        <div className="flex items-center mb-6">
                            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-3">
                                <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor"
                                     viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                                          d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
                                </svg>
                            </div>
                            <h2 className="text-xl font-semibold text-gray-900">Kategoriler</h2>
                        </div>

                        <div className="space-y-2">
                            {/* Tüm Kategoriler Butonu */}
                            <button
                                onClick={() => {
                                    setFilteredProducts(products);
                                    setSelectedCategory('all');
                                    setCurrentPage(1);
                                }}
                                className={`w-full text-left px-4 py-3 rounded-xl transition-all duration-200 flex items-center ${
                                    selectedCategory === 'all'
                                        ? 'bg-green-100 text-green-700 border-2 border-green-200 shadow-sm'
                                        : 'hover:bg-gray-50 text-gray-700 hover:text-green-600'
                                }`}
                            >
                                <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                                          d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                                </svg>
                                Tüm Kategoriler
                            </button>

                            {/* Kategoriler */}
                            {categories.map((category, index) => (
                                <div key={index} className="space-y-1">
                                    <button
                                        onClick={() => toggleCategory(category.categoryId)}
                                        className={`w-full flex justify-between items-center px-4 py-3 rounded-xl transition-all duration-200 ${
                                            selectedCategory === category.categoryName
                                                ? 'bg-green-100 text-green-700 border-2 border-green-200 shadow-sm'
                                                : 'hover:bg-gray-50 text-gray-700 hover:text-green-600'
                                        }`}
                                    >
                                        <div className="flex items-center">
                                            <div className={`w-2 h-2 rounded-full mr-3 transition-colors duration-200 ${
                                                selectedCategory === category.categoryName
                                                    ? 'bg-green-500'
                                                    : 'bg-gray-300'
                                            }`}></div>
                                            <span className="font-medium">{category.categoryName}</span>
                                        </div>
                                        <svg
                                            className={`w-5 h-5 transition-transform duration-300 ${
                                                expandedCategories[category.categoryId] ? 'transform rotate-180' : ''
                                            }`}
                                            fill="none"
                                            stroke="currentColor"
                                            viewBox="0 0 24 24"
                                        >
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                                                  d="M19 9l-7 7-7-7"/>
                                        </svg>
                                    </button>

                                    {/* Alt Kategoriler - Açılıp Kapanan */}
                                    {expandedCategories[category.categoryId] && (
                                        <div className="ml-6 space-y-1 overflow-hidden">
                                            {category.subcategories.map((subcategory) => (
                                                <button
                                                    key={subcategory.id}
                                                    onClick={() => newFilteredProducts(category.categoryId, subcategory.id, subcategory.name)}
                                                    className={`w-full text-left px-4 py-2 rounded-lg transition-all duration-200 flex items-center ${
                                                        selectedCategory === subcategory.name
                                                            ? 'bg-green-50 text-green-700 border border-green-200 shadow-sm'
                                                            : 'hover:bg-gray-50 text-gray-600 hover:text-green-600'
                                                    }`}
                                                >
                                                    <div
                                                        className={`w-1.5 h-1.5 rounded-full mr-3 transition-colors duration-200 ${
                                                            selectedCategory === subcategory.name
                                                                ? 'bg-green-400'
                                                                : 'bg-gray-300'
                                                        }`}></div>
                                                    <span className="text-sm font-medium">{subcategory.name}</span>
                                                </button>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Products Grid */}
                <div className="w-full md:w-3/4">
                    <div className="bg-white rounded-2xl shadow-lg p-6 h-[calc(100vh-4rem)] flex flex-col">
                        {loading ? (
                            <div className="flex justify-center items-center h-64">
                                <div
                                    className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-500"></div>
                            </div>
                        ) : (
                            <>
                                {/* Header - Sabit */}
                                <div className="mb-6 flex-shrink-0">
                                    <h2 className="text-2xl font-bold text-gray-900 mb-2">
                                        {selectedCategory === 'all'
                                            ? 'Tüm Ürünler'
                                            : `${selectedCategory} Kategorisi`}
                                    </h2>
                                    <div className="flex items-center text-gray-600">
                                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor"
                                             viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                                                  d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                                        </svg>
                                        <span>{filteredProducts.length} ürün bulundu</span>
                                    </div>
                                </div>

                                {/* Products Grid - Scrollable */}
                                <div className="flex-1 overflow-y-auto pr-2">
                                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 pb-4">
                                        {currentProducts.map((product, index) => (
                                            <ProductCard
                                                key={product.productId}
                                                product={product}
                                                isFavorite={favorites.has(product.productId)}
                                                onToggleFavorite={() => toggleFavorite(product.productId)}
                                            />
                                        ))}
                                    </div>
                                </div>

                                {/* Pagination - Sabit Alt */}
                                {totalPages > 1 && (
                                    <div className="mt-6 pt-4 border-t border-gray-200 flex-shrink-0">
                                        <nav className="flex flex-wrap justify-center items-center gap-2 px-2">
                                            <button
                                                onClick={() => handlePageChange(currentPage - 1)}
                                                disabled={currentPage === 1}
                                                className="px-3 py-2 text-sm rounded-xl bg-gray-100 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 whitespace-nowrap"
                                            >
                                                <span className="hidden sm:inline">Önceki</span>
                                                <span className="sm:hidden">←</span>
                                            </button>

                                            {/* Sayfa Numaraları - Responsive */}
                                            <div className="flex flex-wrap justify-center gap-1">
                                                {Array.from({length: totalPages}, (_, i) => i + 1).map((page) => {
                                                    // Mobilde sadece mevcut sayfa ve yanındakileri göster
                                                    const isVisible =
                                                        page === 1 ||
                                                        page === totalPages ||
                                                        Math.abs(page - currentPage) <= 1;

                                                    if (isVisible) {
                                                        return (
                                                            <button
                                                                key={page}
                                                                onClick={() => handlePageChange(page)}
                                                                className={`px-3 py-2 text-sm rounded-xl transition-all duration-200 ${
                                                                    currentPage === page
                                                                        ? 'bg-green-600 text-white shadow-md'
                                                                        : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
                                                                }`}
                                                            >
                                                                {page}
                                                            </button>
                                                        );
                                                    } else if (page === 2 || page === totalPages - 1) {
                                                        return <span key={page} className="px-2 py-2 text-gray-400">...</span>;
                                                    }
                                                    return null;
                                                })}
                                            </div>

                                            <button
                                                onClick={() => handlePageChange(currentPage + 1)}
                                                disabled={currentPage === totalPages}
                                                className="px-3 py-2 text-sm rounded-xl bg-gray-100 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 whitespace-nowrap"
                                            >
                                                <span className="hidden sm:inline">Sonraki</span>
                                                <span className="sm:hidden">→</span>
                                            </button>
                                        </nav>
                                    </div>
                                )}
                            </>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

const ProductCard = ({product, isFavorite, onToggleFavorite}) => {
    const originalPrice = product.productPrice;
    const discountedPrice = product.hasDiscount
        ? originalPrice * (1 - product.discountPercentage / 100)
        : originalPrice;

    return (
        <div className="relative w-full bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100">
            {/* Yeni Ürün Etiketi - Card'ın sağ üst köşesinde */}
            {product.isNew && (
                <div className="absolute top-3 right-3 z-10">
                    <span className="bg-green-500 text-white text-xs font-semibold px-2 py-1 rounded-full shadow-sm">
                        YENİ
                    </span>
                </div>
            )}

            {/* Ürün Görseli - Sabit yükseklik */}
            <div className="relative h-48 bg-gradient-to-br from-gray-100 to-gray-200 overflow-hidden">
                <div className="w-full h-full bg-gradient-to-br from-gray-300 to-gray-400 flex items-center justify-center">
                    <div className="text-center">
                        <svg className="w-12 h-12 mx-auto text-gray-500 mb-2" fill="none" stroke="currentColor"
                             viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                        </svg>
                        <span className="text-gray-500 text-sm">Ürün Görseli</span>
                    </div>
                </div>

                {/* İndirim Etiketi */}
                {product.hasDiscount && (
                    <div className="absolute top-3 left-3">
                        <span className="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded shadow-sm">
                            %{product.discountPercentage} İNDİRİM
                        </span>
                    </div>
                )}
            </div>

            {/* Ürün Bilgileri - Sabit yükseklik */}
            <div className="p-4 h-48 flex flex-col">
                <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2 flex-shrink-0">
                    {product.productName}
                </h3>

                <p className="text-sm text-gray-600 mb-3 line-clamp-2 flex-1">
                    {product.productDescription}
                </p>

                {/* Fiyat ve İkonlar - Alt kısımda sabit */}
                <div className="flex items-center justify-between mt-auto">
                    <div className="flex items-center space-x-2">
                        {product.hasDiscount ? (
                            <>
                                <span className="text-lg font-bold text-red-600">
                                    ₺{discountedPrice.toFixed(2)}
                                </span>
                                <span className="text-sm text-gray-500 line-through">
                                    ₺{originalPrice.toFixed(2)}
                                </span>
                            </>
                        ) : (
                            <span className="text-lg font-bold text-gray-900">
                                ₺{originalPrice.toFixed(2)}
                            </span>
                        )}
                    </div>

                    {/* SVG İkonlar - Fiyatın yanında */}
                    <div className="flex items-center space-x-2">
                        {/* Kalp İkonu */}
                        <button
                            onClick={onToggleFavorite}
                            className="p-1 hover:bg-gray-100 rounded-full transition-colors duration-200"
                            aria-label="Favorilere ekle"
                        >
                            <svg
                                className={`w-5 h-5 transition-colors duration-200 ${
                                    isFavorite ? 'text-red-500 fill-current' : 'text-gray-400 hover:text-red-500'
                                }`}
                                fill={isFavorite ? 'currentColor' : 'none'}
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                                      d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                            </svg>
                        </button>

                        {/* Sepet İkonu */}
                        <button
                            className="p-1 hover:bg-gray-100 rounded-full transition-colors duration-200"
                            aria-label="Sepete ekle"
                        >
                            <svg
                                className="w-5 h-5 text-gray-600 hover:text-blue-600 transition-colors duration-200"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                                      d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m6-5v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m8 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProductLayout;