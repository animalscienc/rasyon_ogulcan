# Zootekni Pro: Intelligent Rationing System
# Version: 5.0 (Ultimate Ration Engineering & Economic Intelligence System)

## Project Overview
- **Project Name**: Zootekni Pro
- **Type**: Desktop Application (Decision Support System for Livestock)
- **Core Functionality**: Advanced ration optimization with economic analysis for ruminant and poultry nutrition
- **Target Users**: Livestock producers, nutritionists, and veterinarians in Turkey

## UI/UX Specification

### Layout Structure
- **Window Model**: Single main window with modal dialogs
- **Layout**: 
  - Left sidebar (vertical navigation) - 220px fixed width
  - Main content area (right) - dynamic, uses QGridLayout
  - Top header bar with logo and user info - 60px height

### Visual Design

#### Color Palette (Dark Mode - Primary)
- **Background Primary**: #0D1117 (deep dark)
- **Background Secondary**: #161B22 (card backgrounds)
- **Background Tertiary**: #21262D (elevated surfaces)
- **Accent Primary**: #58A6FF (bright blue - buttons, links)
- **Accent Secondary**: #7EE787 (green - success/positive)
- **Accent Warning**: #F0883E (orange - warnings)
- **Accent Danger**: #F85149 (red - errors)
- **Text Primary**: #F0F6FC (white)
- **Text Secondary**: #8B949E (muted gray)
- **Border**: #30363D

#### Light Mode
- **Background Primary**: #FFFFFF
- **Background Secondary**: #F6F8FA
- **Background Tertiary**: #EAEEF2
- **Accent Primary**: #0969DA
- **Accent Secondary**: #1A7F37
- **Text Primary**: #1F2328
- **Text Secondary**: #656d76

#### Typography
- **Font Family**: "Segoe UI", "SF Pro Display", system-ui
- **Heading 1**: 24px, weight 600
- **Heading 2**: 20px, weight 600
- **Heading 3**: 16px, weight 600
- **Body**: 14px, weight 400
- **Small**: 12px, weight 400

#### Spacing System
- **Base unit**: 8px
- **Margins**: 16px, 24px, 32px
- **Padding**: 8px, 12px, 16px, 24px
- **Border Radius**: 8px (buttons), 12px (cards), 15px (panels)

#### Visual Effects
- **Box Shadow (cards)**: 0 4px 12px rgba(0,0,0,0.3)
- **Transition**: all 0.2s ease-in-out
- **Hover effects**: brightness increase, subtle scale

### Components
- **Sidebar Navigation**: Menu items with icons, active state highlight
- **Data Tables**: Striped rows, sortable columns, hover highlight
- **Buttons**: Primary (filled), Secondary (outlined), Icon buttons
- **Input Fields**: Labeled, with validation states
- **Cards**: Rounded corners, shadows, hover lift
- **Charts**: Interactive, tooltips, legends
- **Dialogs**: Modal, centered, with close button

## Functionality Specification

### Core Features

#### 1. Authentication
- Login screen with username/password
- Session management
- Remember me functionality

#### 2. Feed Library Management
- Import/export CSV feeds (yemler.csv format)
- CRUD operations for feed items
- Feed search and filtering
- Category management (forages, concentrates, supplements)

#### 3. Ration Optimization
- Linear programming solver (scipy.optimize.linprog)
- NRC (2021), INRA, ARC feeding standards
- Constraints: eNDF, RDP/RUP, NEL, ME, Ca/P, DCAD
- Multi-animal group support

#### 4. Economic Analysis
- IOFC (Income Over Feed Cost) calculation
- Marginal analysis (break-even calculations)
- Shadow pricing (dual values from optimization)
- Volatility/sensitivity analysis (10% price shocks)

#### 5. Reporting
- PDF report generation (FPDF/ReportLab)
- Charts: Radar (nutrient spider), Donut (cost distribution)
- Environmental impact (methane, nitrogen excretion)

#### 6. Data Persistence
- SQLite database for ration archives
- Version control (v1, v2, v3...)
- Export to CSV/PDF

### User Interactions
- Sidebar navigation between modules
- Drag-and-drop feed selection
- Real-time calculation updates
- Form validation with error messages

### Edge Cases
- Infeasible ration solutions (constraint relaxation advice)
- Empty feed library handling
- Network-independent operation
- Large dataset handling (310+ feeds)

## Technical Architecture

### MVC Structure
```
models/          # Data layer
  - feed_model.py       # Feed data handling
  - ration_model.py    # Ration logic
  - user_model.py       # Authentication
  - database.py         # SQLite operations

views/          # UI layer
  - login_view.py       # Login screen
  - dashboard_view.py   # Main dashboard
  - feed_editor_view.py # Feed management
  - optimizer_view.py  # Ration optimizer
  - reports_view.py    # Reports/charts
  - widgets.py         # Reusable UI components
  - styles.py          # QSS styling

controllers/    # Business logic
  - auth_controller.py
  - feed_controller.py
  - ration_controller.py
  - report_controller.py

utils/          # Utilities
  - constants.py       # NRC/INRA values
  - calculations.py    # Mathematical functions
  - validators.py      # Input validation
  - logger.py          # Logging

database/      # SQLite
  - rations.db        # Ration archives

data/           # Static data
  - yemler.csv        # Feed library

assets/         # Resources
  - logo.png          # App logo
  - icons/           # Icon resources
```

## Acceptance Criteria

### Visual Checkpoints
- [x] Login screen displays with professional branding
- [x] Dark mode renders correctly with specified colors
- [x] Sidebar navigation animates smoothly
- [x] Tables are sortable and responsive
- [x] Charts render with proper legends

### Functional Tests
- [x] Feed CRUD operations work correctly
- [x] Ration optimization solves within 5 seconds
- [x] Income Over Feed Cost calculates accurately
- [x] PDF reports generate with business branding
- [x] Database stores and retrieves ration versions
- [x] Error handling shows meaningful messages
- [x] Application runs without freezing UI