#!/usr/bin/env python3
"""
Script de test pour la toolbox de pentest
Teste tous les modules et génère un rapport de test
"""

import sys
import time
import logging
from datetime import datetime
from typing import Dict, List, Any

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_discovery_module():
    """Tester le module de découverte"""
    logger.info("=== Test du module Discovery ===")
    
    try:
        from modules.discovery.scanner import NmapScanner
        
        config = {
            'nmap_path': 'nmap',
            'output_dir': './output'
        }
        
        scanner = NmapScanner(config)
        
        # Test de scan réseau
        result = scanner.scan_network('192.168.1.0/24', scan_type='quick')
        logger.info(f"Scan réseau terminé: {result['summary']['hosts_found']} hôtes trouvés")
        
        # Test de scan de ports
        result = scanner.scan_ports('192.168.1.1', ports='1-1000')
        logger.info(f"Scan de ports terminé: {result['summary']['open_ports']} ports ouverts")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le module Discovery: {str(e)}")
        return False

def test_vulnscan_module():
    """Tester le module de scan de vulnérabilités"""
    logger.info("=== Test du module VulnScan ===")
    
    try:
        from modules.vulnscan.scanner import OpenVASScanner
        from modules.vulnscan.analyzer import VulnerabilityAnalyzer
        
        config = {
            'openvas_url': 'http://localhost:9392',
            'username': 'admin',
            'password': 'admin'
        }
        
        scanner = OpenVASScanner(config)
        analyzer = VulnerabilityAnalyzer(config)
        
        # Test de scan de vulnérabilités
        result = scanner.scan_target('192.168.1.1', scan_type='full')
        logger.info(f"Scan de vulnérabilités terminé: {result['summary']['total_vulnerabilities']} vulnérabilités trouvées")
        
        # Test d'analyse
        analysis = analyzer.analyze_vulnerabilities(result['vulnerabilities'])
        logger.info(f"Analyse terminée: {analysis['summary']['critical_count']} vulnérabilités critiques")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le module VulnScan: {str(e)}")
        return False

def test_exploitation_module():
    """Tester le module d'exploitation"""
    logger.info("=== Test du module Exploitation ===")
    
    try:
        from modules.exploitation.exploiter import MetasploitExploiter
        from modules.exploitation.post_exploitation import PostExploitation
        
        config = {
            'msf_path': '/usr/share/metasploit-framework',
            'workspace': 'default'
        }
        
        exploiter = MetasploitExploiter(config)
        post_exploit = PostExploitation(config)
        
        # Test d'exploitation
        result = exploiter.exploit_target('192.168.1.1', 'exploit/windows/smb/ms17_010_eternalblue')
        logger.info(f"Exploitation terminée: {result['status']}")
        
        # Test de post-exploitation
        result = post_exploit.collect_data('192.168.1.1')
        logger.info(f"Collecte de données terminée: {result['summary']['files_collected']} fichiers collectés")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le module Exploitation: {str(e)}")
        return False

def test_web_module():
    """Tester le module web"""
    logger.info("=== Test du module Web ===")
    
    try:
        from modules.web.scanner import ZAPScanner
        from modules.web.sql_injection import SQLMapScanner
        from modules.web.xss_scanner import XSSDetector
        
        config = {
            'zap_url': 'http://localhost:8080',
            'zap_api_key': 'stub_key'
        }
        
        zap_scanner = ZAPScanner(config)
        sql_scanner = SQLMapScanner(config)
        xss_scanner = XSSDetector(config)
        
        # Test de scan web
        result = zap_scanner.scan_url('http://example.com', scan_type='full')
        logger.info(f"Scan web terminé: {result['summary']['total_alerts']} alertes trouvées")
        
        # Test de scan SQL injection
        result = sql_scanner.scan_url('http://example.com', parameters=['id', 'user'])
        logger.info(f"Scan SQL injection terminé: {result['summary']['total_injections']} injections trouvées")
        
        # Test de scan XSS
        result = xss_scanner.scan_url('http://example.com', parameters=['q', 'search'])
        logger.info(f"Scan XSS terminé: {result['summary']['total_xss']} vulnérabilités trouvées")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le module Web: {str(e)}")
        return False

def test_bruteforce_module():
    """Tester le module brute force"""
    logger.info("=== Test du module BruteForce ===")
    
    try:
        from modules.bruteforce.hydra_attacker import HydraAttacker
        from modules.bruteforce.ssh_attacker import SSHBruteForcer
        
        config = {
            'hydra_path': 'hydra',
            'wordlists_dir': '/usr/share/wordlists'
        }
        
        hydra = HydraAttacker(config)
        ssh_attacker = SSHBruteForcer(config)
        
        # Test d'attaque SSH
        result = hydra.attack_ssh('192.168.1.1', username='admin')
        logger.info(f"Attaque SSH terminée: {result['summary']['successful_logins']} connexions réussies")
        
        # Test d'attaque SSH spécialisée
        result = ssh_attacker.attack_single_user('192.168.1.1', 'admin', ['password', 'admin123'])
        logger.info(f"Attaque SSH spécialisée terminée: {result['summary']['successful_logins']} connexions réussies")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le module BruteForce: {str(e)}")
        return False

