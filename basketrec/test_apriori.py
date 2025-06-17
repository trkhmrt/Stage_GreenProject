from apriori_recommender import AprioriRecommender
import pandas as pd

def test_apriori_algorithm():
    """
    Test Apriori algorithm with basket data
    """
    print("🎯 Apriori Algoritması Test Ediliyor...")
    print("=" * 50)
    
    # Initialize recommender with custom parameters
    recommender = AprioriRecommender(
        min_support=0.02,      # 2% minimum support
        min_confidence=0.3,    # 30% minimum confidence
        min_lift=1.2          # 1.2 minimum lift
    )
    
    # Load basket data
    print("\n📊 Veri yükleniyor...")
    basket_data = recommender.load_basket_data()
    
    if basket_data is None:
        print("❌ Veri yüklenemedi!")
        return
    
    # Train the model
    print("\n🤖 Model eğitiliyor...")
    recommender.fit()
    
    # Get basket insights
    print("\n📈 Sepet İstatistikleri:")
    insights = recommender.get_basket_insights()
    if insights:
        print(f"   Toplam Sepet: {insights['total_baskets']}")
        print(f"   Toplam Ürün: {insights['total_products']}")
        print(f"   Toplam İşlem: {insights['total_transactions']}")
        print(f"   Sepet Başına Ortalama Ürün: {insights['avg_products_per_basket']:.2f}")
    
    # Get popular combinations
    print("\n🏆 En Popüler Ürün Kombinasyonları:")
    popular_combinations = recommender.get_popular_combinations(top_n=5)
    for i, combo in enumerate(popular_combinations, 1):
        print(f"   {i}. {', '.join(combo['products'])}")
        print(f"      Support: {combo['support']:.1%} | Sıklık: {combo['frequency']} sepet")
        print(f"      Açıklama: {combo['explanation']}")
        print()
    
    # Test recommendations for different products
    test_products = [
        ["PlayStation 5"],
        ["Xbox Series X"],
        ["Marvel's Spider-Man: Miles Morales"],
        ["Halo 4"],
        ["PlayStation 5", "Marvel's Spider-Man: Miles Morales"],
        ["Xbox 360", "Halo 4"]
    ]
    
    print("🎯 Ürün Önerileri Test Ediliyor:")
    print("=" * 50)
    
    for products in test_products:
        print(f"\n🔍 '{', '.join(products)}' için öneriler:")
        recommendations = recommender.get_recommendations(products, top_n=5)
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec['product']}")
                print(f"      Confidence: {rec['confidence']:.1%} | Lift: {rec['lift']:.2f}")
                print(f"      Açıklama: {rec['explanation']}")
                print(f"      Kural: {', '.join(rec['antecedents'])} → {', '.join(rec['consequents'])}")
                print()
        else:
            print("   ❌ Öneri bulunamadı")
    
    # Show some association rules
    print("🔗 Örnek Association Rules:")
    print("=" * 50)
    
    if recommender.rules is not None and len(recommender.rules) > 0:
        top_rules = recommender.rules.head(10)
        for i, (_, rule) in enumerate(top_rules.iterrows(), 1):
            antecedents = list(rule['antecedents'])
            consequents = list(rule['consequents'])
            print(f"   {i}. {', '.join(antecedents)} → {', '.join(consequents)}")
            print(f"      Confidence: {rule['confidence']:.1%} | Support: {rule['support']:.1%} | Lift: {rule['lift']:.2f}")
            print()
    
    print("✅ Test tamamlandı!")

if __name__ == "__main__":
    test_apriori_algorithm() 