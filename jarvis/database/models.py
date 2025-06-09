"""
Database models for J.A.R.V.I.S.
Defines the database schema and provides database initialization.
"""

import os
import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create base model class
Base = declarative_base()

# Set up logging
logger = logging.getLogger(__name__)

class User(Base):
    """User model for storing user information."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    interactions = relationship('Interaction', back_populates='user')
    preferences = relationship('UserPreference', back_populates='user')
    feedback = relationship('UserFeedback', back_populates='user')
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

class Interaction(Base):
    """Model for storing user interactions with J.A.R.V.I.S."""
    __tablename__ = 'interactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    was_successful = Column(Boolean, default=True)
    category = Column(String(50), nullable=True)  # e.g., 'weather', 'news', etc.
    
    # Relationships
    user = relationship('User', back_populates='interactions')
    
    def __repr__(self):
        return f"<Interaction(id={self.id}, query='{self.query[:20]}...', timestamp={self.timestamp})>"

class UserPreference(Base):
    """Model for storing user preferences."""
    __tablename__ = 'user_preferences'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category = Column(String(50), nullable=False)  # e.g., 'ui', 'notifications'
    name = Column(String(100), nullable=False)
    value = Column(String(255), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='preferences')
    
    def __repr__(self):
        return f"<UserPreference(category='{self.category}', name='{self.name}', value='{self.value}')>"

class UserFeedback(Base):
    """Model for storing user feedback."""
    __tablename__ = 'user_feedback'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    feedback_text = Column(Text, nullable=False)
    is_positive = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='feedback')
    
    def __repr__(self):
        return f"<UserFeedback(id={self.id}, is_positive={self.is_positive})>"

class LearningPattern(Base):
    """Model for storing learned patterns from user interactions."""
    __tablename__ = 'learning_patterns'
    
    id = Column(Integer, primary_key=True)
    pattern = Column(String(255), nullable=False, unique=True)
    count = Column(Integer, default=1)
    success_rate = Column(Integer, default=100)  # Percentage
    last_used = Column(DateTime, default=datetime.utcnow)
    example_query = Column(Text, nullable=True)
    example_response = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<LearningPattern(pattern='{self.pattern}', count={self.count}, success_rate={self.success_rate}%)>"

# Database initialization functions
def get_engine():
    """Get or create a database engine."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Use SQLite as fallback
        db_path = os.path.join(os.path.expanduser("~"), ".jarvis", "jarvis.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        database_url = f"sqlite:///{db_path}"
        logger.warning(f"DATABASE_URL not found, using SQLite at {db_path}")
    
    return create_engine(database_url)

def initialize_database():
    """Initialize the database schema if it doesn't exist."""
    try:
        engine = get_engine()
        # Create all tables if they don't exist
        Base.metadata.create_all(engine)
        
        # Create session factory
        Session = sessionmaker(bind=engine)
        
        # Create a default user if none exists
        session = Session()
        user_count = session.query(User).count()
        
        if user_count == 0:
            default_user = User(name='sir')
            session.add(default_user)
            session.commit()
            logger.info("Created default user")
        
        session.close()
        
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False

def get_session():
    """Get a new database session."""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

# Functions for database operations
def get_or_create_user(name='sir', email=None):
    """Get the default user or create one if not exists."""
    session = get_session()
    
    try:
        if email:
            user = session.query(User).filter_by(email=email).first()
        else:
            user = session.query(User).first()
            
        if not user:
            user = User(name=name, email=email)
            session.add(user)
            session.commit()
            
        return user
    finally:
        session.close()

def record_interaction(user_id, query, response, was_successful=True, category=None):
    """Record a user interaction in the database."""
    session = get_session()
    
    try:
        interaction = Interaction(
            user_id=user_id,
            query=query,
            response=response,
            was_successful=was_successful,
            category=category
        )
        session.add(interaction)
        session.commit()
        return True
    except Exception as e:
        logger.error(f"Error recording interaction: {e}")
        session.rollback()
        return False
    finally:
        session.close()

def update_user_preference(user_id, category, name, value):
    """Update a user preference in the database."""
    session = get_session()
    
    try:
        # Check if preference already exists
        preference = session.query(UserPreference).filter_by(
            user_id=user_id, category=category, name=name
        ).first()
        
        if preference:
            preference.value = value
            preference.updated_at = datetime.utcnow()
        else:
            # Create new preference
            preference = UserPreference(
                user_id=user_id,
                category=category,
                name=name,
                value=value
            )
            session.add(preference)
            
        session.commit()
        return True
    except Exception as e:
        logger.error(f"Error updating user preference: {e}")
        session.rollback()
        return False
    finally:
        session.close()

def get_user_preferences(user_id, category=None):
    """Get user preferences from the database."""
    session = get_session()
    
    try:
        query = session.query(UserPreference).filter_by(user_id=user_id)
        
        if category:
            query = query.filter_by(category=category)
            
        preferences = query.all()
        
        # Convert to dictionary
        result = {}
        for pref in preferences:
            if pref.category not in result:
                result[pref.category] = {}
            result[pref.category][pref.name] = pref.value
            
        return result
    finally:
        session.close()

def record_user_feedback(user_id, feedback_text, is_positive=True):
    """Record user feedback in the database."""
    session = get_session()
    
    try:
        feedback = UserFeedback(
            user_id=user_id,
            feedback_text=feedback_text,
            is_positive=is_positive
        )
        session.add(feedback)
        session.commit()
        return True
    except Exception as e:
        logger.error(f"Error recording user feedback: {e}")
        session.rollback()
        return False
    finally:
        session.close()

def update_learning_pattern(pattern, success=True, query=None, response=None):
    """Update a learning pattern in the database."""
    session = get_session()
    
    try:
        # Check if pattern already exists
        pattern_obj = session.query(LearningPattern).filter_by(pattern=pattern).first()
        
        if pattern_obj:
            pattern_obj.count += 1
            pattern_obj.last_used = datetime.utcnow()
            
            # Update success rate
            if success:
                # Weighted average to slowly move towards success
                pattern_obj.success_rate = int(0.9 * pattern_obj.success_rate + 0.1 * 100)
            else:
                # Weighted average to slowly move towards failure
                pattern_obj.success_rate = int(0.9 * pattern_obj.success_rate + 0.1 * 0)
                
            # Update examples if provided
            if query and response:
                pattern_obj.example_query = query
                pattern_obj.example_response = response
        else:
            # Create new pattern
            pattern_obj = LearningPattern(
                pattern=pattern,
                count=1,
                success_rate=100 if success else 0,
                example_query=query,
                example_response=response
            )
            session.add(pattern_obj)
            
        session.commit()
        return True
    except Exception as e:
        logger.error(f"Error updating learning pattern: {e}")
        session.rollback()
        return False
    finally:
        session.close()

def get_learning_patterns(min_count=1, limit=100):
    """Get learning patterns from the database."""
    session = get_session()
    
    try:
        patterns = session.query(LearningPattern).filter(
            LearningPattern.count >= min_count
        ).order_by(
            LearningPattern.count.desc()
        ).limit(limit).all()
        
        return patterns
    finally:
        session.close()