# Deployment Guide for Streamlit Cloud

## Quick Deployment Steps

### 1. Prepare Your Repository

Make sure your repository has the following structure:
```
fermi_analysis_app/
├── simple_app.py
├── requirements.txt
├── README.md
└── components/
    └── fermi_factors.py
```

### 2. Push to GitHub

1. Create a new repository on GitHub
2. Push your code to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

### 3. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository
5. Set the main file path to: `fermi_analysis_app/simple_app.py`
6. Click "Deploy!"

### 4. Configuration

- **Repository**: Your GitHub repository URL
- **Branch**: `main` (or your default branch)
- **Main file path**: `fermi_analysis_app/simple_app.py`
- **Python version**: 3.9 or higher


### Dependencies

The app requires these packages (already in requirements.txt):
- streamlit>=1.28.0
- pandas>=1.5.0
- plotly>=5.15.0
- yfinance>=0.2.18
- numpy>=1.24.0

## Customization

### Adding More Companies

To add more company name mappings, edit the `symbol_lookup` dictionary in `simple_app.py`:

```python
symbol_lookup = {
    "apple": "AAPL", "tesla": "TSLA", "microsoft": "MSFT",
    "amazon": "AMZN", "google": "GOOGL", "meta": "META",
    "netflix": "NFLX", "nvidia": "NVDA", "berkshire": "BRK-A",
    # Add more mappings here
    "your_company": "YOUR_SYMBOL"
}
```

### Modifying Analysis Factors

To change the analysis factors or weights, edit the `calculate_fermi_scores` function in `simple_app.py`.

## Security Notes

- The app uses free, public APIs (Yahoo Finance)
- No API keys required
- All data is fetched in real-time
- No sensitive data is stored

## Performance

- The app caches data for 5 minutes to improve performance
- Analysis is performed in real-time
- Charts are generated dynamically using Plotly
