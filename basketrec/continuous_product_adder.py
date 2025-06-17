import mysql.connector
import pandas as pd
import random
from apriori_recommender import AprioriRecommender
import time

class ContinuousProductAdder:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': 3309,
            'user': 'root',
            'password': 'root',
            'database': 'basketservicedb'
        }
        
        self.product_db_config = {
            'host': 'localhost',
            'port': 3301,
            'user': 'root',
            'password': 'root',
            'database': 'productservicedb'
        }
        
        self.recommender = AprioriRecommender(
            min_support=0.02,
            min_confidence=0.3,
            min_lift=1.2
        )
        
        self.initial_confidence_values = {}
        self.current_confidence_values = {}
        
    def connect_to_db(self, config):
        """Connect to database"""
        try:
            connection = mysql.connector.connect(**config)
            return connection
        except mysql.connector.Error as err:
            print(f"❌ Veritabanı bağlantı hatası: {err}")
            return None
    
    def get_products_by_category(self, category_id):
        """Get products by category"""
        connection = self.connect_to_db(self.product_db_config)
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT product_id, product_name, product_model, product_model_year, product_sub_category_id, product_price
                FROM products 
                WHERE product_sub_category_id = %s
                ORDER BY product_name
            """
            cursor.execute(query, (category_id,))
            products = cursor.fetchall()
            return products
        except mysql.connector.Error as err:
            print(f"❌ Ürün getirme hatası: {err}")
            return []
        finally:
            connection.close()
    
    def get_existing_baskets(self):
        """Get existing baskets"""
        connection = self.connect_to_db(self.db_config)
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT basket_id, customer_id FROM baskets WHERE basket_status_id = 4"
            cursor.execute(query)
            baskets = cursor.fetchall()
            return baskets
        except mysql.connector.Error as err:
            print(f"❌ Sepet getirme hatası: {err}")
            return []
        finally:
            connection.close()
    
    def add_products_to_baskets(self, products, target_products, num_baskets=10):
        """Add related products to existing baskets"""
        connection = self.connect_to_db(self.db_config)
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            # Get existing baskets
            baskets = self.get_existing_baskets()
            if not baskets:
                print("❌ Mevcut sepet bulunamadı!")
                return False
            
            # Select random baskets
            selected_baskets = random.sample(baskets, min(num_baskets, len(baskets)))
            
            added_count = 0
            
            for basket in selected_baskets:
                # Add 2-5 related products to each basket (increased from 1-3)
                num_products = random.randint(2, 5)
                selected_products = random.sample(products, min(num_products, len(products)))
                
                for product in selected_products:
                    # Check if product already exists in this basket
                    check_query = """
                        SELECT basket_product_unit_id FROM basket_product_units 
                        WHERE basket_id = %s AND product_id = %s
                    """
                    cursor.execute(check_query, (basket['basket_id'], product['product_id']))
                    
                    if not cursor.fetchone():
                        # Add product to basket
                        insert_query = """
                            INSERT INTO basket_product_units 
                            (basket_id, product_id, product_name, product_quantity, product_total_price)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                        
                        quantity = random.randint(1, 3)  # Increased from 1-2
                        total_price = product['product_price'] * quantity
                        
                        cursor.execute(insert_query, (
                            basket['basket_id'],
                            product['product_id'],
                            product['product_name'],
                            quantity,
                            total_price
                        ))
                        added_count += 1
            
            connection.commit()
            print(f"✅ {added_count} adet ürün sepete eklendi")
            return True
            
        except mysql.connector.Error as err:
            print(f"❌ Ürün ekleme hatası: {err}")
            connection.rollback()
            return False
        finally:
            connection.close()
    
    def test_confidence_values(self):
        """Test current confidence values"""
        print("🔄 Confidence değerleri test ediliyor...")
        
        # Load and train model
        self.recommender.load_basket_data()
        self.recommender.fit()
        
        if self.recommender.rules is None or len(self.recommender.rules) == 0:
            print("❌ İlişki kuralı bulunamadı!")
            return {}
        
        # Get top confidence values
        top_rules = self.recommender.rules.sort_values('confidence', ascending=False).head(20)
        
        confidence_values = {}
        for _, rule in top_rules.iterrows():
            antecedents = ', '.join(list(rule['antecedents']))
            consequents = ', '.join(list(rule['consequents']))
            rule_key = f"{antecedents} → {consequents}"
            confidence_values[rule_key] = rule['confidence']
        
        return confidence_values
    
    def compare_confidence_values(self):
        """Compare current vs initial confidence values"""
        if not self.initial_confidence_values:
            print("❌ İlk confidence değerleri henüz alınmamış!")
            return False
        
        improved_count = 0
        total_comparisons = 0
        
        print("\n📊 Confidence Değerleri Karşılaştırması:")
        print("=" * 60)
        
        for rule_key, current_conf in self.current_confidence_values.items():
            if rule_key in self.initial_confidence_values:
                initial_conf = self.initial_confidence_values[rule_key]
                improvement = current_conf - initial_conf
                total_comparisons += 1
                
                if improvement > 0:
                    improved_count += 1
                    print(f"✅ {rule_key}")
                    print(f"   İlk: {initial_conf:.3f} → Şimdi: {current_conf:.3f} (+{improvement:.3f})")
                elif improvement < 0:
                    print(f"❌ {rule_key}")
                    print(f"   İlk: {initial_conf:.3f} → Şimdi: {current_conf:.3f} ({improvement:.3f})")
                else:
                    print(f"➖ {rule_key}")
                    print(f"   İlk: {initial_conf:.3f} → Şimdi: {current_conf:.3f} (değişim yok)")
                print()
        
        improvement_rate = (improved_count / total_comparisons * 100) if total_comparisons > 0 else 0
        print(f"📈 İyileşme Oranı: {improvement_rate:.1f}% ({improved_count}/{total_comparisons})")
        
        return improvement_rate > 50  # %50'den fazla iyileşme varsa True
    
    def get_related_products(self):
        """Get related products by category with more diverse combinations"""
        related_products = []
        
        # Phone + Case combinations (same brand/model families)
        phones = self.get_products_by_category(1)  # Phones
        cases = self.get_products_by_category(32)  # Cases
        
        # Console + Game combinations (same platform families)
        consoles = self.get_products_by_category(2)  # Consoles
        games = self.get_products_by_category(3)     # Games
        
        # Add phone-case pairs (same brand/model compatibility)
        for phone in phones[:8]:  # First 8 phones
            for case in cases[:5]:  # First 5 cases
                related_products.extend([phone, case])
        
        # Add console-game pairs (platform-specific games)
        for console in consoles[:5]:  # First 5 consoles
            for game in games[:8]:    # First 8 games
                related_products.extend([console, game])
        
        # Add same brand/model family combinations
        # iPhone family combinations
        iphone_phones = [p for p in phones if 'iPhone' in p['product_name']]
        iphone_cases = [c for c in cases if 'iPhone' in c['product_name']]
        
        for phone in iphone_phones[:3]:
            for case in iphone_cases[:3]:
                related_products.extend([phone, case])
        
        # Samsung family combinations
        samsung_phones = [p for p in phones if 'Samsung' in p['product_name']]
        samsung_cases = [c for c in cases if 'Samsung' in c['product_name']]
        
        for phone in samsung_phones[:3]:
            for case in samsung_cases[:3]:
                related_products.extend([phone, case])
        
        # PlayStation family combinations
        ps_consoles = [c for c in consoles if 'PlayStation' in c['product_name']]
        ps_games = [g for g in games if any(ps in g['product_name'] for ps in ['Spider-Man', 'God of War', 'Uncharted', 'The Last of Us', 'Horizon', 'Ratchet', 'Ghost'])]
        
        for console in ps_consoles[:3]:
            for game in ps_games[:5]:
                related_products.extend([console, game])
        
        # Xbox family combinations
        xbox_consoles = [c for c in consoles if 'Xbox' in c['product_name']]
        xbox_games = [g for g in games if any(xb in g['product_name'] for xb in ['Halo', 'Gears of War', 'Forza', 'Fable', 'State of Decay', 'Sea of Thieves'])]
        
        for console in xbox_consoles[:3]:
            for game in xbox_games[:5]:
                related_products.extend([console, game])
        
        # Add cross-platform popular games
        popular_games = [g for g in games if any(pop in g['product_name'] for pop in ['GTA', 'FIFA', 'Call of Duty', 'Minecraft', 'Fortnite', 'Red Dead', 'Assassin'])]
        
        for console in consoles[:4]:
            for game in popular_games[:3]:
                related_products.extend([console, game])
        
        # Add multiple games for same console (bundle effect)
        for console in consoles[:3]:
            selected_games = random.sample(games, min(3, len(games)))
            related_products.extend([console] + selected_games)
        
        # Add multiple accessories for same phone (accessory bundle)
        for phone in phones[:3]:
            selected_cases = random.sample(cases, min(2, len(cases)))
            related_products.extend([phone] + selected_cases)
        
        return related_products
    
    def run_continuous_adding(self):
        """Main function to continuously add products and test"""
        print("🚀 Sürekli Ürün Ekleme Sistemi Başlatılıyor...")
        print("=" * 60)
        
        # Get initial confidence values
        print("📊 İlk confidence değerleri alınıyor...")
        self.initial_confidence_values = self.test_confidence_values()
        
        if not self.initial_confidence_values:
            print("❌ İlk confidence değerleri alınamadı!")
            return
        
        print(f"✅ {len(self.initial_confidence_values)} adet kural bulundu")
        
        iteration = 1
        while True:
            print(f"\n🔄 İTERASYON {iteration}")
            print("=" * 40)
            
            # Get related products
            related_products = self.get_related_products()
            if not related_products:
                print("❌ İlişkili ürün bulunamadı!")
                break
            
            print(f"📦 {len(related_products)} adet ilişkili ürün hazırlandı")
            
            # Add products to baskets
            success = self.add_products_to_baskets(related_products, related_products, num_baskets=25)
            
            if not success:
                print("❌ Ürün ekleme başarısız!")
                break
            
            # Wait a bit for database to update
            time.sleep(2)
            
            # Test new confidence values
            self.current_confidence_values = self.test_confidence_values()
            
            if not self.current_confidence_values:
                print("❌ Yeni confidence değerleri alınamadı!")
                break
            
            # Compare and check improvement
            significant_improvement = self.compare_confidence_values()
            
            if significant_improvement:
                print(f"\n🎉 İTERASYON {iteration}: ÖNEMLİ İYİLEŞME TESPİT EDİLDİ!")
                print("=" * 50)
                
                user_input = input("❓ Devam etmek istiyor musunuz? (devam/bitir): ").lower().strip()
                
                if user_input in ['bitir', 'b', 'stop', 's']:
                    print("✅ Süreç tamamlandı!")
                    break
                elif user_input in ['devam', 'd', 'continue', 'c']:
                    print("🔄 Devam ediliyor...")
                else:
                    print("❓ Anlaşılamadı, devam ediliyor...")
            
            iteration += 1
            
            # Safety check - max 20 iterations
            if iteration > 20:
                print("⚠️ Maksimum iterasyon sayısına ulaşıldı (20)")
                break
        
        print("\n🏁 Süreç tamamlandı!")
        print("📊 Final confidence değerleri:")
        self.compare_confidence_values()

if __name__ == "__main__":
    adder = ContinuousProductAdder()
    adder.run_continuous_adding() 