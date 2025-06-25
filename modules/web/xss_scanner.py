"""
Module XSS scanner pour détecter les vulnérabilités XSS
"""

import logging
import time
import requests
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class XSSScanner(ABC):
    """Classe abstraite pour les scanners XSS"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.scan_results = {}
    
    @abstractmethod
    def scan_url(self, url: str, parameters: List[str] = None) -> Dict[str, Any]:
        """Scanner une URL pour des vulnérabilités XSS"""
        pass
    
    @abstractmethod
    def test_parameter(self, url: str, parameter: str, payloads: List[str] = None) -> Dict[str, Any]:
        """Tester un paramètre spécifique pour XSS"""
        pass

class XSSDetector(XSSScanner):
    """Détecteur XSS pour les applications web"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.payloads = config.get('xss_payloads', self._get_default_payloads())
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _get_default_payloads(self) -> List[str]:
        """Obtenir les payloads XSS par défaut"""
        return [
            '<script>alert(1)</script>',
            '"><script>alert(1)</script>',
            'javascript:alert(1)',
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            '"><img src=x onerror=alert(1)>',
            '\'><img src=x onerror=alert(1)>',
            '"><script>alert(String.fromCharCode(88,83,83))</script>',
            '<script>alert(document.cookie)</script>',
            '<script>alert(location.href)</script>'
        ]
    
    def scan_url(self, url: str, parameters: List[str] = None) -> Dict[str, Any]:
        """
        Scanner une URL pour des vulnérabilités XSS
        
        Args:
            url: URL à scanner
            parameters: Liste des paramètres à tester
        
        Returns:
            Résultats du scan
        """
        try:
            logger.info(f"Démarrage du scan XSS sur {url}")
            
            # Stub pour le scan XSS
            scan_id = f"xss_scan_{int(time.time())}"
            
            # Simuler le scan
            time.sleep(3)
            
            results = {
                'scan_id': scan_id,
                'url': url,
                'parameters_tested': parameters or ['q', 'search', 'id', 'name'],
                'status': 'completed',
                'vulnerabilities': self._generate_stub_vulnerabilities(url),
                'xss_found': self._generate_stub_xss_found(url),
                'summary': {
                    'total_xss': 4,
                    'reflected': 2,
                    'stored': 1,
                    'dom_based': 1,
                    'parameters_vulnerable': 3
                },
                'scan_time': 150.8
            }
            
            self.scan_results[scan_id] = results
            logger.info(f"Scan XSS terminé: {results['summary']['total_xss']} vulnérabilités trouvées")
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors du scan XSS: {str(e)}")
            raise
    
    def test_parameter(self, url: str, parameter: str, payloads: List[str] = None) -> Dict[str, Any]:
        """
        Tester un paramètre spécifique pour XSS
        
        Args:
            url: URL à tester
            parameter: Paramètre à tester
            payloads: Liste de payloads personnalisés
        
        Returns:
            Résultats du test
        """
        try:
            logger.info(f"Test XSS du paramètre {parameter} sur {url}")
            
            # Stub pour le test de paramètre
            test_id = f"xss_test_{int(time.time())}"
            
            # Simuler le test
            time.sleep(2)
            
            results = {
                'test_id': test_id,
                'url': url,
                'parameter': parameter,
                'status': 'completed',
                'vulnerable': True,
                'xss_type': 'reflected',
                'payload': '<script>alert(1)</script>',
                'evidence': 'Payload reflected in response',
                'confidence': 'High',
                'details': {
                    'technique': 'Reflected XSS',
                    'title': 'Cross-Site Scripting (XSS)',
                    'description': f'Parameter {parameter} is vulnerable to reflected XSS',
                    'solution': 'Implement proper input validation and output encoding'
                }
            }
            
            logger.info(f"Test XSS terminé: paramètre {parameter} vulnérable")
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors du test XSS: {str(e)}")
            raise
    
    def _generate_stub_vulnerabilities(self, url: str) -> List[Dict[str, Any]]:
        """Générer des vulnérabilités XSS de test"""
        return [
            {
                'id': 'xss-001',
                'name': 'Reflected Cross-Site Scripting (XSS)',
                'severity': 'High',
                'confidence': 'High',
                'url': f'{url}/search.php',
                'parameter': 'q',
                'payload': '<script>alert(1)</script>',
                'evidence': 'Payload reflected in response without encoding',
                'description': 'Reflected XSS vulnerability found in search parameter',
                'solution': 'Implement proper input validation and output encoding',
                'reference': 'https://owasp.org/www-community/attacks/xss/'
            },
            {
                'id': 'xss-002',
                'name': 'Stored Cross-Site Scripting (XSS)',
                'severity': 'Critical',
                'confidence': 'High',
                'url': f'{url}/comment.php',
                'parameter': 'comment',
                'payload': '<script>alert(document.cookie)</script>',
                'evidence': 'Payload stored in database and executed on page load',
                'description': 'Stored XSS vulnerability found in comment system',
                'solution': 'Implement proper input validation and output encoding',
                'reference': 'https://owasp.org/www-community/attacks/xss/'
            },
            {
                'id': 'xss-003',
                'name': 'DOM-based Cross-Site Scripting (XSS)',
                'severity': 'High',
                'confidence': 'Medium',
                'url': f'{url}/user.php',
                'parameter': 'user_id',
                'payload': 'javascript:alert(1)',
                'evidence': 'Payload executed through DOM manipulation',
                'description': 'DOM-based XSS vulnerability found in user profile',
                'solution': 'Implement proper input validation and output encoding',
                'reference': 'https://owasp.org/www-community/attacks/DOM_Based_XSS'
            },
            {
                'id': 'xss-004',
                'name': 'Reflected Cross-Site Scripting (XSS)',
                'severity': 'Medium',
                'confidence': 'Medium',
                'url': f'{url}/product.php',
                'parameter': 'name',
                'payload': '<img src=x onerror=alert(1)>',
                'evidence': 'Image tag with onerror event reflected in response',
                'description': 'Reflected XSS vulnerability found in product name parameter',
                'solution': 'Implement proper input validation and output encoding',
                'reference': 'https://owasp.org/www-community/attacks/xss/'
            }
        ]
    
    def _generate_stub_xss_found(self, url: str) -> List[Dict[str, Any]]:
        """Générer des vulnérabilités XSS trouvées de test"""
        return [
            {
                'id': 'xss-001',
                'name': 'Reflected Cross-Site Scripting (XSS)',
                'severity': 'High',
                'confidence': 'High',
                'url': f'{url}/search.php',
                'parameter': 'q',
                'payload': '<script>alert(1)</script>',
                'evidence': 'Payload reflected in response without encoding',
                'description': 'Reflected XSS vulnerability found in search parameter',
                'solution': 'Implement proper input validation and output encoding',
                'reference': 'https://owasp.org/www-community/attacks/xss/'
            },
            {
                'id': 'xss-002',
                'name': 'Stored Cross-Site Scripting (XSS)',
                'severity': 'Critical',
                'confidence': 'High',
                'url': f'{url}/comment.php',
                'parameter': 'comment',
                'payload': '<script>alert(document.cookie)</script>',
                'evidence': 'Payload stored in database and executed on page load',
                'description': 'Stored XSS vulnerability found in comment system',
                'solution': 'Implement proper input validation and output encoding',
                'reference': 'https://owasp.org/www-community/attacks/xss/'
            },
            {
                'id': 'xss-003',
                'name': 'DOM-based Cross-Site Scripting (XSS)',
                'severity': 'High',
                'confidence': 'Medium',
                'url': f'{url}/user.php',
                'parameter': 'user_id',
                'payload': 'javascript:alert(1)',
                'evidence': 'Payload executed through DOM manipulation',
                'description': 'DOM-based XSS vulnerability found in user profile',
                'solution': 'Implement proper input validation and output encoding',
                'reference': 'https://owasp.org/www-community/attacks/DOM_Based_XSS'
            },
            {
                'id': 'xss-004',
                'name': 'Reflected Cross-Site Scripting (XSS)',
                'severity': 'Medium',
                'confidence': 'Medium',
                'url': f'{url}/product.php',
                'parameter': 'name',
                'payload': '<img src=x onerror=alert(1)>',
                'evidence': 'Image tag with onerror event reflected in response',
                'description': 'Reflected XSS vulnerability found in product name parameter',
                'solution': 'Implement proper input validation and output encoding',
                'reference': 'https://owasp.org/www-community/attacks/xss/'
            }
        ] 