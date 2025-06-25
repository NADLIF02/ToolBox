#!/usr/bin/env python3
"""
Script de démarrage de la toolbox de pentest
Interface en ligne de commande pour utiliser tous les modules
"""

import sys
import argparse
import logging
from typing import Dict, Any

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_discovery(args):
    """Exécuter le module de découverte"""
    logger.info("Démarrage du module Discovery")
    
    try:
        from modules.discovery.scanner import NmapScanner
        
        config = {
            'nmap_path': args.nmap_path,
            'output_dir': args.output_dir
        }
        
        scanner = NmapScanner(config)
        
        if args.scan_type == 'network':
            result = scanner.scan_network(args.target, scan_type=args.scan_mode)
            logger.info(f"Scan réseau terminé: {result['summary']['hosts_found']} hôtes trouvés")
        elif args.scan_type == 'ports':
            result = scanner.scan_ports(args.target, ports=args.ports)
            logger.info(f"Scan de ports terminé: {result['summary']['open_ports']} ports ouverts")
        else:
            logger.error("Type de scan non reconnu")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le module Discovery: {str(e)}")
        return False

def run_vulnscan(args):
    """Exécuter le module de scan de vulnérabilités"""
    logger.info("Démarrage du module VulnScan")
    
    try:
        from modules.vulnscan.scanner import OpenVASScanner
        
        config = {
            'openvas_url': args.openvas_url,
            'username': args.username,
            'password': args.password
        }
        
        scanner = OpenVASScanner(config)
        result = scanner.scan_target(args.target, scan_type=args.scan_type)
        logger.info(f"Scan de vulnérabilités terminé: {result['summary']['total_vulnerabilities']} vulnérabilités trouvées")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le module VulnScan: {str(e)}")
        return False

def run_web_scan(args):
    """Exécuter le module de scan web"""
    logger.info("Démarrage du module Web")
    
    try:
        from modules.web.scanner import ZAPScanner
        
        config = {
            'zap_url': args.zap_url,
            'zap_api_key': args.zap_api_key
        }
        
        scanner = ZAPScanner(config)
        result = scanner.scan_url(args.url, scan_type=args.scan_type)
        logger.info(f"Scan web terminé: {result['summary']['total_alerts']} alertes trouvées")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le module Web: {str(e)}")
        return False

def run_bruteforce(args):
    """Exécuter le module brute force"""
    logger.info("Démarrage du module BruteForce")
    
    try:
        from modules.bruteforce.hydra_attacker import HydraAttacker
        
        config = {
            'hydra_path': args.hydra_path,
            'wordlists_dir': args.wordlists_dir
        }
        
        attacker = HydraAttacker(config)
        
        if args.service == 'ssh':
            result = attacker.attack_ssh(args.target, username=args.username)
        elif args.service == 'ftp':
            result = attacker.attack_ftp(args.target, username=args.username)
        else:
            logger.error("Service non supporté")
            return False
        
        logger.info(f"Attaque terminée: {result['summary']['successful_logins']} connexions réussies")
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le module BruteForce: {str(e)}")
        return False

def run_wifi_scan(args):
    """Exécuter le module WiFi"""
    logger.info("Démarrage du module WiFi")
    
    try:
        from modules.wifi.scanner import WiFiScanner
        
        config = {
            'wifi_interface': args.interface
        }
        
        scanner = WiFiScanner(config)
        result = scanner.scan_networks(interface=args.interface)
        logger.info(f"Scan WiFi terminé: {result['summary']['total_networks']} réseaux trouvés")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le module WiFi: {str(e)}")
        return False

