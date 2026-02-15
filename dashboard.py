"""Streamlit dashboard for market analysis."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent))

from src.database.connection import db
from src.ml.volatility import VolatilityMonitor
import config

# Page configuration
st.set_page_config(
    page_title="Market Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


def get_portfolio_summary(portfolio_type: str):
    """Get portfolio summary statistics."""
    query = """
        SELECT 
            p.name,
            p.portfolio_type,
            COUNT(ph.id) as num_holdings,
            SUM(ph.quantity * ph.purchase_price) as total_invested
        FROM portfolio p
        LEFT JOIN portfolio_holdings ph ON p.id = ph.portfolio_id
        WHERE p.portfolio_type = %s
        GROUP BY p.id, p.name, p.portfolio_type
    """
    results = db.execute_query(query, (portfolio_type,))
    return pd.DataFrame(results) if results else pd.DataFrame()


def get_stock_performance(symbol: str, days: int = 30):
    """Get stock performance data."""
    query = """
        SELECT date, close, volume
        FROM daily_data
        WHERE symbol = %s
        AND date >= CURRENT_DATE - CAST(%s || ' days' AS INTERVAL)
        ORDER BY date
    """
    results = db.execute_query(query, (symbol, days))
    return pd.DataFrame(results) if results else pd.DataFrame()


def get_volatility_data(exchange: str = None, days: int = 7):
    """Get volatility alerts data."""
    if exchange:
        query = """
            SELECT va.*, si.company_name, si.exchange
            FROM volatility_alerts va
            JOIN stock_info si ON va.symbol = si.symbol
            WHERE si.exchange = %s
            AND va.alert_date >= CURRENT_DATE - CAST(%s || ' days' AS INTERVAL)
            ORDER BY va.alert_date DESC, va.volatility_score DESC
        """
        results = db.execute_query(query, (exchange, days))
    else:
        query = """
            SELECT va.*, si.company_name, si.exchange
            FROM volatility_alerts va
            JOIN stock_info si ON va.symbol = si.symbol
            WHERE va.alert_date >= CURRENT_DATE - CAST(%s || ' days' AS INTERVAL)
            ORDER BY va.alert_date DESC, va.volatility_score DESC
        """
        results = db.execute_query(query, (days,))
    
    return pd.DataFrame(results) if results else pd.DataFrame()


def plot_stock_chart(df: pd.DataFrame, symbol: str):
    """Create interactive stock price chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['close'],
        mode='lines',
        name='Close Price',
        line=dict(color='#1f77b4', width=2)
    ))
    
    fig.update_layout(
        title=f'{symbol} - Stock Price',
        xaxis_title='Date',
        yaxis_title='Price',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_volume_chart(df: pd.DataFrame, symbol: str):
    """Create volume bar chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['date'],
        y=df['volume'],
        name='Volume',
        marker_color='#2ca02c'
    ))
    
    fig.update_layout(
        title=f'{symbol} - Trading Volume',
        xaxis_title='Date',
        yaxis_title='Volume',
        template='plotly_white',
        height=300
    )
    
    return fig


def plot_volatility_distribution(df: pd.DataFrame, exchange: str):
    """Create volatility distribution chart."""
    fig = px.histogram(
        df,
        x='volatility_score',
        color='alert_type',
        title=f'{exchange} - Volatility Distribution',
        labels={'volatility_score': 'Volatility Score', 'alert_type': 'Alert Type'},
        color_discrete_map={'HIGH': '#d62728', 'MEDIUM': '#ff7f0e', 'LOW': '#2ca02c'}
    )
    
    fig.update_layout(template='plotly_white', height=400)
    return fig


def main():
    """Main dashboard function."""
    
    # Sidebar
    st.sidebar.markdown('<p class="main-header">📈 Market Analysis</p>', unsafe_allow_html=True)
    
    page = st.sidebar.radio(
        "Navigation",
        ["Overview", "Japanese Investments (NISA)", "Korean Trading (Active)", "Volatility Monitor"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Settings")
    days_filter = st.sidebar.slider("Days to Display", 7, 365, 30)
    
    # Main content
    if page == "Overview":
        st.markdown('<p class="main-header">Market Analysis Dashboard</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Japanese Stocks", len(config.JAPANESE_SYMBOLS))
        
        with col2:
            st.metric("Korean Stocks", len(config.KOREAN_SYMBOLS))
        
        with col3:
            volatility_df = get_volatility_data(days=7)
            high_alerts = len(volatility_df[volatility_df['alert_type'] == 'HIGH']) if not volatility_df.empty else 0
            st.metric("High Volatility Alerts (7d)", high_alerts)
        
        st.markdown("---")
        
        # Recent volatility alerts
        st.markdown('<p class="section-header">Recent Volatility Alerts</p>', unsafe_allow_html=True)
        volatility_df = get_volatility_data(days=7)
        
        if not volatility_df.empty:
            display_df = volatility_df[['symbol', 'company_name', 'exchange', 'alert_date', 
                                        'volatility_score', 'price_at_alert', 'alert_type']]
            display_df['volatility_score'] = display_df['volatility_score'].round(4)
            display_df['price_at_alert'] = display_df['price_at_alert'].round(2)
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("No recent volatility alerts")
    
    elif page == "Japanese Investments (NISA)":
        st.markdown('<p class="main-header">🇯🇵 Japanese Investments (NISA)</p>', unsafe_allow_html=True)
        st.markdown("*Conservative Long-term Investment Strategy*")
        
        # Portfolio summary
        portfolio_df = get_portfolio_summary('NISA')
        if not portfolio_df.empty:
            st.markdown('<p class="section-header">Portfolio Summary</p>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Holdings", int(portfolio_df['num_holdings'].sum()))
            with col2:
                total = portfolio_df['total_invested'].sum() if 'total_invested' in portfolio_df else 0
                st.metric("Total Invested", f"¥{total:,.0f}")
        
        st.markdown("---")
        
        # Stock selection
        selected_symbol = st.selectbox("Select Stock", config.JAPANESE_SYMBOLS)
        
        if selected_symbol:
            # Get stock performance
            df = get_stock_performance(selected_symbol, days_filter)
            
            if not df.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Price chart
                    fig = plot_stock_chart(df, selected_symbol)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Volume chart
                    fig = plot_volume_chart(df, selected_symbol)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Statistics
                st.markdown('<p class="section-header">Statistics</p>', unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)
                
                latest_price = df['close'].iloc[-1]
                price_change = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
                avg_volume = df['volume'].mean()
                
                with col1:
                    st.metric("Current Price", f"¥{latest_price:.2f}")
                with col2:
                    st.metric("Price Change", f"{price_change:.2f}%")
                with col3:
                    st.metric("Avg Volume", f"{avg_volume:,.0f}")
                with col4:
                    st.metric("Data Points", len(df))
            else:
                st.warning(f"No data available for {selected_symbol}")
    
    elif page == "Korean Trading (Active)":
        st.markdown('<p class="main-header">🇰🇷 Korean Trading (Active)</p>', unsafe_allow_html=True)
        st.markdown("*High-risk Active Trading Strategy*")
        
        # Portfolio summary
        portfolio_df = get_portfolio_summary('ACTIVE')
        if not portfolio_df.empty:
            st.markdown('<p class="section-header">Portfolio Summary</p>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Holdings", int(portfolio_df['num_holdings'].sum()))
            with col2:
                total = portfolio_df['total_invested'].sum() if 'total_invested' in portfolio_df else 0
                st.metric("Total Invested", f"₩{total:,.0f}")
        
        st.markdown("---")
        
        # Stock selection
        selected_symbol = st.selectbox("Select Stock", config.KOREAN_SYMBOLS)
        
        if selected_symbol:
            # Get stock performance
            df = get_stock_performance(selected_symbol, days_filter)
            
            if not df.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Price chart
                    fig = plot_stock_chart(df, selected_symbol)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Volume chart
                    fig = plot_volume_chart(df, selected_symbol)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Statistics
                st.markdown('<p class="section-header">Statistics</p>', unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)
                
                latest_price = df['close'].iloc[-1]
                price_change = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
                avg_volume = df['volume'].mean()
                
                with col1:
                    st.metric("Current Price", f"₩{latest_price:.2f}")
                with col2:
                    st.metric("Price Change", f"{price_change:.2f}%")
                with col3:
                    st.metric("Avg Volume", f"{avg_volume:,.0f}")
                with col4:
                    st.metric("Data Points", len(df))
            else:
                st.warning(f"No data available for {selected_symbol}")
    
    else:  # Volatility Monitor
        st.markdown('<p class="main-header">⚠️ Volatility Monitor</p>', unsafe_allow_html=True)
        st.markdown("*ML-based Price Volatility Detection*")
        
        # Exchange filter
        exchange_filter = st.selectbox("Select Exchange", ["All", "JAPANESE", "KOREAN"])
        
        # Get volatility data
        if exchange_filter == "All":
            volatility_df = get_volatility_data(days=days_filter)
        else:
            volatility_df = get_volatility_data(exchange=exchange_filter, days=days_filter)
        
        if not volatility_df.empty:
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                high_count = len(volatility_df[volatility_df['alert_type'] == 'HIGH'])
                st.metric("High Alerts", high_count, delta=None)
            
            with col2:
                medium_count = len(volatility_df[volatility_df['alert_type'] == 'MEDIUM'])
                st.metric("Medium Alerts", medium_count, delta=None)
            
            with col3:
                avg_volatility = volatility_df['volatility_score'].mean()
                st.metric("Avg Volatility", f"{avg_volatility:.4f}")
            
            st.markdown("---")
            
            # Volatility distribution chart
            fig = plot_volatility_distribution(volatility_df, exchange_filter)
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed alerts table
            st.markdown('<p class="section-header">Detailed Alerts</p>', unsafe_allow_html=True)
            display_df = volatility_df[['symbol', 'company_name', 'exchange', 'alert_date', 
                                        'volatility_score', 'price_at_alert', 'alert_type', 'message']]
            display_df['volatility_score'] = display_df['volatility_score'].round(6)
            display_df['price_at_alert'] = display_df['price_at_alert'].round(2)
            
            # Color code by alert type
            def highlight_alerts(row):
                if row['alert_type'] == 'HIGH':
                    return ['background-color: #ffcccc'] * len(row)
                elif row['alert_type'] == 'MEDIUM':
                    return ['background-color: #fff3cd'] * len(row)
                return [''] * len(row)
            
            styled_df = display_df.style.apply(highlight_alerts, axis=1)
            st.dataframe(styled_df, use_container_width=True)
        else:
            st.info(f"No volatility alerts in the last {days_filter} days")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "Market Analysis Dashboard\n\n"
        "A comprehensive ELT pipeline and dashboard for analyzing Japanese and Korean stock markets.\n\n"
        "Features:\n"
        "- Real-time data from yfinance\n"
        "- PostgreSQL data warehouse\n"
        "- ML-based volatility monitoring\n"
        "- Portfolio tracking"
    )


if __name__ == "__main__":
    main()
