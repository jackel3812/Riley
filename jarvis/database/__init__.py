"""
Database modules for the RILEY system.
This package contains database models and utilities.
"""

# Import the models to make them available from the package
from jarvis.database.models import (
    User, Interaction, UserPreference, 
    UserFeedback, LearningPattern,
    initialize_database, get_or_create_user
)