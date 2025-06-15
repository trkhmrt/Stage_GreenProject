import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from database_config import DatabaseConfig
from apriori_recommender import AprioriRecommender

# Page configuration
st.set_page_config(
    page_title="Basket Recommendation System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .recommendation-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load data from database with caching"""
    db_config = DatabaseConfig()
    if db_config.test_connection():
        return db_config.get_basket_data()
    return None

@st.cache_resource
def train_model(df, min_support, min_confidence):
    """Train Apriori model with caching"""
    recommender = AprioriRecommender(min_support=min_support, min_confidence=min_confidence)
    return recommender.fit(df)

def main():
    # Header
    st.markdown('<h1 class="main-header">🛒 Basket Recommendation System</h1>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Model parameters
    min_support = st.sidebar.slider("Minimum Support", 0.001, 0.1, 0.003, 0.001)
    min_confidence = st.sidebar.slider("Minimum Confidence", 0.01, 1.0, 0.03, 0.01)
    
    # Load data
    with st.spinner("Loading data from database..."):
        df = load_data()
    
    if df is None:
        st.error("❌ Could not connect to database. Please check your connection settings.")
        st.stop()
    
    # Display basic info
    st.success(f"✅ Successfully loaded {len(df)} records from database")
    
    # Train model
    with st.spinner("Training Apriori model..."):
        recommender = train_model(df, min_support, min_confidence)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔍 Recommendations", "📈 Analytics", "⚙️ Settings"])
    
    with tab1:
        st.header("📊 Dashboard Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Baskets", df['basket_id'].nunique())
        
        with col2:
            st.metric("Total Products", df['product_name'].nunique())
        
        with col3:
            st.metric("Total Transactions", len(df))
        
        with col4:
            st.metric("Total Revenue", f"${df['product_total_price'].sum():,.2f}")
        
        # Data preview
        st.subheader("📋 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Product statistics
        st.subheader("🏆 Top Products by Basket Count")
        product_stats = recommender.get_product_stats(df)
        st.dataframe(product_stats.head(10), use_container_width=True)
    
    with tab2:
        st.header("🔍 Product Recommendations")
        
        # Get unique products for selection
        unique_products = sorted(df['product_name'].unique())
        
        # Product selection
        selected_products = st.multiselect(
            "Select products in your basket:",
            unique_products,
            help="Choose products that are currently in your basket to get recommendations"
        )
        
        if selected_products:
            # Get recommendations
            recommendations = recommender.get_recommendations(selected_products, top_n=20)
            
            if recommendations:
                st.subheader("💡 Recommended Products")
                
                # Group recommendations by type
                direct_rules = [r for r in recommendations if r.get('type') == 'direct_rule']
                partial_matches = [r for r in recommendations if r.get('type') == 'partial_match']
                category_based = [r for r in recommendations if r.get('type') == 'category_based']
                popular_products = [r for r in recommendations if r.get('type') == 'popular_product']
                
                # Show direct rules first
                if direct_rules:
                    st.markdown("**🎯 Direct Association Rules:**")
                    for i, rec in enumerate(direct_rules, 1):
                        with st.container():
                            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                            
                            with col1:
                                st.markdown(f"**{i}. {rec['product']}**")
                                st.markdown(f"*Based on: {', '.join(rec['antecedents'])}*")
                            
                            with col2:
                                st.metric("Confidence", f"{rec['confidence']:.2%}")
                            
                            with col3:
                                st.metric("Lift", f"{rec['lift']:.2f}")
                            
                            with col4:
                                st.markdown("🎯")
                            
                            st.divider()
                
                # Show partial matches
                if partial_matches:
                    st.markdown("**🔗 Partial Matches:**")
                    for i, rec in enumerate(partial_matches, 1):
                        with st.container():
                            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                            
                            with col1:
                                st.markdown(f"**{i}. {rec['product']}**")
                                st.markdown(f"*Based on: {', '.join(rec['antecedents'])}*")
                            
                            with col2:
                                st.metric("Confidence", f"{rec['confidence']:.2%}")
                            
                            with col3:
                                st.metric("Lift", f"{rec['lift']:.2f}")
                            
                            with col4:
                                st.markdown("🔗")
                            
                            st.divider()
                
                # Show category-based recommendations
                if category_based:
                    st.markdown("**📂 Category-Based:**")
                    for i, rec in enumerate(category_based, 1):
                        with st.container():
                            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                            
                            with col1:
                                st.markdown(f"**{i}. {rec['product']}**")
                                st.markdown(f"*Based on: {', '.join(rec['antecedents'])}*")
                            
                            with col2:
                                st.metric("Confidence", f"{rec['confidence']:.2%}")
                            
                            with col3:
                                st.metric("Lift", f"{rec['lift']:.2f}")
                            
                            with col4:
                                st.markdown("📂")
                            
                            st.divider()
                
                # Show popular products
                if popular_products:
                    st.markdown("**🔥 Popular Products:**")
                    for i, rec in enumerate(popular_products, 1):
                        with st.container():
                            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                            
                            with col1:
                                st.markdown(f"**{i}. {rec['product']}**")
                                st.markdown(f"*Based on: {', '.join(rec['antecedents'])}*")
                            
                            with col2:
                                st.metric("Confidence", f"{rec['confidence']:.2%}")
                            
                            with col3:
                                st.metric("Lift", f"{rec['lift']:.2f}")
                            
                            with col4:
                                st.markdown("🔥")
                            
                            st.divider()
            else:
                st.info("No recommendations found for the selected products. Try adjusting the minimum support and confidence parameters.")
        
        # Popular combinations
        st.subheader("🔥 Popular Product Combinations")
        popular_combinations = recommender.get_popular_combinations(top_n=10)
        
        for i, combo in enumerate(popular_combinations, 1):
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{i}. {', '.join(combo['products'])}**")
                
                with col2:
                    st.metric("Support", f"{combo['support']:.2%}")
                
                with col3:
                    st.metric("Frequency", combo['frequency'])
                
                st.divider()
    
    with tab3:
        st.header("📈 Analytics")
        
        # Product popularity chart
        st.subheader("📊 Product Popularity")
        top_products = product_stats.head(15)
        
        fig = px.bar(
            top_products.reset_index(),
            x='product_name',
            y='basket_count',
            title="Top 15 Products by Basket Count",
            labels={'product_name': 'Product', 'basket_count': 'Number of Baskets'}
        )
        fig.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Revenue analysis
        st.subheader("💰 Revenue Analysis")
        revenue_data = product_stats.sort_values('total_revenue', ascending=False).head(15)
        
        fig2 = px.bar(
            revenue_data.reset_index(),
            x='product_name',
            y='total_revenue',
            title="Top 15 Products by Revenue",
            labels={'product_name': 'Product', 'total_revenue': 'Total Revenue ($)'}
        )
        fig2.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Basket size distribution
        st.subheader("📦 Basket Size Distribution")
        basket_sizes = df.groupby('basket_id').size().value_counts().sort_index()
        
        fig3 = px.bar(
            x=basket_sizes.index,
            y=basket_sizes.values,
            title="Distribution of Basket Sizes",
            labels={'x': 'Number of Products', 'y': 'Number of Baskets'}
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab4:
        st.header("⚙️ Model Settings & Information")
        
        st.subheader("Current Model Parameters")
        st.write(f"- **Minimum Support**: {min_support}")
        st.write(f"- **Minimum Confidence**: {min_confidence}")
        st.write(f"- **Frequent Itemsets Found**: {len(recommender.frequent_itemsets) if recommender.frequent_itemsets is not None else 0}")
        st.write(f"- **Association Rules Generated**: {len(recommender.rules) if recommender.rules is not None else 0}")
        
        st.subheader("About Apriori Algorithm")
        st.markdown("""
        The Apriori algorithm is used for frequent itemset mining and association rule learning.
        
        **Key Concepts:**
        - **Support**: The frequency of an itemset appearing in transactions
        - **Confidence**: The probability that a rule is correct
        - **Lift**: The ratio of observed support to expected support if items were independent
        
        **How it works:**
        1. Find all frequent itemsets (itemsets with support ≥ minimum support)
        2. Generate association rules from frequent itemsets
        3. Filter rules by minimum confidence
        4. Use rules to make product recommendations
        """)
        
        # Export functionality
        st.subheader("📥 Export Data")
        
        if st.button("Export Association Rules"):
            if recommender.rules is not None:
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
                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="Download Association Rules CSV",
                    data=csv,
                    file_name="association_rules.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main() 