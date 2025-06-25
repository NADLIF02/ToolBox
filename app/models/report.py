"""
Modèle Report pour la gestion des rapports de tests d'intrusion
"""

from datetime import datetime
from app.extensions import db

class Report(db.Model):
    """Modèle rapport pour les tests d'intrusion"""
    
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    report_type = db.Column(db.String(50), nullable=False)  # executive, technical, detailed
    format = db.Column(db.String(20), default='pdf')  # pdf, html, docx, json
    
    # Contenu du rapport
    executive_summary = db.Column(db.Text, nullable=True)
    methodology = db.Column(db.Text, nullable=True)
    findings_summary = db.Column(db.JSON, nullable=True)  # Résumé des découvertes
    recommendations = db.Column(db.Text, nullable=True)
    conclusion = db.Column(db.Text, nullable=True)
    
    # Métadonnées
    version = db.Column(db.String(20), default='1.0')
    status = db.Column(db.String(20), default='draft')  # draft, review, approved, published
    is_public = db.Column(db.Boolean, default=False)
    
    # Fichiers générés
    file_path = db.Column(db.String(500), nullable=True)
    file_size = db.Column(db.Integer, nullable=True)  # Taille en bytes
    checksum = db.Column(db.String(64), nullable=True)  # Hash du fichier
    
    # Relations
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, title, report_type, project_id, author_id, **kwargs):
        self.title = title
        self.report_type = report_type
        self.project_id = project_id
        self.author_id = author_id
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def publish(self):
        """Publier le rapport"""
        self.status = 'published'
        self.published_at = datetime.utcnow()
        db.session.commit()
    
    def approve(self):
        """Approuver le rapport"""
        self.status = 'approved'
        db.session.commit()
    
    def set_to_review(self):
        """Mettre le rapport en révision"""
        self.status = 'review'
        db.session.commit()
    
    def get_file_size_formatted(self):
        """Obtenir la taille du fichier formatée"""
        if not self.file_size:
            return "N/A"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} TB"
    
    def get_vulnerability_summary(self):
        """Obtenir un résumé des vulnérabilités du projet"""
        from app.models.vulnerability import Vulnerability
        
        vulnerabilities = Vulnerability.query.filter_by(project_id=self.project_id).all()
        
        summary = {
            'total': len(vulnerabilities),
            'critical': len([v for v in vulnerabilities if v.severity == 'critical']),
            'high': len([v for v in vulnerabilities if v.severity == 'high']),
            'medium': len([v for v in vulnerabilities if v.severity == 'medium']),
            'low': len([v for v in vulnerabilities if v.severity == 'low']),
            'verified': len([v for v in vulnerabilities if v.verified]),
            'exploited': len([v for v in vulnerabilities if v.exploited]),
            'fixed': len([v for v in vulnerabilities if v.status == 'fixed'])
        }
        
        return summary
    
    def to_dict(self):
        """Convertir le rapport en dictionnaire"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'report_type': self.report_type,
            'format': self.format,
            'executive_summary': self.executive_summary,
            'methodology': self.methodology,
            'findings_summary': self.findings_summary,
            'recommendations': self.recommendations,
            'conclusion': self.conclusion,
            'version': self.version,
            'status': self.status,
            'is_public': self.is_public,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'file_size_formatted': self.get_file_size_formatted(),
            'checksum': self.checksum,
            'project_id': self.project_id,
            'author_id': self.author_id,
            'vulnerability_summary': self.get_vulnerability_summary(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'published_at': self.published_at.isoformat() if self.published_at else None
        }
    
    def __repr__(self):
        return f'<Report {self.title} ({self.report_type})>' 