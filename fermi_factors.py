# Fermi Analysis Factors Configuration

FERMI_FACTORS = {
    'Market Position': {
        'description': 'Company\'s competitive position and market share',
        'weight': '15%',
        'considerations': [
            'Market capitalization size',
            'Industry leadership position',
            'Brand recognition and reputation',
            'Competitive advantages'
        ],
        'data_sources': 'Yahoo Finance, Market data'
    },
    'Financial Health': {
        'description': 'Revenue growth, profitability, and debt levels',
        'weight': '20%',
        'considerations': [
            'Profit margins and earnings growth',
            'Debt-to-equity ratio',
            'Cash flow stability',
            'Return on equity (ROE)'
        ],
        'data_sources': 'Financial statements, Yahoo Finance'
    },
    'Management Quality': {
        'description': 'Leadership effectiveness and strategic vision',
        'weight': '15%',
        'considerations': [
            'Management track record',
            'Strategic decision making',
            'Corporate governance',
            'Innovation and adaptability'
        ],
        'data_sources': 'Company reports, News analysis'
    },
    'Industry Trends': {
        'description': 'Sector growth and market dynamics',
        'weight': '10%',
        'considerations': [
            'Industry growth rate',
            'Market trends and disruptions',
            'Regulatory environment',
            'Sector performance vs market'
        ],
        'data_sources': 'Sector ETFs, Industry reports'
    },
    'Valuation Metrics': {
        'description': 'P/E ratios, book value, and growth rates',
        'weight': '15%',
        'considerations': [
            'Price-to-earnings (P/E) ratio',
            'Price-to-book (P/B) ratio',
            'Dividend yield',
            'Growth rate vs valuation'
        ],
        'data_sources': 'Yahoo Finance, Financial ratios'
    },
    'Risk Factors': {
        'description': 'Market volatility, regulatory risks, and competition',
        'weight': '10%',
        'considerations': [
            'Stock price volatility',
            'Beta coefficient',
            'Regulatory risks',
            'Competitive threats'
        ],
        'data_sources': 'Market data, Risk metrics'
    },
    'Growth Potential': {
        'description': 'Expansion opportunities and innovation capacity',
        'weight': '10%',
        'considerations': [
            'Revenue growth rate',
            'Market expansion opportunities',
            'Innovation and R&D',
            'Geographic expansion'
        ],
        'data_sources': 'Financial statements, Company reports'
    },
    'Economic Sensitivity': {
        'description': 'Performance in different economic conditions',
        'weight': '5%',
        'considerations': [
            'Economic cycle sensitivity',
            'Interest rate impact',
            'Inflation sensitivity',
            'Recession resilience'
        ],
        'data_sources': 'Economic analysis, Historical performance'
    }
} 
