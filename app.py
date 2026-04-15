"""
Zootekni Pro - Intelligent Rationing System
Run this file to start the application

Usage:
    python3 app.py

The application requires a display. For headless environments, use:
    QT_QPA_PLATFORM=offscreen python3 app.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Qt platform if not available
if "QT_QPA_PLATFORM" not in os.environ:
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

# Run main application
from main import main
sys.exit(main())