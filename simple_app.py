import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Fermi Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

def get_stock_data(symbol):
    """Get stock data from Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1Y")
        info = ticker.info
        return data, info
    except:
        return None, None

def calculate_fermi_scores(stock_data, stock_info):
    """Calculate Fermi analysis scores for each factor"""
    
    scores = {}
    
    # Market Position (15% weight)
    market_cap = stock_info.get('marketCap', 0)
    if market_cap > 100e9:  # Large cap
        scores['Market Position'] = 8.5
    elif market_cap > 10e9:  # Mid cap
        scores['Market Position'] = 7.0
    elif market_cap > 2e9:  # Small cap
        scores['Market Position'] = 6.0
    else:
        scores['Market Position'] = 5.0
    
    # Financial Health (20% weight)
    profit_margins = stock_info.get('profitMargins', 0)
    debt_to_equity = stock_info.get('debtToEquity', 0)
    roe = stock_info.get('returnOnEquity', 0)
    
    financial_score = 5.0
    if profit_margins > 0.15:
        financial_score += 2.0
    elif profit_margins > 0.05:
        financial_score += 1.0
    
    if debt_to_equity < 0.5:
        financial_score += 1.5
    elif debt_to_equity < 1.0:
        financial_score += 1.0
    
    if roe > 0.15:
        financial_score += 1.5
    elif roe > 0.10:
        financial_score += 1.0
    
    scores['Financial Health'] = min(financial_score, 10.0)
    
    # Management Quality (15% weight)
    roa = stock_info.get('returnOnAssets', 0)
    revenue_growth = stock_info.get('revenueGrowth', 0)
    
    mgmt_score = 5.0
    if roa > 0.10:
        mgmt_score += 2.0
    elif roa > 0.05:
        mgmt_score += 1.0
    
    if revenue_growth > 0.15:
        mgmt_score += 2.0
    elif revenue_growth > 0.05:
        mgmt_score += 1.0
    
    scores['Management Quality'] = min(mgmt_score, 10.0)
    
    # Industry Trends (10% weight)
    returns = stock_data['Close'].pct_change().dropna()
    recent_performance = returns.tail(30).mean() * 252 * 100
    
    if recent_performance > 10:
        scores['Industry Trends'] = 8.0
    elif recent_performance > 5:
        scores['Industry Trends'] = 7.0
    elif recent_performance > 0:
        scores['Industry Trends'] = 6.0
    else:
        scores['Industry Trends'] = 4.0
    
    # Valuation Metrics (15% weight)
    pe_ratio = stock_info.get('trailingPE', 0)
    pb_ratio = stock_info.get('priceToBook', 0)
    dividend_yield = stock_info.get('dividendYield', 0)
    
    valuation_score = 5.0
    if 0 < pe_ratio < 15:
        valuation_score += 2.0
    elif 15 <= pe_ratio < 25:
        valuation_score += 1.0
    elif pe_ratio > 50:
        valuation_score -= 1.0
    
    if 0 < pb_ratio < 3:
        valuation_score += 1.5
    elif 3 <= pb_ratio < 5:
        valuation_score += 0.5
    elif pb_ratio > 10:
        valuation_score -= 1.0
    
    if dividend_yield > 0.03:
        valuation_score += 1.0
    elif dividend_yield > 0.01:
        valuation_score += 0.5
    
    scores['Valuation Metrics'] = min(max(valuation_score, 0.0), 10.0)
    
    # Risk Factors (10% weight)
    volatility = returns.std() * np.sqrt(252) * 100
    beta = stock_info.get('beta', 1)
    
    risk_score = 5.0
    if volatility < 0.15:
        risk_score += 2.0
    elif volatility < 0.25:
        risk_score += 1.0
    elif volatility > 0.40:
        risk_score -= 1.0
    
    if 0.8 <= beta <= 1.2:
        risk_score += 1.5
    elif beta < 0.8:
        risk_score += 1.0
    elif beta > 1.5:
        risk_score -= 1.0
    
    scores['Risk Factors'] = min(max(risk_score, 0.0), 10.0)
    
    # Growth Potential (10% weight)
    if revenue_growth > 0.20:
        scores['Growth Potential'] = 9.0
    elif revenue_growth > 0.10:
        scores['Growth Potential'] = 7.5
    elif revenue_growth > 0.05:
        scores['Growth Potential'] = 6.5
    else:
        scores['Growth Potential'] = 5.0
    
    # Economic Sensitivity (5% weight)
    if volatility < 0.20:
        scores['Economic Sensitivity'] = 7.0
    elif volatility < 0.30:
        scores['Economic Sensitivity'] = 6.0
    elif volatility > 0.40:
        scores['Economic Sensitivity'] = 4.0
    else:
        scores['Economic Sensitivity'] = 5.0
    
    return scores

def create_spider_chart(scores):
    """Create a spider chart for the Fermi scores"""
    
    categories = list(scores.keys())
    values = list(scores.values())
    
    # Add the first value to the end to close the polygon
    values += values[:1]
    categories += categories[:1]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Fermi Scores',
        line_color='#1f77b4',
        fillcolor='rgba(31, 119, 180, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=False,
        title="Fermi Analysis Spider Chart",
        title_x=0.5,
        font=dict(size=12)
    )
    
    return fig

def calculate_overall_score(scores):
    """Calculate weighted overall score"""
    weights = {
        'Market Position': 0.15,
        'Financial Health': 0.20,
        'Management Quality': 0.15,
        'Industry Trends': 0.10,
        'Valuation Metrics': 0.15,
        'Risk Factors': 0.10,
        'Growth Potential': 0.10,
        'Economic Sensitivity': 0.05
    }
    
    total_score = 0.0
    for factor, score in scores.items():
        total_score += score * weights.get(factor, 0.1)
    
    return total_score

def main():
    st.title("📊 Fermi Analysis Dashboard")
    st.markdown("### Analyze investment opportunities using Fermi estimation techniques")
    
    # Sidebar
    with st.sidebar:
        st.header("🔍 Stock Analysis")
        
        # Market selection
        market = st.selectbox(
            "Select Market:",
            ["🇺🇸 US Market", "🇦🇺 Australian Market", "🌍 Other International"]
        )
        
        # Input method selection
        input_method = st.radio(
            "Select input method:",
            ["Company Name", "Stock Symbol"]
        )
        
        symbol = None
        
        if market == "🇺🇸 US Market":
            if input_method == "Company Name":
                company_name = st.text_input("Enter US company name:", placeholder="e.g., Apple, Tesla, Microsoft")
                if company_name:
                    # US companies lookup
                    us_symbol_lookup = {
                        "apple": "AAPL", "tesla": "TSLA", "microsoft": "MSFT",
                        "amazon": "AMZN", "google": "GOOGL", "meta": "META",
                        "netflix": "NFLX", "nvidia": "NVDA", "berkshire": "BRK-A",
                        "vanguard": "VGS", "vgs": "VGS", "vanguard global": "VGS"
                    }
                    symbol = us_symbol_lookup.get(company_name.lower(), company_name.upper())
            else:
                symbol = st.text_input("Enter US stock symbol:", placeholder="e.g., AAPL, TSLA, VGS").upper()
                
        elif market == "🇦🇺 Australian Market":
            if input_method == "Company Name":
                company_name = st.text_input("Enter Australian company name:", placeholder="e.g., Commonwealth Bank, BHP, VAS")
                if company_name:
                    # Australian companies lookup
                    aus_symbol_lookup = {
                        # Australian ETFs
                        "vanguard australian shares": "VAS.AX", "vas": "VAS.AX",
                        "vanguard global shares": "VGS.AX", "vgs australia": "VGS.AX",
                        "vanguard international shares": "VTS.AX", "vts": "VTS.AX",
                        "vanguard emerging markets": "VGE.AX", "vge": "VGE.AX",
                        "vanguard australian property": "VAP.AX", "vap": "VAP.AX",
                        "vanguard australian bonds": "VGB.AX", "vgb": "VGB.AX",
                        # Australian Stocks
                        "commonwealth bank": "CBA.AX", "cba": "CBA.AX",
                        "westpac": "WBC.AX", "wbc": "WBC.AX",
                        "anz": "ANZ.AX", "australia and new zealand": "ANZ.AX",
                        "nab": "NAB.AX", "national australia bank": "NAB.AX",
                        "bhp": "BHP.AX", "bhp billiton": "BHP.AX",
                        "rio tinto": "RIO.AX", "rio": "RIO.AX",
                        "csl": "CSL.AX", "csl limited": "CSL.AX",
                        "telstra": "TLS.AX", "tls": "TLS.AX"
                    }
                    symbol = aus_symbol_lookup.get(company_name.lower(), company_name.upper())
            else:
                user_symbol = st.text_input("Enter Australian stock symbol:", placeholder="e.g., VAS.AX, CBA.AX, BHP.AX").upper()
                # Auto-add .AX suffix if not present
                if user_symbol and not user_symbol.endswith('.AX'):
                    symbol = user_symbol + '.AX'
                else:
                    symbol = user_symbol
                
        else:  # Other International
            if input_method == "Company Name":
                company_name = st.text_input("Enter company name:", placeholder="e.g., Company Name")
                symbol = company_name.upper()
            else:
                symbol = st.text_input("Enter stock symbol:", placeholder="e.g., SYMBOL").upper()
        
        # Market-specific help
        if market == "🇦🇺 Australian Market":
            st.info("💡 Australian stocks need .AX suffix (e.g., VAS.AX, CBA.AX)")
        elif market == "🌍 Other International":
            st.info("💡 Some international stocks may need country suffix")
        
        # Run analysis button
        run_analysis = st.button("🚀 Run Fermi Analysis", type="primary")
    
    # Main content
    if 'run_analysis' in locals() and run_analysis and symbol:
        with st.spinner("Fetching stock data and performing analysis..."):
            # Get stock data
            stock_data, stock_info = get_stock_data(symbol)
            
            if stock_data is None or stock_info is None or stock_data.empty:
                st.error(f"Could not fetch data for {symbol}. Please check the symbol and try again.")
                st.info("💡 For Australian stocks, make sure to add .AX suffix (e.g., VGS.AX, VAS.AX)")
                return
            
            # Calculate Fermi scores
            fermi_scores = calculate_fermi_scores(stock_data, stock_info)
            overall_score = calculate_overall_score(fermi_scores)
            
            # Display results
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.subheader(f"📈 Analysis Results for {symbol}")
            
            with col2:
                current_price = stock_data['Close'].iloc[-1]
                st.metric("Current Price", f"${current_price:.2f}")
            
            with col3:
                price_change = stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[-2]
                price_change_pct = (price_change / stock_data['Close'].iloc[-2]) * 100
                st.metric("Daily Change", f"{price_change_pct:.2f}%", f"{price_change:.2f}")
            
            # Overall score
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Overall Score", f"{overall_score:.1f}/10")
            
            with col2:
                risk_level = "Low" if overall_score >= 7 else "Medium" if overall_score >= 5 else "High"
                st.metric("Risk Level", risk_level)
            
            with col3:
                recommendation = "Buy" if overall_score >= 7 else "Hold" if overall_score >= 5 else "Sell"
                st.metric("Recommendation", recommendation)
            
            # Spider chart
            st.subheader("🕷️ Fermi Analysis Spider Chart")
            fig = create_spider_chart(fermi_scores)
            st.plotly_chart(fig, use_container_width=True)
            
            # Factor breakdown
            st.subheader("🔍 Factor Breakdown")
            
            for factor, score in fermi_scores.items():
                with st.expander(f"{factor} - Score: {score:.1f}/10"):
                    st.progress(score / 10)
                    
                    if score >= 7:
                        st.success("✅ Strong positive signal")
                    elif score >= 5:
                        st.warning("⚠️ Neutral signal")
                    else:
                        st.error("❌ Potential concern")
            
            # Price chart
            st.subheader("📈 Price Analysis")
            
            price_fig = go.Figure()
            price_fig.add_trace(go.Scatter(
                x=stock_data.index,
                y=stock_data['Close'],
                mode='lines',
                name='Close Price',
                line=dict(color='#1f77b4', width=2)
            ))
            
            price_fig.update_layout(
                title=f"{symbol} Stock Price (1 Year)",
                xaxis_title="Date",
                yaxis_title="Price ($)",
                hovermode='x unified'
            )
            
            st.plotly_chart(price_fig, use_container_width=True)
            
            # Key statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("52-Week High", f"${stock_data['High'].max():.2f}")
            
            with col2:
                st.metric("52-Week Low", f"${stock_data['Low'].min():.2f}")
            
            with col3:
                returns = ((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / stock_data['Close'].iloc[0]) * 100
                st.metric("1-Year Return", f"{returns:.2f}%")
            
            with col4:
                volatility = stock_data['Close'].pct_change().std() * np.sqrt(252) * 100
                st.metric("Annualized Volatility", f"{volatility:.2f}%")
    
    elif 'run_analysis' in locals() and run_analysis:
        st.warning("Please enter a company name or stock symbol to begin analysis.")
    
    # Information section
    else:
        st.markdown("""
        ## 🎯 What is Fermi Analysis?
        
        Fermi analysis is a method of estimation that breaks down complex problems into smaller, 
        more manageable components. In investment analysis, it helps evaluate stocks by considering 
        multiple factors systematically.
        
        ### 📊 Key Factors Analyzed:
        
        1. **Market Position** - Company's competitive position and market share
        2. **Financial Health** - Revenue growth, profitability, and debt levels
        3. **Management Quality** - Leadership effectiveness and strategic vision
        4. **Industry Trends** - Sector growth and market dynamics
        5. **Valuation Metrics** - P/E ratios, book value, and growth rates
        6. **Risk Factors** - Market volatility, regulatory risks, and competition
        7. **Growth Potential** - Expansion opportunities and innovation capacity
        8. **Economic Sensitivity** - Performance in different economic conditions
        
        ### 🚀 How to Use This Dashboard:
        
        1. **Select your market** (US, Australian, or International)
        2. **Choose input method** (Company Name or Stock Symbol)
        3. **Enter the company/symbol** based on your selection
        4. **Click "Run Fermi Analysis"** to generate results
        5. **Review the spider chart** and detailed report
        6. **Use the insights** to make informed investment decisions
        
        ### 💡 Pro Tips:
        - **US Market**: Direct symbols (AAPL, TSLA, VGS, VTI, SPY)
        - **Australian Market**: Add .AX suffix (VAS.AX, CBA.AX, BHP.AX)
        - **International**: May need country-specific suffixes
        - **Unknown symbols** will show an error if data isn't available
        
        **⚠️ Disclaimer:** This analysis is for educational purposes only and should not be considered as financial advice.
        """)

if __name__ == "__main__":
    main() 
