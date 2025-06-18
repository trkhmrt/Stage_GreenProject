import React, { useState, useEffect } from 'react';
import axios from 'axios';

// API fonksiyonu
export const recommendProductFromBasket = async (products) => {
    console.log("Gönderilen ürünler:", products);
    try {
        const response = await axios.post("http://localhost:5000/recommend", {
            "products": products,
            min_confidence: 0.01
        });
        console.log("Recommendation API Response:", response.data);
        return response.data.recommendations;
    } catch (error) {
        console.error("Error recommending products:", error);
        return [];
    }
};

const RecommendedProducts = ({ productNames }) => {
    const [recommendedProducts, setRecommendedProducts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [noRecommendations, setNoRecommendations] = useState(false);

    useEffect(() => {
        const fetchRecommendations = async () => {
            if (!productNames || productNames.length === 0) {
                setRecommendedProducts([]);
                setNoRecommendations(false);
                setError(null);
                return;
            }

            setLoading(true);
            setError(null);
            setNoRecommendations(false);

            try {
                const data = await recommendProductFromBasket(productNames);
                
                if (data && data.length > 0) {
                    const formattedProducts = data.map(item => ({
                        productId: item.product_id,
                        productName: item.product_name,
                        productDescription: item.product_description,
                        productPrice: item.product_price,
                        productQuantity: item.product_quantity || 1,
                        isNew: false,
                        hasDiscount: false,
                        discountPercentage: 0,
                        categoryName: item.category_name || "Genel",
                        subCategoryName: item.sub_category_name || "Genel",
                        // Apriori metrikleri
                        confidence: item.confidence,
                        lift: item.lift,
                        support: item.support,
                        antecedents: item.antecedents
                    }));
                    setRecommendedProducts(formattedProducts);
                    setNoRecommendations(false);
                } else {
                    setRecommendedProducts([]);
                    setNoRecommendations(true);
                }
            } catch (error) {
                console.error("Öneri alma hatası:", error);
                setError("Öneriler alınırken bir hata oluştu.");
                setRecommendedProducts([]);
            } finally {
                setLoading(false);
            }
        };

        fetchRecommendations();
    }, [productNames]);

    if (loading) {
        return (
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                <h3 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
                    🎯 Size Özel Öneriler
                </h3>
                <div className="flex items-center justify-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mr-3"></div>
                    <p className="text-gray-600">Öneriler yükleniyor...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                <h3 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
                    🎯 Size Özel Öneriler
                </h3>
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-700 flex items-center">
                        ❌ {error}
                    </p>
                </div>
            </div>
        );
    }

    if (noRecommendations) {
        return (
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                <h3 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
                    🎯 Size Özel Öneriler
                </h3>
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                    <p className="text-blue-800 mb-2 flex items-center">
                        📝 Sepetinizdeki ürünler için henüz öneri bulunamadı.
                    </p>
                    <p className="text-blue-700 mb-4 flex items-center">
                        💡 Daha fazla ürün ekleyerek öneriler alabilirsiniz.
                    </p>
                    <details className="text-sm">
                        <summary className="cursor-pointer text-blue-600 hover:text-blue-800 font-medium">
                            🔍 Teknik Detaylar
                        </summary>
                        <div className="mt-2 space-y-1 text-blue-700">
                            <p><strong>Gönderilen ürünler:</strong> {productNames.join(", ")}</p>
                            <p><strong>Sebep:</strong> Bu ürünler Apriori model'inde minimum support eşiğini geçmemiş.</p>
                        </div>
                    </details>
                </div>
            </div>
        );
    }

    if (recommendedProducts.length === 0) {
        return null;
    }

    return (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
                🎯 Size Özel Öneriler
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {recommendedProducts.map((product, index) => (
                    <div key={`${product.productId}-${index}`} className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-4 hover:shadow-lg transition-shadow duration-300">
                        <div className="space-y-3">
                            <h4 className="text-lg font-semibold text-gray-800 line-clamp-2">
                                {product.productName}
                            </h4>
                            <p className="text-gray-600 text-sm line-clamp-3">
                                {product.productDescription}
                            </p>
                            <p className="text-2xl font-bold text-blue-600">
                                ₺{product.productPrice.toFixed(2)}
                            </p>
                            
                            {/* Apriori Metrikleri */}
                            <div className="bg-white rounded-lg p-3 space-y-2">
                                <div className="flex justify-between items-center">
                                    <span className="text-xs font-medium text-gray-600">Güven:</span>
                                    <span className="text-sm font-bold text-green-600">
                                        {(product.confidence * 100).toFixed(1)}%
                                    </span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-xs font-medium text-gray-600">Lift:</span>
                                    <span className="text-sm font-bold text-purple-600">
                                        {product.lift.toFixed(2)}
                                    </span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-xs font-medium text-gray-600">Support:</span>
                                    <span className="text-sm font-bold text-orange-600">
                                        {(product.support * 100).toFixed(2)}%
                                    </span>
                                </div>
                            </div>
                            
                            <div className="bg-blue-100 rounded-lg p-2">
                                <small className="text-xs text-blue-800">
                                    📦 Sepetinizdeki: {product.antecedents.join(", ")}
                                </small>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default RecommendedProducts; 