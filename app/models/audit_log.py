"""
Modèle AuditLog pour la traçabilité des actions dans la toolbox
"""

from datetime import datetime
from app.extensions import db

class AuditLog(db.Model):
    """Modèle journal d'audit pour tracer les actions des utilisateurs"""
    
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)  # create, read, update, delete, login, logout, etc.
    resource_type = db.Column(db.String(50), nullable=True)  # user, project, scan, vulnerability, report
    resource_id = db.Column(db.Integer, nullable=True)  # ID de la ressource concernée
    details = db.Column(db.JSON, nullable=True)  # Détails de l'action
    ip_address = db.Column(db.String(45), nullable=True)  # Adresse IP de l'utilisateur
    user_agent = db.Column(db.String(500), nullable=True)  # User-Agent du navigateur
    success = db.Column(db.Boolean, default=True)  # Si l'action a réussi
    error_message = db.Column(db.Text, nullable=True)  # Message d'erreur si échec
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, action, user_id=None, **kwargs):
        self.action = action
        self.user_id = user_id
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @classmethod
    def log_action(cls, action, user_id=None, **kwargs):
        """Méthode de classe pour logger une action"""
        log_entry = cls(action=action, user_id=user_id, **kwargs)
        db.session.add(log_entry)
        db.session.commit()
        return log_entry
    
    @classmethod
    def log_login(cls, user_id, ip_address, user_agent, success=True, error_message=None):
        """Logger une tentative de connexion"""
        return cls.log_action(
            action='login',
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            error_message=error_message
        )
    
    @classmethod
    def log_logout(cls, user_id, ip_address):
        """Logger une déconnexion"""
        return cls.log_action(
            action='logout',
            user_id=user_id,
            ip_address=ip_address
        )
    
    @classmethod
    def log_create(cls, user_id, resource_type, resource_id, details=None, ip_address=None):
        """Logger la création d'une ressource"""
        return cls.log_action(
            action='create',
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address
        )
    
    @classmethod
    def log_update(cls, user_id, resource_type, resource_id, details=None, ip_address=None):
        """Logger la modification d'une ressource"""
        return cls.log_action(
            action='update',
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address
        )
    
    @classmethod
    def log_delete(cls, user_id, resource_type, resource_id, details=None, ip_address=None):
        """Logger la suppression d'une ressource"""
        return cls.log_action(
            action='delete',
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address
        )
    
    @classmethod
    def log_scan_start(cls, user_id, scan_id, target, scan_type, ip_address=None):
        """Logger le démarrage d'un scan"""
        return cls.log_action(
            action='scan_start',
            user_id=user_id,
            resource_type='scan',
            resource_id=scan_id,
            details={
                'target': target,
                'scan_type': scan_type
            },
            ip_address=ip_address
        )
    
    @classmethod
    def log_scan_complete(cls, user_id, scan_id, results_count, duration, ip_address=None):
        """Logger la fin d'un scan"""
        return cls.log_action(
            action='scan_complete',
            user_id=user_id,
            resource_type='scan',
            resource_id=scan_id,
            details={
                'results_count': results_count,
                'duration': duration
            },
            ip_address=ip_address
        )
    
    @classmethod
    def log_vulnerability_found(cls, user_id, vulnerability_id, severity, target, ip_address=None):
        """Logger la découverte d'une vulnérabilité"""
        return cls.log_action(
            action='vulnerability_found',
            user_id=user_id,
            resource_type='vulnerability',
            resource_id=vulnerability_id,
            details={
                'severity': severity,
                'target': target
            },
            ip_address=ip_address
        )
    
    def to_dict(self):
        """Convertir le log en dictionnaire"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'details': self.details,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'success': self.success,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<AuditLog {self.action} by user {self.user_id}>' 