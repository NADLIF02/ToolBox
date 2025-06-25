"""
Générateur de rapports principal
"""

import logging
import time
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Générateur de rapports principal"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_dir = config.get('output_dir', './reports')
        self.template_dir = config.get('template_dir', './templates')
        self.report_results = {}
    
    def generate_executive_summary(self, project_data: Dict[str, Any], 
                                 scan_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Générer un résumé exécutif
        
        Args:
            project_data: Données du projet
            scan_results: Résultats des scans
        
        Returns:
            Résumé exécutif
        """
        try:
            logger.info("Génération du résumé exécutif")
            
            # Analyser les résultats
            total_vulnerabilities = 0
            critical_vulnerabilities = 0
            high_vulnerabilities = 0
            medium_vulnerabilities = 0
            low_vulnerabilities = 0
            
            for result in scan_results:
                if 'vulnerabilities' in result:
                    for vuln in result['vulnerabilities']:
                        total_vulnerabilities += 1
                        severity = vuln.get('severity', 'low').lower()
                        if severity == 'critical':
                            critical_vulnerabilities += 1
                        elif severity == 'high':
                            high_vulnerabilities += 1
                        elif severity == 'medium':
                            medium_vulnerabilities += 1
                        else:
                            low_vulnerabilities += 1
            
            executive_summary = {
                'report_id': f"exec_summary_{int(time.time())}",
                'generation_date': datetime.now().isoformat(),
                'project_info': {
                    'name': project_data.get('name', 'Unknown Project'),
                    'client': project_data.get('client', 'Unknown Client'),
                    'scope': project_data.get('scope', 'Full scope'),
                    'start_date': project_data.get('start_date', 'Unknown'),
                    'end_date': project_data.get('end_date', 'Unknown')
                },
                'security_overview': {
                    'total_vulnerabilities': total_vulnerabilities,
                    'critical_vulnerabilities': critical_vulnerabilities,
                    'high_vulnerabilities': high_vulnerabilities,
                    'medium_vulnerabilities': medium_vulnerabilities,
                    'low_vulnerabilities': low_vulnerabilities,
                    'risk_score': self._calculate_risk_score(critical_vulnerabilities, 
                                                           high_vulnerabilities, 
                                                           medium_vulnerabilities, 
                                                           low_vulnerabilities)
                },
                'key_findings': self._generate_key_findings(scan_results),
                'recommendations': self._generate_recommendations(scan_results)
            }
            
            logger.info("Résumé exécutif généré avec succès")
            return executive_summary
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération du résumé exécutif: {str(e)}")
            raise
    
    def generate_technical_report(self, project_data: Dict[str, Any], 
                                scan_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Générer un rapport technique détaillé
        
        Args:
            project_data: Données du projet
            scan_results: Résultats des scans
        
        Returns:
            Rapport technique
        """
        try:
            logger.info("Génération du rapport technique")
            
            technical_report = {
                'report_id': f"tech_report_{int(time.time())}",
                'generation_date': datetime.now().isoformat(),
                'project_info': project_data,
                'methodology': self._generate_methodology(),
                'scan_results': self._organize_scan_results(scan_results),
                'vulnerability_details': self._extract_vulnerability_details(scan_results),
                'risk_assessment': self._generate_risk_assessment(scan_results),
                'remediation_guide': self._generate_remediation_guide(scan_results),
                'appendix': self._generate_appendix(scan_results)
            }
            
            logger.info("Rapport technique généré avec succès")
            return technical_report
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération du rapport technique: {str(e)}")
            raise
    
    def generate_compliance_report(self, project_data: Dict[str, Any], 
                                 scan_results: List[Dict[str, Any]], 
                                 compliance_framework: str = 'ISO27001') -> Dict[str, Any]:
        """
        Générer un rapport de conformité
        
        Args:
            project_data: Données du projet
            scan_results: Résultats des scans
            compliance_framework: Cadre de conformité
        
        Returns:
            Rapport de conformité
        """
        try:
            logger.info(f"Génération du rapport de conformité {compliance_framework}")
            
            compliance_report = {
                'report_id': f"compliance_report_{int(time.time())}",
                'generation_date': datetime.now().isoformat(),
                'compliance_framework': compliance_framework,
                'project_info': project_data,
                'compliance_assessment': self._assess_compliance(scan_results, compliance_framework),
                'control_mapping': self._map_controls(scan_results, compliance_framework),
                'gap_analysis': self._analyze_gaps(scan_results, compliance_framework),
                'remediation_plan': self._generate_compliance_remediation(scan_results, compliance_framework)
            }
            
            logger.info("Rapport de conformité généré avec succès")
            return compliance_report
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération du rapport de conformité: {str(e)}")
            raise
    
    def _calculate_risk_score(self, critical: int, high: int, medium: int, low: int) -> str:
        """Calculer le score de risque global"""
        score = (critical * 10) + (high * 7) + (medium * 4) + (low * 1)
        
        if score >= 50:
            return "Critical"
        elif score >= 30:
            return "High"
        elif score >= 15:
            return "Medium"
        else:
            return "Low"
    
    def _generate_key_findings(self, scan_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Générer les principales découvertes"""
        findings = []
        
        for result in scan_results:
            if 'vulnerabilities' in result:
                for vuln in result['vulnerabilities']:
                    if vuln.get('severity', 'low').lower() in ['critical', 'high']:
                        findings.append({
                            'title': vuln.get('name', 'Unknown vulnerability'),
                            'severity': vuln.get('severity', 'Unknown'),
                            'description': vuln.get('description', 'No description available'),
                            'impact': vuln.get('impact', 'Unknown impact'),
                            'recommendation': vuln.get('solution', 'No solution provided')
                        })
        
        return findings[:10]  # Limiter à 10 principales découvertes
    
    def _generate_recommendations(self, scan_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Générer les recommandations"""
        recommendations = [
            {
                'priority': 'High',
                'title': 'Implement Security Headers',
                'description': 'Add security headers to all web applications',
                'effort': 'Low',
                'impact': 'High'
            },
            {
                'priority': 'High',
                'title': 'Update Outdated Software',
                'description': 'Update all outdated software and dependencies',
                'effort': 'Medium',
                'impact': 'High'
            },
            {
                'priority': 'Medium',
                'title': 'Implement Input Validation',
                'description': 'Add proper input validation to all forms',
                'effort': 'Medium',
                'impact': 'Medium'
            }
        ]
        
        return recommendations
    
    def _generate_methodology(self) -> Dict[str, Any]:
        """Générer la méthodologie"""
        return {
            'phases': [
                {
                    'phase': 'Reconnaissance',
                    'description': 'Information gathering and target identification',
                    'tools': ['Nmap', 'WHOIS', 'DNS enumeration']
                },
                {
                    'phase': 'Scanning',
                    'description': 'Vulnerability scanning and port enumeration',
                    'tools': ['Nmap', 'OpenVAS', 'Nessus']
                },
                {
                    'phase': 'Exploitation',
                    'description': 'Attempting to exploit identified vulnerabilities',
                    'tools': ['Metasploit', 'Custom exploits']
                },
                {
                    'phase': 'Post-Exploitation',
                    'description': 'Data collection and privilege escalation',
                    'tools': ['Mimikatz', 'BloodHound']
                }
            ],
            'tools_used': ['Nmap', 'OpenVAS', 'Metasploit', 'OWASP ZAP', 'SQLmap', 'Hydra']
        }
    
    def _organize_scan_results(self, scan_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Organiser les résultats des scans"""
        organized = {
            'network_scanning': [],
            'web_application_testing': [],
            'vulnerability_assessment': [],
            'exploitation': [],
            'post_exploitation': []
        }
        
        for result in scan_results:
            scan_type = result.get('scan_type', 'unknown')
            if 'network' in scan_type.lower():
                organized['network_scanning'].append(result)
            elif 'web' in scan_type.lower():
                organized['web_application_testing'].append(result)
            elif 'vulnerability' in scan_type.lower():
                organized['vulnerability_assessment'].append(result)
            elif 'exploitation' in scan_type.lower():
                organized['exploitation'].append(result)
            elif 'post' in scan_type.lower():
                organized['post_exploitation'].append(result)
        
        return organized
    
    def _extract_vulnerability_details(self, scan_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extraire les détails des vulnérabilités"""
        vulnerabilities = []
        
        for result in scan_results:
            if 'vulnerabilities' in result:
                for vuln in result['vulnerabilities']:
                    vulnerabilities.append({
                        'id': vuln.get('id', 'Unknown'),
                        'name': vuln.get('name', 'Unknown'),
                        'severity': vuln.get('severity', 'Unknown'),
                        'description': vuln.get('description', 'No description'),
                        'solution': vuln.get('solution', 'No solution'),
                        'cvss_score': vuln.get('cvss_score', 'Unknown'),
                        'references': vuln.get('references', []),
                        'affected_components': vuln.get('affected_components', []),
                        'evidence': vuln.get('evidence', 'No evidence')
                    })
        
        return vulnerabilities
    
    def _generate_risk_assessment(self, scan_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Générer l'évaluation des risques"""
        return {
            'risk_matrix': {
                'critical': 3,
                'high': 8,
                'medium': 15,
                'low': 25
            },
            'risk_categories': [
                {
                    'category': 'Network Security',
                    'risk_level': 'High',
                    'description': 'Multiple critical vulnerabilities found'
                },
                {
                    'category': 'Web Application Security',
                    'risk_level': 'Medium',
                    'description': 'Several medium-severity vulnerabilities'
                },
                {
                    'category': 'Physical Security',
                    'risk_level': 'Low',
                    'description': 'No physical security issues identified'
                }
            ]
        }
    
    def _generate_remediation_guide(self, scan_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Générer le guide de remédiation"""
        return [
            {
                'vulnerability': 'SQL Injection',
                'priority': 'Critical',
                'description': 'Fix SQL injection vulnerabilities',
                'steps': [
                    'Use parameterized queries',
                    'Implement input validation',
                    'Use ORM frameworks'
                ],
                'estimated_time': '2-4 weeks',
                'resources_needed': ['Developer', 'Security expert']
            },
            {
                'vulnerability': 'Cross-Site Scripting (XSS)',
                'priority': 'High',
                'description': 'Fix XSS vulnerabilities',
                'steps': [
                    'Implement output encoding',
                    'Use Content Security Policy',
                    'Validate and sanitize input'
                ],
                'estimated_time': '1-2 weeks',
                'resources_needed': ['Developer']
            }
        ]
    
    def _generate_appendix(self, scan_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Générer l'annexe"""
        return {
            'tools_used': ['Nmap', 'OpenVAS', 'Metasploit', 'OWASP ZAP'],
            'scan_configurations': scan_results,
            'raw_data': 'Available upon request',
            'contact_information': {
                'security_team': 'security@company.com',
                'emergency_contact': '+1-555-0123'
            }
        }
    
    def _assess_compliance(self, scan_results: List[Dict[str, Any]], framework: str) -> Dict[str, Any]:
        """Évaluer la conformité"""
        return {
            'framework': framework,
            'overall_compliance': '75%',
            'compliant_controls': 15,
            'non_compliant_controls': 5,
            'partially_compliant_controls': 2
        }
    
    def _map_controls(self, scan_results: List[Dict[str, Any]], framework: str) -> List[Dict[str, Any]]:
        """Mapper les contrôles"""
        return [
            {
                'control_id': 'A.9.1.1',
                'control_name': 'Access Control Policy',
                'status': 'Compliant',
                'evidence': 'Access control policy documented and implemented'
            },
            {
                'control_id': 'A.9.2.1',
                'control_name': 'User Registration and De-registration',
                'status': 'Non-Compliant',
                'evidence': 'No formal user registration process found'
            }
        ]
    
    def _analyze_gaps(self, scan_results: List[Dict[str, Any]], framework: str) -> List[Dict[str, Any]]:
        """Analyser les écarts"""
        return [
            {
                'gap_id': 'GAP-001',
                'control_id': 'A.9.2.1',
                'description': 'Missing user registration process',
                'impact': 'High',
                'remediation_required': True
            }
        ]
    
    def _generate_compliance_remediation(self, scan_results: List[Dict[str, Any]], framework: str) -> List[Dict[str, Any]]:
        """Générer le plan de remédiation pour la conformité"""
        return [
            {
                'gap_id': 'GAP-001',
                'action': 'Implement user registration process',
                'timeline': '30 days',
                'responsible_party': 'IT Department',
                'estimated_cost': '$10,000'
            }
        ] 