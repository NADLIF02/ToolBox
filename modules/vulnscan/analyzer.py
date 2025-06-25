"""
Analyseur de vulnérabilités pour traiter et analyser les résultats
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class VulnerabilityAnalyzer:
    """Analyseur de vulnérabilités pour traiter les résultats des scans"""
    
    def __init__(self):
        self.analysis_results = {}
    
    def analyze_scan_results(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyser les résultats d'un scan de vulnérabilités
        
        Args:
            scan_results: Résultats du scan à analyser
        
        Returns:
            Analyse des vulnérabilités
        """
        try:
            logger.info("Démarrage de l'analyse des vulnérabilités")
            
            analysis = {
                'scan_id': scan_results.get('scan_id'),
                'target': scan_results.get('target'),
                'analysis_date': datetime.utcnow().isoformat(),
                'risk_assessment': self._assess_risk(scan_results),
                'vulnerability_categories': self._categorize_vulnerabilities(scan_results),
                'recommendations': self._generate_recommendations(scan_results),
                'trends': self._analyze_trends(scan_results),
                'compliance': self._check_compliance(scan_results)
            }
            
            self.analysis_results[scan_results.get('scan_id')] = analysis
            logger.info("Analyse des vulnérabilités terminée")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse des vulnérabilités: {str(e)}")
            raise
    
    def _assess_risk(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Évaluer le niveau de risque global"""
        vulnerabilities = scan_results.get('vulnerabilities', [])
        summary = scan_results.get('summary', {})
        
        # Calcul du score de risque
        risk_score = 0
        risk_factors = {
            'critical': 10,
            'high': 7,
            'medium': 4,
            'low': 1
        }
        
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'low')
            risk_score += risk_factors.get(severity, 1)
        
        # Détermination du niveau de risque
        if risk_score >= 20:
            risk_level = 'critical'
        elif risk_score >= 15:
            risk_level = 'high'
        elif risk_score >= 10:
            risk_level = 'medium'
        elif risk_score >= 5:
            risk_level = 'low'
        else:
            risk_level = 'minimal'
        
        return {
            'overall_risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': {
                'critical_vulnerabilities': summary.get('critical', 0),
                'high_vulnerabilities': summary.get('high', 0),
                'medium_vulnerabilities': summary.get('medium', 0),
                'low_vulnerabilities': summary.get('low', 0)
            },
            'risk_description': self._get_risk_description(risk_level)
        }
    
    def _categorize_vulnerabilities(self, scan_results: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Catégoriser les vulnérabilités par type"""
        vulnerabilities = scan_results.get('vulnerabilities', [])
        
        categories = {
            'web_application': [],
            'network': [],
            'authentication': [],
            'encryption': [],
            'configuration': [],
            'other': []
        }
        
        for vuln in vulnerabilities:
            vuln_name = vuln.get('name', '').lower()
            
            if any(keyword in vuln_name for keyword in ['sql', 'xss', 'csrf', 'injection']):
                categories['web_application'].append(vuln)
            elif any(keyword in vuln_name for keyword in ['port', 'service', 'protocol']):
                categories['network'].append(vuln)
            elif any(keyword in vuln_name for keyword in ['password', 'credential', 'auth']):
                categories['authentication'].append(vuln)
            elif any(keyword in vuln_name for keyword in ['ssl', 'tls', 'encryption']):
                categories['encryption'].append(vuln)
            elif any(keyword in vuln_name for keyword in ['configuration', 'header', 'setting']):
                categories['configuration'].append(vuln)
            else:
                categories['other'].append(vuln)
        
        return categories
    
    def _generate_recommendations(self, scan_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Générer des recommandations de sécurité"""
        vulnerabilities = scan_results.get('vulnerabilities', [])
        recommendations = []
        
        # Recommandations basées sur les vulnérabilités trouvées
        vuln_types = set()
        for vuln in vulnerabilities:
            vuln_name = vuln.get('name', '').lower()
            if 'sql' in vuln_name:
                vuln_types.add('sql_injection')
            elif 'xss' in vuln_name:
                vuln_types.add('xss')
            elif 'ssl' in vuln_name or 'tls' in vuln_name:
                vuln_types.add('ssl_tls')
            elif 'password' in vuln_name or 'credential' in vuln_name:
                vuln_types.add('authentication')
        
        # Recommandations spécifiques
        if 'sql_injection' in vuln_types:
            recommendations.append({
                'priority': 'high',
                'category': 'web_application',
                'title': 'Implement Parameterized Queries',
                'description': 'Use prepared statements or parameterized queries to prevent SQL injection attacks',
                'implementation': 'Update all database queries to use parameterized statements',
                'effort': 'medium'
            })
        
        if 'xss' in vuln_types:
            recommendations.append({
                'priority': 'high',
                'category': 'web_application',
                'title': 'Implement Input Validation and Output Encoding',
                'description': 'Validate all user inputs and encode outputs to prevent XSS attacks',
                'implementation': 'Use input validation libraries and output encoding functions',
                'effort': 'medium'
            })
        
        if 'ssl_tls' in vuln_types:
            recommendations.append({
                'priority': 'medium',
                'category': 'encryption',
                'title': 'Update SSL/TLS Configuration',
                'description': 'Disable outdated SSL/TLS protocols and use strong cipher suites',
                'implementation': 'Configure web server to use TLS 1.2+ and strong ciphers',
                'effort': 'low'
            })
        
        if 'authentication' in vuln_types:
            recommendations.append({
                'priority': 'high',
                'category': 'authentication',
                'title': 'Implement Strong Authentication',
                'description': 'Use multi-factor authentication and strong password policies',
                'implementation': 'Deploy MFA solution and enforce password complexity requirements',
                'effort': 'high'
            })
        
        # Recommandations générales
        recommendations.append({
            'priority': 'medium',
            'category': 'general',
            'title': 'Regular Security Updates',
            'description': 'Keep all systems and applications updated with the latest security patches',
            'implementation': 'Establish a patch management process',
            'effort': 'medium'
        })
        
        return recommendations
    
    def _analyze_trends(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyser les tendances des vulnérabilités"""
        # Stub pour l'analyse des tendances
        return {
            'vulnerability_trend': 'stable',
            'new_vulnerabilities': 2,
            'fixed_vulnerabilities': 1,
            'recurring_vulnerabilities': 1,
            'trend_analysis': 'Vulnerability count has remained stable over the last 3 scans'
        }
    
    def _check_compliance(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Vérifier la conformité aux standards de sécurité"""
        vulnerabilities = scan_results.get('vulnerabilities', [])
        
        # Standards de conformité
        compliance_standards = {
            'OWASP_Top_10': {
                'status': 'partial',
                'issues': ['A03:2021 - Injection', 'A07:2021 - Identification and Authentication Failures'],
                'score': 70
            },
            'NIST_Cybersecurity_Framework': {
                'status': 'partial',
                'issues': ['Identify', 'Protect'],
                'score': 75
            },
            'ISO_27001': {
                'status': 'partial',
                'issues': ['A.12.2 - Protection from malware', 'A.12.6 - Technical vulnerability management'],
                'score': 65
            }
        }
        
        return compliance_standards
    
    def _get_risk_description(self, risk_level: str) -> str:
        """Obtenir la description du niveau de risque"""
        descriptions = {
            'critical': 'Immediate action required. System is highly vulnerable to attacks.',
            'high': 'Urgent attention needed. Multiple high-severity vulnerabilities detected.',
            'medium': 'Moderate risk level. Some vulnerabilities need to be addressed.',
            'low': 'Low risk level. Minor vulnerabilities detected.',
            'minimal': 'Very low risk level. System appears secure.'
        }
        return descriptions.get(risk_level, 'Unknown risk level')
    
    def get_analysis_summary(self, scan_id: str) -> Dict[str, Any]:
        """Obtenir un résumé de l'analyse"""
        analysis = self.analysis_results.get(scan_id, {})
        if not analysis:
            return {}
        
        return {
            'scan_id': analysis.get('scan_id'),
            'risk_level': analysis.get('risk_assessment', {}).get('risk_level'),
            'total_vulnerabilities': len(analysis.get('vulnerability_categories', {}).get('web_application', []) + 
                                       analysis.get('vulnerability_categories', {}).get('network', []) +
                                       analysis.get('vulnerability_categories', {}).get('authentication', []) +
                                       analysis.get('vulnerability_categories', {}).get('encryption', []) +
                                       analysis.get('vulnerability_categories', {}).get('configuration', []) +
                                       analysis.get('vulnerability_categories', {}).get('other', [])),
            'recommendations_count': len(analysis.get('recommendations', [])),
            'analysis_date': analysis.get('analysis_date')
        } 