def run_reporting(args):
    """Exécuter le module reporting"""
    logger.info("Démarrage du module Reporting")
    
    try:
        from modules.reporting.report_generator import ReportGenerator
        from modules.reporting.pdf_generator import PDFGenerator
        
        config = {
            'output_dir': args.output_dir,
            'template_dir': args.template_dir
        }
        
        report_gen = ReportGenerator(config)
        pdf_gen = PDFGenerator(config)
        
        # Données de test pour la démonstration
        project_data = {
            'name': args.project_name,
            'client': args.client,
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
        
        # Générer le rapport
        executive_summary = report_gen.generate_executive_summary(project_data, scan_results)
        
        if args.format == 'pdf':
            pdf_path = pdf_gen.generate_executive_summary_pdf(executive_summary)
            logger.info(f"Rapport PDF généré: {pdf_path}")
        else:
            logger.info("Rapport généré en format JSON")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le module Reporting: {str(e)}")
        return False

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description='Toolbox de pentest - Interface en ligne de commande',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python run_toolbox.py discovery --scan-type network --target 192.168.1.0/24
  python run_toolbox.py vulnscan --target 192.168.1.1 --scan-type full
  python run_toolbox.py web --url http://example.com --scan-type full
  python run_toolbox.py bruteforce --service ssh --target 192.168.1.1 --username admin
  python run_toolbox.py wifi --interface wlan0
  python run_toolbox.py reporting --project-name "Test Project" --client "Test Client" --format pdf
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')
    
    # Parser pour Discovery
    discovery_parser = subparsers.add_parser('discovery', help='Module de découverte')
    discovery_parser.add_argument('--scan-type', choices=['network', 'ports'], required=True,
                                 help='Type de scan')
    discovery_parser.add_argument('--target', required=True, help='Cible à scanner')
    discovery_parser.add_argument('--scan-mode', default='quick', choices=['quick', 'full'],
                                 help='Mode de scan')
    discovery_parser.add_argument('--ports', help='Ports à scanner (pour scan de ports)')
    discovery_parser.add_argument('--nmap-path', default='nmap', help='Chemin vers nmap')
    discovery_parser.add_argument('--output-dir', default='./output', help='Répertoire de sortie')
    
    # Parser pour VulnScan
    vulnscan_parser = subparsers.add_parser('vulnscan', help='Module de scan de vulnérabilités')
    vulnscan_parser.add_argument('--target', required=True, help='Cible à scanner')
    vulnscan_parser.add_argument('--scan-type', default='full', choices=['quick', 'full'],
                                help='Type de scan')
    vulnscan_parser.add_argument('--openvas-url', default='http://localhost:9392',
                                help='URL d\'OpenVAS')
    vulnscan_parser.add_argument('--username', default='admin', help='Nom d\'utilisateur')
    vulnscan_parser.add_argument('--password', default='admin', help='Mot de passe')
    
    # Parser pour Web
    web_parser = subparsers.add_parser('web', help='Module de scan web')
    web_parser.add_argument('--url', required=True, help='URL à scanner')
    web_parser.add_argument('--scan-type', default='full', choices=['quick', 'full'],
                           help='Type de scan')
    web_parser.add_argument('--zap-url', default='http://localhost:8080',
                           help='URL de ZAP')
    web_parser.add_argument('--zap-api-key', default='stub_key', help='Clé API ZAP')
    
    # Parser pour BruteForce
    bruteforce_parser = subparsers.add_parser('bruteforce', help='Module brute force')
    bruteforce_parser.add_argument('--service', required=True, choices=['ssh', 'ftp'],
                                  help='Service à attaquer')
    bruteforce_parser.add_argument('--target', required=True, help='Cible à attaquer')
    bruteforce_parser.add_argument('--username', help='Nom d\'utilisateur')
    bruteforce_parser.add_argument('--hydra-path', default='hydra', help='Chemin vers hydra')
    bruteforce_parser.add_argument('--wordlists-dir', default='/usr/share/wordlists',
                                  help='Répertoire des wordlists')
    
    # Parser pour WiFi
    wifi_parser = subparsers.add_parser('wifi', help='Module WiFi')
    wifi_parser.add_argument('--interface', default='wlan0', help='Interface WiFi')
    
    # Parser pour Reporting
    reporting_parser = subparsers.add_parser('reporting', help='Module de reporting')
    reporting_parser.add_argument('--project-name', required=True, help='Nom du projet')
    reporting_parser.add_argument('--client', required=True, help='Nom du client')
    reporting_parser.add_argument('--format', default='json', choices=['json', 'pdf'],
                                 help='Format du rapport')
    reporting_parser.add_argument('--output-dir', default='./reports',
                                 help='Répertoire de sortie')
    reporting_parser.add_argument('--template-dir', default='./templates',
                                 help='Répertoire des templates')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Exécuter la commande appropriée
    success = False
    
    if args.command == 'discovery':
        success = run_discovery(args)
    elif args.command == 'vulnscan':
        success = run_vulnscan(args)
    elif args.command == 'web':
        success = run_web_scan(args)
    elif args.command == 'bruteforce':
        success = run_bruteforce(args)
    elif args.command == 'wifi':
        success = run_wifi_scan(args)
    elif args.command == 'reporting':
        success = run_reporting(args)
    
    if success:
        logger.info("✅ Commande exécutée avec succès")
        return 0
    else:
        logger.error("❌ Erreur lors de l'exécution de la commande")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 