"""
Modèle Project pour la gestion des projets de tests d'intrusion
"""

from datetime import datetime
from app.extensions import db

class Project(db.Model):
    """Modèle projet pour organiser les tests d'intrusion"""
    
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(120), nullable=True)
    scope = db.Column(db.Text, nullable=False)  # Périmètre du test
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    budget = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Relations
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    scans = db.relationship('Scan', backref='project', lazy=True)
    vulnerabilities = db.relationship('Vulnerability', backref='project', lazy=True)
    reports = db.relationship('Report', backref='project', lazy=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, client_name, scope, start_date, end_date, owner_id, **kwargs):
        self.name = name
        self.client_name = client_name
        self.scope = scope
        self.start_date = start_date
        self.end_date = end_date
        self.owner_id = owner_id
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def is_active(self):
        """Vérifier si le projet est actif"""
        return self.status == 'active'
    
    def is_completed(self):
        """Vérifier si le projet est terminé"""
        return self.status == 'completed'
    
    def is_overdue(self):
        """Vérifier si le projet est en retard"""
        return datetime.utcnow().date() > self.end_date and self.status == 'active'
    
    def get_progress(self):
        """Calculer le progrès du projet basé sur les scans complétés"""
        total_scans = len(self.scans)
        completed_scans = len([scan for scan in self.scans if scan.status == 'completed'])
        
        if total_scans == 0:
            return 0
        
        return (completed_scans / total_scans) * 100
    
    def get_critical_vulnerabilities(self):
        """Obtenir les vulnérabilités critiques du projet"""
        return [vuln for vuln in self.vulnerabilities if vuln.severity == 'critical']
    
    def get_high_vulnerabilities(self):
        """Obtenir les vulnérabilités élevées du projet"""
        return [vuln for vuln in self.vulnerabilities if vuln.severity == 'high']
    
    def to_dict(self):
        """Convertir le projet en dictionnaire"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'client_name': self.client_name,
            'client_email': self.client_email,
            'scope': self.scope,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'status': self.status,
            'priority': self.priority,
            'budget': self.budget,
            'notes': self.notes,
            'owner_id': self.owner_id,
            'progress': self.get_progress(),
            'critical_vulnerabilities_count': len(self.get_critical_vulnerabilities()),
            'high_vulnerabilities_count': len(self.get_high_vulnerabilities()),
            'total_scans': len(self.scans),
            'completed_scans': len([scan for scan in self.scans if scan.status == 'completed']),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Project {self.name}>' 