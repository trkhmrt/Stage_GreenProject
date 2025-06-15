#!/usr/bin/env python3
"""
Simple CLI version of the Basket Recommendation System
"""

import pandas as pd
from database_config import DatabaseConfig
from apriori_recommender import AprioriRecommender

def print_header():
    print("=" * 60)
    print("🛒 BASKET RECOMMENDATION SYSTEM")
    print("=" * 60)
    print()

def print_menu():
    print("Available options:")
    print("1. Test database connection")
    print("2. Load and analyze data")
    print("3. Get product recommendations")
    print("4. Show popular product combinations")
    print("5. Show product statistics")
    print("6. Export association rules")
    print("0. Exit")
    print()

def test_connection():
    print("Testing database connection...")
    db_config = DatabaseConfig()
    if db_config.test_connection():
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed!")
    print()

def load_and_analyze_data():
    print("Loading data from database...")
    db_config = DatabaseConfig()
    df = db_config.get_basket_data()
    
    if df is None:
        print("❌ Failed to load data!")
        return None, None
    
    print(f"✅ Successfully loaded {len(df)} records")
    print(f"📊 Data shape: {df.shape}")
    print(f"🛒 Unique baskets: {df['basket_id'].nunique()}")
    print(f"📦 Unique products: {df['product_name'].nunique()}")
    print()
    
    # Train model
    print("Training Apriori model...")
    recommender = AprioriRecommender(min_support=0.01, min_confidence=0.5)
    recommender.fit(df)
    print("✅ Model training completed!")
    print()
    
    return df, recommender

def get_recommendations(df, recommender):
    if df is None or recommender is None:
        print("❌ Please load data first (option 2)")
        return
    
    # Show available products
    unique_products = sorted(df['product_name'].unique())
    print("Available products:")
    for i, product in enumerate(unique_products, 1):
        print(f"{i:2d}. {product}")
    print()
    
    # Get user input
    try:
        product_indices = input("Enter product numbers (comma-separated): ").strip()
        if not product_indices:
            return
        
        indices = [int(x.strip()) - 1 for x in product_indices.split(",")]
        selected_products = [unique_products[i] for i in indices if 0 <= i < len(unique_products)]
        
        if not selected_products:
            print("❌ No valid products selected!")
            return
        
        print(f"\nSelected products: {', '.join(selected_products)}")
        print()
        
        # Get recommendations
        recommendations = recommender.get_recommendations(selected_products, top_n=5)
        
        if recommendations:
            print("💡 Recommended products:")
            print("-" * 50)
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec['product']}")
                print(f"   Confidence: {rec['confidence']:.2%}")
                print(f"   Lift: {rec['lift']:.2f}")
                print(f"   Based on: {', '.join(rec['antecedents'])}")
                print()
        else:
            print("❌ No recommendations found for the selected products.")
            print("💡 Try adjusting the minimum support and confidence parameters.")
        
    except (ValueError, IndexError):
        print("❌ Invalid input! Please enter valid product numbers.")
    print()

def show_popular_combinations(df, recommender):
    if df is None or recommender is None:
        print("❌ Please load data first (option 2)")
        return
    
    print("🔥 Popular Product Combinations:")
    print("-" * 50)
    
    combinations = recommender.get_popular_combinations(top_n=10)
    
    for i, combo in enumerate(combinations, 1):
        print(f"{i}. {', '.join(combo['products'])}")
        print(f"   Support: {combo['support']:.2%}")
        print(f"   Frequency: {combo['frequency']} baskets")
        print()

def show_product_stats(df, recommender):
    if df is None or recommender is None:
        print("❌ Please load data first (option 2)")
        return
    
    print("📊 Product Statistics:")
    print("-" * 50)
    
    stats = recommender.get_product_stats(df)
    
    print("Top 10 products by basket count:")
    print(f"{'Product':<30} {'Baskets':<8} {'Revenue':<12}")
    print("-" * 50)
    
    for i, (product, row) in enumerate(stats.head(10).iterrows(), 1):
        print(f"{product[:29]:<30} {row['basket_count']:<8} ${row['total_revenue']:<11.2f}")
    print()

def export_rules(df, recommender):
    if df is None or recommender is None:
        print("❌ Please load data first (option 2)")
        return
    
    if recommender.rules is None:
        print("❌ No association rules available!")
        return
    
    filename = "association_rules.csv"
    
    # Convert rules to a more readable format
    export_rules = []
    for _, rule in recommender.rules.iterrows():
        export_rules.append({
            'Antecedents': ', '.join(list(rule['antecedents'])),
            'Consequents': ', '.join(list(rule['consequents'])),
            'Support': rule['support'],
            'Confidence': rule['confidence'],
            'Lift': rule['lift']
        })
    
    export_df = pd.DataFrame(export_rules)
    export_df.to_csv(filename, index=False)
    
    print(f"✅ Association rules exported to {filename}")
    print(f"📊 Total rules exported: {len(export_df)}")
    print()

def main():
    print_header()
    
    df = None
    recommender = None
    
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (0-6): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                test_connection()
            elif choice == "2":
                df, recommender = load_and_analyze_data()
            elif choice == "3":
                get_recommendations(df, recommender)
            elif choice == "4":
                show_popular_combinations(df, recommender)
            elif choice == "5":
                show_product_stats(df, recommender)
            elif choice == "6":
                export_rules(df, recommender)
            else:
                print("❌ Invalid choice! Please enter a number between 0 and 6.")
                print()
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print()

if __name__ == "__main__":
    main() 