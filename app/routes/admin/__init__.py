"""
Admin Routes Package

This package contains all admin-related routes split into logical modules:
- views: Main admin pages and navigation
- audit: Audit log formatting helpers (routes in api/admin.py)

Note: Block CRUD routes are in app/routes/api/admin.py under /api/admin/blocks/
"""

from flask import Blueprint

# Create the main admin blueprint
bp = Blueprint('admin', __name__, url_prefix='/admin')

# Import all route modules to register them with the blueprint
from . import views
from . import audit