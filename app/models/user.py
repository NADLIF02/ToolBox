"""
Modèle User pour la gestion des utilisateurs
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db

class User(db.Model):
    """Modèle utilisateur avec authentification et autorisation"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(20), default='user')  # admin, user, pentester
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    projects = db.relationship('Project', backref='owner', lazy=True)
    scans = db.relationship('Scan', backref='user', lazy=True)
    reports = db.relationship('Report', backref='author', lazy=True)
    audit_logs = db.relationship('AuditLog', backref='user', lazy=True)
    
    def __init__(self, username, email, password, **kwargs):
        self.username = username
        self.email = email
        self.set_password(password)
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def set_password(self, password):
        """Hacher le mot de passe"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Vérifier le mot de passe"""
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role):
        """Vérifier si l'utilisateur a un rôle spécifique"""
        return self.role == role
    
    def is_admin(self):
        """Vérifier si l'utilisateur est administrateur"""
        return self.role == 'admin'
    
    def is_pentester(self):
        """Vérifier si l'utilisateur est pentester"""
        return self.role in ['admin', 'pentester']
    
    def update_last_login(self):
        """Mettre à jour la date de dernière connexion"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convertir l'utilisateur en dictionnaire"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.username}>' 