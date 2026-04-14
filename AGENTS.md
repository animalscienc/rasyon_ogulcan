# Zootekni Pro - Intelligent Rationing System

Zootekni Pro is a comprehensive ration engineering and economic intelligence system designed for livestock farming in Turkey. Built with Python, PyQt5, and advanced optimization algorithms.

## Project Structure

```
/workspace/project/
├── main.py              # Application entry point
├── pyproject.toml       # Project dependencies
├── utils/               # Utility modules
│   ├── auth.py          # Authentication utilities
│   ├── database.py      # SQLite database manager
│   ├── logger.py        # Logging setup
│   ├── reporting.py     # PDF report generation
│   └── visualization.py # Chart generation
├── models/              # Data models
│   ├── nutrition_models.py  # NRC 2021, INRA, ARC standards
│   └── optimization_model.py # Linear programming optimizer
├── views/               # PyQt5 UI views
│   ├── login_view.py    # Login screen
│   └── dashboard_view.py # Main dashboard
├── controllers/          # Business logic
│   ├── auth_controller.py
│   └── dashboard_controller.py
├── data/                # Data files
│   └── yemler.csv       # Feed database
└── reports/             # Generated reports
```

## Key Features

### Biological Algorithms
- NRC 2021 dairy cattle nutrition standards
- INRA and ARC support
- Dynamic DMI calculation
- Protein fractionation (RDP/RUP)
- Mineral requirements (Ca/P balance, DCAD)
- Environmental impact (methane, nitrogen)

### Economic Analysis
- IOFC (Income Over Feed Cost)
- Marginal analysis
- Shadow pricing
- Sensitivity analysis (price volatility)

### Visualization
- Radar charts (nutrition spider)
- Donut charts (cost distribution)
- Bar charts (comparison)

### Reporting
- Professional PDF reports
- Feed instructions
- Economic summaries

## Running the Application

```bash
uv run python main.py
```

## Default Credentials
- Username: admin
- Password: admin123

## Dependencies
- PyQt5 >= 5.15
- pandas >= 3.0
- numpy >= 2.4
- scipy >= 1.17
- matplotlib >= 3.10
- fpdf >= 1.7
- reportlab >= 4.4
