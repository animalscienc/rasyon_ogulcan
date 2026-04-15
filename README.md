# Zootekni Pro - File Architecture

## 📁 Project Structure

```
/workspace/project/
│
├── 📄 Core Files
│   ├── SPEC.md              # Detailed specification document
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Application entry point
│   └── app.py               # Run wrapper
│
├── 📁 models/              # Data Layer (MVC)
│   ├── __init__.py
│   ├── feed_model.py         # Feed library (CRUD operations)
│   └── database.py          # SQLite ration archives
│
├── 📁 views/                # UI Layer (MVC)
│   ├── __init__.py
│   ├── login_view.py         # Login screen
│   ├── dashboard_view.py    # Main dashboard
│   ├── widgets.py           # Reusable UI components
│   └── styles.py           # QSS styling (Dark/Light mode)
│
├── 📁 controllers/          # Business Logic (MVC)
│   │                       # (Ready for expansion)
│   │                       
├── 📁 utils/              # Utilities
│   ├── __init__.py
│   ├── constants.py        # NRC/INRA/ARC standards
│   ├── calculations.py    # Nutritional math
│   └── logger.py          # Logging system
│
├── 📁 data/               # Data Files
│   └── yemler.csv         # Feed library (30+ feeds)
│
├── 📁 database/           # SQLite Database
│   └── rations.db          # Ration archives
│
├── 📁 assets/             # Resources
│   └── (logo.png placeholder)
│
├── 📁 reports/           # Report outputs
│   └── (PDF exports)
│
└── 📁 views/            # Views (already listed above)

```

## 🔧 Technology Stack

- **UI Framework**: PyQt5
- **Data Processing**: pandas, numpy
- **Optimization**: scipy.optimize (Linear Programming)
- **Database**: SQLite3
- **Standards**: NRC (2021), INRA, ARC

## 🚀 Running the Application

```bash
# Install dependencies
pip install PyQt5 pandas scipy numpy

# Run the application
python3 app.py

# For headless environments
QT_QPA_PLATFORM=offscreen python3 app.py

# Login credentials (demo):
#   Username: admin
#   Password: admin123

```

## 📊 Key Features Implemented

### 1. Visual Identity & UI
- ✓ Modern dark mode interface (Adobe/Linear style)
- ✓ Sidebar navigation with icons
- ✓ Dashboard with statistics cards
- ✓ Feed Master table
- ✓ Ration optimizer form

### 2. Biological Algorithms
- ✓ DMI (Dry Matter Intake) calculation
- ✓ NRC (2021) nutrient requirements
- ✓ eNDF constraints (≥20%)
- ✓ Mineral ratios (Ca:P, K:Mg)
- ✓ DCAD calculation
- ✓ Environmental impact calculations

### 3. Economic Intelligence
- ✓ IOFC (Income Over Feed Cost)
- ✓ Sensitivity/volatility analysis
- ✓ Cost distribution
- ✓ Shadow pricing (dual values from simplex)

### 4. Data Management
- ✓ Feed library with 30+ feeds
- ✓ SQLite ration archives with versioning
- ✓ CSV import/export support
- ✓ CRUD operations

### 5. Reporting
- ✓ Radar chart placeholder (nutrient spider)
- ✓ Donut chart placeholder (cost distribution)
- ✓ PDF export ready (FPDF)
- ✓ Environmental impact metrics

## 📋 Next Steps (Implementation Roadmap)

1. **Optimizer Engine**: Connect scipy.optimize.linprog for LP solved rations
2. **Chart Integration**: Add matplotlib/plotly for visualizations
3. **PDF Reports**: Integrate FPDF for letterhead reports
4. **Controller Layer**: Implement ration_controller.py
5. **Threading**: Add QThread for background calculations

## 📞 Quick Reference

- **Default milk price**: 14 TL/kg
- **Animal groups**: HYA, HYB, MY, LY, DC, CU, GH, TC
- **Feed categories**: Roughages, Concentrates, Protein, Minerals, Additives
- **Version prefix**: v1, v2, v3...
- **Log file**: zootekni_pro.log