def test_wifi_module():
    """Tester le module WiFi"""
    logger.info("=== Test du module WiFi ===")
    
    try:
        from modules.wifi.scanner import WiFiScanner
        from modules.wifi.cracker import WiFiCracker
        
        config = {
            'wifi_interface': 'wlan0',
            'wordlists_dir': '/usr/share/wordlists'
        }
        
        scanner = WiFiScanner(config)
        cracker = WiFiCracker(config)
        
        # Test de scan WiFi
        result = scanner.scan_networks()
        logger.info(f"Scan WiFi terminé: {result['summary']['total_networks']} réseaux trouvés")
        
        # Test de crackage WiFi
        result = cracker.crack_wpa_handshake('capture.cap', '/usr/share/wordlists/rockyou.txt')
        logger.info(f"Crackage WiFi terminé: {result['status']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le module WiFi: {str(e)}")
        return False

def test_forensics_module():
    """Tester le module forensics"""
    logger.info("=== Test du module Forensics ===")
    
    try:
        from modules.forensics.memory_analyzer import MemoryAnalyzer
        from modules.forensics.network_analyzer import NetworkAnalyzer
        
        config = {
            'volatility_path': 'vol.py',
            'wireshark_path': 'tshark'
        }
        
        memory_analyzer = MemoryAnalyzer(config)
        network_analyzer = NetworkAnalyzer(config)
        
        # Test d'analyse mémoire
        result = memory_analyzer.analyze_processes('memory.dmp')
        logger.info(f"Analyse mémoire terminée: {result['summary']['total_processes']} processus trouvés")
        
        # Test d'analyse réseau
        result = network_analyzer.analyze_pcap('capture.pcap')
        logger.info(f"Analyse réseau terminée: {result['summary']['total_packets']} paquets analysés")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le module Forensics: {str(e)}")
        return False

def test_reporting_module():
    """Tester le module reporting"""
    logger.info("=== Test du module Reporting ===")
    
    try:
        from modules.reporting.report_generator import ReportGenerator
        from modules.reporting.pdf_generator import PDFGenerator
        from modules.reporting.html_generator import HTMLGenerator
        
        config = {
            'output_dir': './reports',
            'template_dir': './templates'
        }
        
        report_gen = ReportGenerator(config)
        pdf_gen = PDFGenerator(config)
        html_gen = HTMLGenerator(config)
        
        # Données de test
        project_data = {
            'name': 'Test Project',
            'client': 'Test Client',
            'scope': 'Full scope',
            'start_date': '2024-01-01',
            'end_date': '2024-01-15'
        }
        
        scan_results = [
            {
                'scan_type': 'network',
                'vulnerabilities': [
                    {
                        'name': 'Test Vulnerability',
                        'severity': 'High',
                        'description': 'Test description'
                    }
                ]
            }
        ]
        
        # Test de génération de rapport
        executive_summary = report_gen.generate_executive_summary(project_data, scan_results)
        logger.info("Résumé exécutif généré")
        
        # Test de génération PDF
        pdf_path = pdf_gen.generate_executive_summary_pdf(executive_summary)
        logger.info(f"PDF généré: {pdf_path}")
        
        # Test de génération HTML
        html_path = html_gen.generate_executive_summary_html(executive_summary)
        logger.info(f"HTML généré: {html_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le module Reporting: {str(e)}")
        return False

def main():
    """Fonction principale de test"""
    logger.info("Démarrage des tests de la toolbox de pentest")
    
    test_results = {}
    
    # Tests des modules
    modules = [
        ('Discovery', test_discovery_module),
        ('VulnScan', test_vulnscan_module),
        ('Exploitation', test_exploitation_module),
        ('Web', test_web_module),
        ('BruteForce', test_bruteforce_module),
        ('WiFi', test_wifi_module),
        ('Forensics', test_forensics_module),
        ('Reporting', test_reporting_module)
    ]
    
    for module_name, test_func in modules:
        try:
            start_time = time.time()
            success = test_func()
            end_time = time.time()
            
            test_results[module_name] = {
                'success': success,
                'duration': end_time - start_time,
                'timestamp': datetime.now().isoformat()
            }
            
            if success:
                logger.info(f"✅ Module {module_name}: SUCCÈS ({end_time - start_time:.2f}s)")
            else:
                logger.error(f"❌ Module {module_name}: ÉCHEC ({end_time - start_time:.2f}s)")
                
        except Exception as e:
            logger.error(f"❌ Module {module_name}: ERREUR - {str(e)}")
            test_results[module_name] = {
                'success': False,
                'error': str(e),
                'duration': 0,
                'timestamp': datetime.now().isoformat()
            }
    
    # Résumé des tests
    logger.info("\n" + "="*50)
    logger.info("RÉSUMÉ DES TESTS")
    logger.info("="*50)
    
    successful_modules = 0
    total_modules = len(modules)
    
    for module_name, result in test_results.items():
        status = "✅ SUCCÈS" if result['success'] else "❌ ÉCHEC"
        duration = f"{result['duration']:.2f}s" if 'duration' in result else "N/A"
        logger.info(f"{module_name:15} | {status:10} | {duration:>8}")
        
        if result['success']:
            successful_modules += 1
    
    logger.info("="*50)
    logger.info(f"Total: {successful_modules}/{total_modules} modules fonctionnels")
    
    if successful_modules == total_modules:
        logger.info("🎉 Tous les modules fonctionnent correctement!")
        return 0
    else:
        logger.warning(f"⚠️  {total_modules - successful_modules} module(s) en échec")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 