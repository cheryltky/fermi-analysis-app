# Fermi Analysis Dashboard

A simple Streamlit app that performs Fermi analysis on stocks to help with investment decisions.

## Features

- **Stock Analysis**: Enter a company name or stock symbol to analyze
- **Spider Chart**: Visual representation of 8 key investment factors
- **Fermi Analysis**: Systematic evaluation using estimation techniques
- **Investment Recommendations**: Buy/Hold/Sell recommendations based on analysis
- **Price Charts**: Historical price data and key statistics

## Key Factors Analyzed

1. **Market Position** (15%) - Competitive position and market share
2. **Financial Health** (20%) - Revenue growth, profitability, debt levels
3. **Management Quality** (15%) - Leadership effectiveness and strategy
4. **Industry Trends** (10%) - Sector growth and market dynamics
5. **Valuation Metrics** (15%) - P/E ratios, book value, growth rates
6. **Risk Factors** (10%) - Volatility, regulatory risks, competition
7. **Growth Potential** (10%) - Expansion opportunities and innovation
8. **Economic Sensitivity** (5%) - Performance in different economic conditions

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run simple_app.py
   ```

2. Enter a company name or stock symbol in the sidebar
3. Click "Run Fermi Analysis" to generate results
4. Review the spider chart and detailed analysis

## Example Usage

- Company names: Apple, Tesla, Microsoft, Amazon, Google
- Stock symbols: AAPL, TSLA, MSFT, AMZN, GOOGL

## Disclaimer

This analysis is for educational purposes only and should not be considered as financial advice. Always do your own research before making investment decisions.

## Technologies Used

- **Streamlit** - Web app framework
- **Plotly** - Interactive charts and visualizations
- **Yahoo Finance** - Stock data via yfinance
- **Pandas** - Data manipulation
- **NumPy** - Numerical computations

## Deployment

This app can be deployed on Streamlit Cloud:

1. Push your code to GitHub
2. Connect your GitHub repository to Streamlit Cloud
3. Deploy with the command: `streamlit run simple_app.py`

## File Structure

```
fermi_analysis_app/
├── simple_app.py          # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── components/
    └── fermi_factors.py  # Factor definitions
``` 
