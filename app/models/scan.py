"""
Modèles Scan et ScanResult pour la gestion des scans de tests d'intrusion
"""

from datetime import datetime
from app.extensions import db

class Scan(db.Model):
    """Modèle scan pour les tests d'intrusion"""
    
    __tablename__ = 'scans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    scan_type = db.Column(db.String(50), nullable=False)  # discovery, vulnerability, exploitation, forensics
    target = db.Column(db.String(255), nullable=False)  # IP, domaine, URL
    ports = db.Column(db.String(500), nullable=True)  # Ports à scanner
    options = db.Column(db.JSON, nullable=True)  # Options spécifiques au scan
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed, cancelled
    progress = db.Column(db.Integer, default=0)  # Progression en pourcentage
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Integer, nullable=True)  # Durée en secondes
    error_message = db.Column(db.Text, nullable=True)
    
    # Relations
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    results = db.relationship('ScanResult', backref='scan', lazy=True, cascade='all, delete-orphan')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, scan_type, target, project_id, user_id, **kwargs):
        self.name = name
        self.scan_type = scan_type
        self.target = target
        self.project_id = project_id
        self.user_id = user_id
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def start_scan(self):
        """Démarrer le scan"""
        self.status = 'running'
        self.start_time = datetime.utcnow()
        self.progress = 0
        db.session.commit()
    
    def complete_scan(self):
        """Terminer le scan"""
        self.status = 'completed'
        self.end_time = datetime.utcnow()
        self.progress = 100
        if self.start_time:
            self.duration = int((self.end_time - self.start_time).total_seconds())
        db.session.commit()
    
    def fail_scan(self, error_message):
        """Marquer le scan comme échoué"""
        self.status = 'failed'
        self.end_time = datetime.utcnow()
        self.error_message = error_message
        if self.start_time:
            self.duration = int((self.end_time - self.start_time).total_seconds())
        db.session.commit()
    
    def update_progress(self, progress):
        """Mettre à jour la progression du scan"""
        self.progress = progress
        db.session.commit()
    
    def get_duration_formatted(self):
        """Obtenir la durée formatée"""
        if not self.duration:
            return "N/A"
        
        hours = self.duration // 3600
        minutes = (self.duration % 3600) // 60
        seconds = self.duration % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    def to_dict(self):
        """Convertir le scan en dictionnaire"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'scan_type': self.scan_type,
            'target': self.target,
            'ports': self.ports,
            'options': self.options,
            'status': self.status,
            'progress': self.progress,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'duration_formatted': self.get_duration_formatted(),
            'error_message': self.error_message,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'results_count': len(self.results),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Scan {self.name} ({self.scan_type})>'

class ScanResult(db.Model):
    """Modèle pour les résultats de scan"""
    
    __tablename__ = 'scan_results'
    
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('scans.id'), nullable=False)
    result_type = db.Column(db.String(50), nullable=False)  # port, service, vulnerability, etc.
    target = db.Column(db.String(255), nullable=False)
    port = db.Column(db.Integer, nullable=True)
    service = db.Column(db.String(100), nullable=True)
    version = db.Column(db.String(100), nullable=True)
    banner = db.Column(db.Text, nullable=True)
    data = db.Column(db.JSON, nullable=True)  # Données supplémentaires
    severity = db.Column(db.String(20), nullable=True)  # low, medium, high, critical
    confidence = db.Column(db.Integer, nullable=True)  # Niveau de confiance (0-100)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, scan_id, result_type, target, **kwargs):
        self.scan_id = scan_id
        self.result_type = result_type
        self.target = target
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self):
        """Convertir le résultat en dictionnaire"""
        return {
            'id': self.id,
            'scan_id': self.scan_id,
            'result_type': self.result_type,
            'target': self.target,
            'port': self.port,
            'service': self.service,
            'version': self.version,
            'banner': self.banner,
            'data': self.data,
            'severity': self.severity,
            'confidence': self.confidence,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ScanResult {self.result_type} on {self.target}>' 