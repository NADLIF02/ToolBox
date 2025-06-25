#!/usr/bin/env python3
"""
Toolbox Automatisée pour Tests d'Intrusion - «Le partenaire»
Application principale Flask
"""

import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/toolbox.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def create_app():
    """Factory function pour créer l'application Flask"""
    app = Flask(__name__)
    
    # Configuration de base
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///toolbox.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
    # Configuration CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Configuration du rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Initialiser les extensions
    from app.extensions import db, jwt, migrate
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # Enregistrer les blueprints
    from app.views.auth import auth_bp
    from app.views.api import api_bp
    from app.views.dashboard import dashboard_bp
    from app.views.reports import reports_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    
    # Routes de base
    @app.route('/')
    def index():
        """Page d'accueil de la toolbox"""
        return jsonify({
            'message': 'Toolbox Automatisée pour Tests d\'Intrusion',
            'version': '1.0.0',
            'status': 'running',
            'documentation': '/api/docs'
        })
    
    @app.route('/health')
    def health_check():
        """Point de terminaison pour vérifier la santé de l'application"""
        return jsonify({
            'status': 'healthy',
            'timestamp': '2024-01-01T00:00:00Z'
        })
    
    @app.route('/api/docs')
    def api_docs():
        """Documentation de l'API"""
        return jsonify({
            'endpoints': {
                'auth': '/auth',
                'api': '/api',
                'dashboard': '/dashboard',
                'reports': '/reports'
            },
            'swagger': '/api/swagger'
        })
    
    # Gestionnaire d'erreurs
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({'error': 'Internal server error'}), 500
    
    # Créer les tables de base de données
    with app.app_context():
        db.create_all()
        logger.info("Base de données initialisée")
    
    return app

def create_celery(app):
    """Factory function pour créer l'instance Celery"""
    from app.extensions import celery
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

# Créer l'application
app = create_app()

if __name__ == '__main__':
    # Démarrer l'application en mode développement
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    ) 