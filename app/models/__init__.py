# app/models/__init__.py
"""
This file makes the models directory a Python package.
We can also use it to expose our models more conveniently.
"""

from app.models.pet import Pet
from app.models.owner import Owner

# Now instead of: from app.models.pet import Pet
# You can write: from app.models import Pet