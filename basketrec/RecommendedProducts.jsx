import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Axios'u import et

// BasketService.js (Örnek olarak, bu fonksiyonu ayrı bir dosyaya taşımanız önerilir)
export const recommendProductFromBasket = async (products) => {
    try {
        const response = await axios.post("http://localhost:5000/recommend", {
            "products": products, // products dizisini doğrudan gönderiyoruz
            min_confidence: 0.01
        });
        console.log("Recommendation API Response:", response.data);
        return response.data.recommendations; // Sadece recommendations dizisini döndür
    } catch (error) {
        console.error("Error recommending products:", error);
        // Hata durumunda boş bir dizi veya hata mesajı döndürebilirsiniz
        return [];
    }
};

const RecommendedProducts = ({ productNames = [] }) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [recommendedProducts, setRecommendedProducts] = useState([]); // Önerilen ürünleri tutacak state
    const [loading, setLoading] = useState(true); // Yükleme durumu
    const [error, setError] = useState(null); // Hata durumu

    // useEffect ile component mount edildiğinde API isteği at
    useEffect(() => {
        const fetchRecommendations = async () => {
            setLoading(true); // Yüklemeyi başlat
            setError(null); // Önceki hataları temizle
            try {
                // Eğer productNames props olarak geliyorsa onu kullan, yoksa boş dizi gönder
                if (productNames && productNames.length > 0) {
                    console.log("Sepetteki ürünlerden öneri alınıyor:", productNames);
                    const data = await recommendProductFromBasket(productNames);
                    // API'den gelen veriyi bizim ProductCard yapımıza uyduralım
                    const formattedProducts = data.map(item => ({
                        productId: item.product_id,
                        productName: item.product_name,
                        productDescription: item.product_description,
                        productPrice: item.product_price,
                        // API'den gelmeyen diğer alanlar için varsayılan değerler
                        productQuantity: 1, // Öneri olduğu için miktar önemli olmayabilir
                        isNew: false, // Öneri ürünlerinde 'yeni' durumu genelde olmaz
                        hasDiscount: false, // İndirim bilgisi API'den gelmiyorsa
                        discountPercentage: 0,
                        categoryName: item.category_name, // Yeni eklenen alanlar
                        subCategoryName: item.sub_category_name, // Yeni eklenen alanlar
                        // Confidence ve lift değerleri
                        confidence: item.confidence,
                        lift: item.lift,
                        support: item.support,
                        antecedents: item.antecedents
                    }));
                    setRecommendedProducts(formattedProducts);
                } else {
                    console.log("Sepette ürün bulunamadı, öneri gösterilmiyor");
                    setRecommendedProducts([]);
                }
            } catch (err) {
                console.error("Failed to fetch recommendations:", err);
                setError("Önerilen ürünler yüklenirken bir hata oluştu.");
            } finally {
                setLoading(false); // Yüklemeyi bitir
            }
        };

        fetchRecommendations();
    }, [productNames]); // productNames değiştiğinde yeniden çalıştır

    // Favori ürünler state'i aynı kalıyor
    const [favorites, setFavorites] = useState(new Set());

    const productsPerPage = 5; // Her sayfada 5 ürün göster
    // API'den gelen ürün sayısına göre totalPages hesaplanır
    const totalPages = recommendedProducts.length > 0 ? Math.ceil(recommendedProducts.length / productsPerPage) : 0;


    const nextSlide = () => {
        setCurrentIndex((prevIndex) =>
            prevIndex === totalPages - 1 ? 0 : prevIndex + 1
        );
    };

    const prevSlide = () => {
        setCurrentIndex((prevIndex) =>
            prevIndex === 0 ? totalPages - 1 : prevIndex - 1
        );
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

    const startIndex = currentIndex * productsPerPage;
    const visibleProducts = recommendedProducts.slice(startIndex, startIndex + productsPerPage);

    // Eğer sepette ürün yoksa component'i gösterme
    if (productNames.length === 0) {
        return null;
    }

    if (loading) {
        return (
            <div className="relative w-full px-4 sm:px-6 lg:px-8 py-8 flex justify-center items-center h-64">
                <p className="text-xl text-gray-700">Önerilen ürünler yükleniyor...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="relative w-full px-4 sm:px-6 lg:px-8 py-8 flex justify-center items-center h-64">
                <p className="text-xl text-red-600">Hata: {error}</p>
            </div>
        );
    }

    if (recommendedProducts.length === 0 && !loading) {
        return (
            <div className="relative w-full px-4 sm:px-6 lg:px-8 py-8 flex justify-center items-center h-64">
                <p className="text-xl text-gray-700">Bu ürünler için öneri bulunamadı.</p>
            </div>
        );
    }


    return (
        <div className="relative w-full px-4 sm:px-6 lg:px-8 py-8">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Sepetinizle İlgili Öneriler</h2>
                <div className="flex items-center space-x-4">
                    <span className="text-sm text-gray-600">
                        {currentIndex + 1} / {totalPages}
                    </span>
                    <div className="flex space-x-2">
                        <button
                            onClick={prevSlide}
                            className="p-2 rounded-full bg-white border border-gray-300 hover:bg-gray-50 transition-colors duration-200 shadow-sm"
                            aria-label="Önceki"
                        >
                            <svg className="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                            </svg>
                        </button>
                        <button
                            onClick={nextSlide}
                            className="p-2 rounded-full bg-white border border-gray-300 hover:bg-gray-50 transition-colors duration-200 shadow-sm"
                            aria-label="Sonraki"
                        >
                            <svg className="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>

            {/* Card'ları ortalamak için container - Tailwind ile scrollbar gizli */}
            <div className="flex justify-center">
                <div className="flex space-x-6 overflow-x-auto max-w-7xl scrollbar-none">
                    {visibleProducts.map((product) => (
                        <ProductCard
                            key={product.productId}
                            product={product}
                            isFavorite={favorites.has(product.productId)}
                            onToggleFavorite={() => toggleFavorite(product.productId)}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
};

// ProductCard bileşeni aynı kalıyor
const ProductCard = ({ product, isFavorite, onToggleFavorite }) => {
    const originalPrice = product.productPrice;
    // API'den gelen ürünlerde indirim bilgisi yoksa, doğrudan gelen fiyatı kullanırız
    const discountedPrice = product.hasDiscount
        ? originalPrice * (1 - product.discountPercentage / 100)
        : originalPrice;

    return (
        <div className="relative w-80 h-96 bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100 flex-shrink-0">
            {/* Yeni Ürün Etiketi - API'den gelmediği için şimdilik kaldırabiliriz veya varsayılan false kalır */}
            {/* {product.isNew && (
                <div className="absolute top-3 right-3 z-10">
                    <span className="bg-green-500 text-white text-xs font-semibold px-2 py-1 rounded-full shadow-sm">
                        YENİ
                    </span>
                </div>
            )} */}

            {/* Ürün Görseli - Sabit yükseklik */}
            <div className="relative h-48 bg-gradient-to-br from-gray-100 to-gray-200 overflow-hidden">
                <div className="w-full h-full bg-gradient-to-br from-gray-300 to-gray-400 flex items-center justify-center">
                    <div className="text-center">
                        <svg className="w-12 h-12 mx-auto text-gray-500 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        <span className="text-gray-500 text-sm">Ürün Görseli</span>
                    </div>
                </div>

                {/* İndirim Etiketi - API'den indirim bilgisi gelmediği için kaldırılabilir */}
                {/* {product.hasDiscount && (
                    <div className="absolute top-3 left-3">
                        <span className="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded shadow-sm">
                            %{product.discountPercentage} İNDİRİM
                        </span>
                    </div>
                )} */}
            </div>

            {/* Ürün Bilgileri - Sabit yükseklik */}
            <div className="p-4 h-48 flex flex-col">
                <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2 flex-shrink-0">
                    {product.productName}
                </h3>

                <p className="text-sm text-gray-600 mb-3 line-clamp-2 flex-1">
                    {product.productDescription}
                </p>

                {/* Confidence ve Lift bilgileri */}
                {product.confidence && product.lift && (
                    <div className="text-xs text-gray-500 mb-2">
                        <span className="mr-2">Confidence: {(product.confidence * 100).toFixed(1)}%</span>
                        <span>Lift: {product.lift.toFixed(2)}</span>
                    </div>
                )}

                {/* Fiyat ve İkonlar - Alt kısımda sabit */}
                <div className="flex items-center justify-between mt-auto">
                    <div className="flex items-center space-x-2">
                        {/* API'den gelen ürünlerde indirim yoksa sadece tek fiyat gösteririz */}
                        <span className="text-lg font-bold text-gray-900">
                            ₺{originalPrice.toFixed(2)}
                        </span>
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
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
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
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m6-5v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m8 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4" />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RecommendedProducts; 