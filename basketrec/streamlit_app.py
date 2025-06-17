import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from apriori_recommender import AprioriRecommender
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Basket Recommendation System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
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
    .confidence-high { color: #28a745; }
    .confidence-medium { color: #ffc107; }
    .confidence-low { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_apriori_model():
    """Load and cache the Apriori model"""
    with st.spinner("🤖 Apriori modeli yükleniyor..."):
        recommender = AprioriRecommender(
            min_support=0.02,
            min_confidence=0.3,
            min_lift=1.2
        )
        
        # Load data
        basket_data = recommender.load_basket_data()
        if basket_data is None:
            st.error("❌ Veri yüklenemedi!")
            return None
        
        # Train model
        recommender.fit()
        return recommender

def get_confidence_color(confidence):
    """Get color based on confidence level"""
    if confidence >= 0.7:
        return "confidence-high"
    elif confidence >= 0.4:
        return "confidence-medium"
    else:
        return "confidence-low"

def main():
    # Header
    st.markdown('<h1 class="main-header">🛒 Basket Recommendation System</h1>', unsafe_allow_html=True)
    
    # Load model
    recommender = load_apriori_model()
    if recommender is None:
        st.stop()
    
    # Sidebar
    st.sidebar.title("🎯 Kontrol Paneli")
    
    # Navigation buttons
    st.sidebar.markdown("### 📱 Sayfa Seçin:")
    
    if st.sidebar.button("📊 Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
    
    if st.sidebar.button("🎯 Ürün Önerileri", use_container_width=True):
        st.session_state.page = "recommendations"
    
    if st.sidebar.button("🔗 İlişki Kuralları", use_container_width=True):
        st.session_state.page = "rules"
    
    if st.sidebar.button("📈 İstatistikler", use_container_width=True):
        st.session_state.page = "statistics"
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"
    
    # Show selected page
    if st.session_state.page == "dashboard":
        show_dashboard(recommender)
    elif st.session_state.page == "recommendations":
        show_recommendations(recommender)
    elif st.session_state.page == "rules":
        show_association_rules(recommender)
    elif st.session_state.page == "statistics":
        show_statistics(recommender)

def show_dashboard(recommender):
    """Show main dashboard"""
    st.header("📊 Dashboard")
    
    # Get insights
    insights = recommender.get_basket_insights()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📦 Toplam Sepet</h3>
            <h2>{insights['total_baskets']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🛍️ Toplam Ürün</h3>
            <h2>{insights['total_products']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Toplam İşlem</h3>
            <h2>{insights['total_transactions']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Ortalama Ürün/Sepet</h3>
            <h2>{insights['avg_products_per_basket']:.1f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Popular combinations
    st.subheader("🏆 En Popüler Ürün Kombinasyonları")
    popular_combinations = recommender.get_popular_combinations(top_n=10)
    
    if popular_combinations:
        for i, combo in enumerate(popular_combinations, 1):
            with st.expander(f"{i}. {', '.join(combo['products'])}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Support", f"{combo['support']:.1%}")
                with col2:
                    st.metric("Sıklık", f"{combo['frequency']} sepet")
                with col3:
                    st.write(combo['explanation'])
    else:
        st.info("Henüz popüler kombinasyon bulunamadı.")
    
    # Basket size distribution
    st.subheader("📊 Sepet Boyutu Dağılımı")
    basket_dist = insights['basket_size_distribution']
    
    if basket_dist:
        fig = px.bar(
            x=list(basket_dist.keys()),
            y=list(basket_dist.values()),
            title="Sepet Başına Ürün Sayısı Dağılımı",
            labels={'x': 'Ürün Sayısı', 'y': 'Sepet Sayısı'}
        )
        st.plotly_chart(fig, use_container_width=True)

def show_recommendations(recommender):
    """Show product recommendations"""
    st.header("🎯 Ürün Önerileri")
    
    # Get available products
    if recommender.basket_data is not None:
        available_products = sorted(recommender.basket_data['product_name'].unique())
    else:
        available_products = []
    
    # Product selection
    st.subheader("🔍 Ürün Seçin")
    
    # Search box
    search_term = st.text_input("Ürün ara:", placeholder="Örn: PlayStation, Xbox, Spider-Man...")
    
    if search_term:
        filtered_products = [p for p in available_products if search_term.lower() in p.lower()]
    else:
        filtered_products = available_products
    
    # Product selection
    selected_products = st.multiselect(
        "Ürünler seçin:",
        options=filtered_products,
        default=filtered_products[:1] if filtered_products else None,
        help="Birden fazla ürün seçebilirsiniz"
    )
    
    # Recommendation parameters
    col1, col2 = st.columns(2)
    with col1:
        top_n = st.slider("Öneri sayısı:", min_value=1, max_value=20, value=10)
    with col2:
        min_confidence = st.slider("Minimum confidence:", min_value=0.1, max_value=1.0, value=0.3, step=0.1)
    
    # Get recommendations automatically when products are selected
    if selected_products:
        with st.spinner("Öneriler hesaplanıyor..."):
            recommendations = recommender.get_recommendations(selected_products, top_n=top_n)
            
            if recommendations:
                st.subheader(f"📋 '{', '.join(selected_products)}' için Öneriler")
                
                # Filter by confidence
                filtered_recommendations = [r for r in recommendations if r['confidence'] >= min_confidence]
                
                if filtered_recommendations:
                    for i, rec in enumerate(filtered_recommendations, 1):
                        confidence_class = get_confidence_color(rec['confidence'])
                        
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h4>{i}. {rec['product']}</h4>
                            <p><strong class="{confidence_class}">Confidence: {rec['confidence']:.1%}</strong> | 
                            <strong>Lift: {rec['lift']:.2f}</strong></p>
                            <p><em>{rec['explanation']}</em></p>
                            <small>Kural: {', '.join(rec['antecedents'])} → {', '.join(rec['consequents'])}</small>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning(f"Seçilen confidence ({min_confidence:.1%}) için öneri bulunamadı.")
            else:
                st.info("Bu ürünler için öneri bulunamadı.")

def show_association_rules(recommender):
    """Show association rules"""
    st.header("🔗 İlişki Kuralları")
    
    if recommender.rules is None or len(recommender.rules) == 0:
        st.info("Henüz ilişki kuralı bulunamadı.")
        return
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_confidence_filter = st.slider(
            "Minimum Confidence:",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1
        )
    
    with col2:
        min_lift_filter = st.slider(
            "Minimum Lift:",
            min_value=0.0,
            max_value=20.0,
            value=1.0,
            step=0.1
        )
    
    with col3:
        max_rules = st.slider(
            "Maksimum Kural Sayısı:",
            min_value=10,
            max_value=100,
            value=20
        )
    
    # Filter rules
    filtered_rules = recommender.rules[
        (recommender.rules['confidence'] >= min_confidence_filter) &
        (recommender.rules['lift'] >= min_lift_filter)
    ].head(max_rules)
    
    st.subheader(f"📊 {len(filtered_rules)} İlişki Kuralı")
    
    # Display rules
    for i, (_, rule) in enumerate(filtered_rules.iterrows(), 1):
        antecedents = list(rule['antecedents'])
        consequents = list(rule['consequents'])
        
        confidence_class = get_confidence_color(rule['confidence'])
        
        st.markdown(f"""
        <div class="recommendation-card">
            <h4>{i}. {', '.join(antecedents)} → {', '.join(consequents)}</h4>
            <p><strong class="{confidence_class}">Confidence: {rule['confidence']:.1%}</strong> | 
            <strong>Support: {rule['support']:.1%}</strong> | 
            <strong>Lift: {rule['lift']:.2f}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Visualization
    st.subheader("📈 İlişki Kuralları Görselleştirmesi")
    
    if len(filtered_rules) > 0:
        # Create a copy of filtered_rules with frozenset converted to list for JSON serialization
        plot_data = filtered_rules.copy()
        plot_data['antecedents_str'] = plot_data['antecedents'].apply(lambda x: ', '.join(list(x)))
        plot_data['consequents_str'] = plot_data['consequents'].apply(lambda x: ', '.join(list(x)))
        
        # Confidence vs Lift scatter plot
        fig = px.scatter(
            plot_data,
            x='confidence',
            y='lift',
            size='support',
            hover_data=['antecedents_str', 'consequents_str'],
            title="Confidence vs Lift Dağılımı"
        )
        st.plotly_chart(fig, use_container_width=True)

def show_statistics(recommender):
    """Show detailed statistics"""
    st.header("📈 Detaylı İstatistikler")
    
    if recommender.basket_data is None:
        st.error("Veri bulunamadı!")
        return
    
    # Product statistics
    st.subheader("🛍️ Ürün İstatistikleri")
    product_stats = recommender.get_product_stats()
    
    if product_stats is not None:
        # Top products by basket count
        top_products = product_stats.head(10)
        
        fig = px.bar(
            top_products,
            x='basket_count',
            y=top_products.index,
            orientation='h',
            title="En Çok Sepette Bulunan Ürünler"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Product details table
        st.subheader("📋 Ürün Detayları")
        st.dataframe(
            product_stats.head(20).round(2),
            use_container_width=True
        )
    
    # Basket insights
    st.subheader("📊 Sepet Analizi")
    insights = recommender.get_basket_insights()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**En Popüler Ürünler:**")
        for product, count in list(insights['most_common_products'].items())[:5]:
            st.write(f"• {product}: {count} sepet")
    
    with col2:
        st.write("**Sepet Boyutu Dağılımı:**")
        for size, count in insights['basket_size_distribution'].items():
            st.write(f"• {size} ürün: {count} sepet")

if __name__ == "__main__":
    main() 