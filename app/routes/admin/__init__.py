"""
Admin Routes Package

This package contains all admin-related routes split into logical modules:
- views: Main admin pages and navigation
- blocks: Block CRUD operations
- series: Recurring block series management  
- templates: Block template management
- reasons: Block reason and sub-reason management
- bulk: Bulk operations and multi-court operations
- audit: Audit log functionality
"""

from flask import Blueprint

# Create the main admin blueprint
bp = Blueprint('admin', __name__, url_prefix='/admin')

# Import all route modules to register them with the blueprint
from . import views
from . import blocks
from . import series
from . import templates
from . import reasons
from . import bulk
from . import audit