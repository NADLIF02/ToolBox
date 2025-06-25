"""
Module de scan réseau pour la découverte d'hôtes et de services
"""

import nmap
import subprocess
import json
import logging
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import ipaddress

logger = logging.getLogger(__name__)

class NetworkScanner:
    """Scanner réseau pour découvrir les hôtes actifs"""
    
    def __init__(self):
        self.nm = nmap.PortScanner()
        self.results = {}
    
    def scan_network(self, network: str, scan_type: str = 'ping') -> Dict[str, Any]:
        """
        Scanner un réseau pour découvrir les hôtes actifs
        
        Args:
            network: Plage réseau (ex: 192.168.1.0/24)
            scan_type: Type de scan (ping, tcp, udp)
        
        Returns:
            Dictionnaire avec les résultats du scan
        """
        try:
            logger.info(f"Démarrage du scan réseau: {network}")
            
            # Configuration du scan selon le type
            if scan_type == 'ping':
                arguments = '-sn'  # Scan ping
            elif scan_type == 'tcp':
                arguments = '-sS -T4'  # Scan TCP SYN
            elif scan_type == 'udp':
                arguments = '-sU -T4'  # Scan UDP
            else:
                arguments = '-sn'
            
            # Exécuter le scan
            self.nm.scan(hosts=network, arguments=arguments)
            
            # Traiter les résultats
            results = {
                'network': network,
                'scan_type': scan_type,
                'hosts': [],
                'summary': {
                    'total_hosts': 0,
                    'up_hosts': 0,
                    'down_hosts': 0
                }
            }
            
            for host in self.nm.all_hosts():
                host_info = self.nm[host]
                
                if host_info.state() == 'up':
                    results['summary']['up_hosts'] += 1
                    host_data = {
                        'ip': host,
                        'state': host_info.state(),
                        'hostname': host_info.hostname() if 'hostname' in host_info else None,
                        'mac_address': None,
                        'vendor': None
                    }
                    
                    # Extraire les informations supplémentaires
                    if 'addresses' in host_info:
                        addresses = host_info['addresses']
                        if 'mac' in addresses:
                            host_data['mac_address'] = addresses['mac']
                        if 'vendor' in addresses:
                            host_data['vendor'] = addresses['vendor']
                    
                    results['hosts'].append(host_data)
                else:
                    results['summary']['down_hosts'] += 1
                
                results['summary']['total_hosts'] += 1
            
            self.results = results
            logger.info(f"Scan réseau terminé: {results['summary']['up_hosts']} hôtes actifs trouvés")
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors du scan réseau: {str(e)}")
            raise
    
    def scan_hosts(self, hosts: List[str], ports: str = '1-1000') -> Dict[str, Any]:
        """
        Scanner des hôtes spécifiques pour les ports ouverts
        
        Args:
            hosts: Liste des hôtes à scanner
            ports: Plage de ports à scanner
        
        Returns:
            Dictionnaire avec les résultats du scan
        """
        try:
            logger.info(f"Démarrage du scan de ports sur {len(hosts)} hôtes")
            
            results = {
                'hosts': [],
                'summary': {
                    'total_hosts': len(hosts),
                    'scanned_hosts': 0,
                    'open_ports_found': 0
                }
            }
            
            for host in hosts:
                try:
                    # Scan de ports sur l'hôte
                    self.nm.scan(host, ports, arguments='-sS -T4 --version-intensity 5')
                    
                    host_info = self.nm[host]
                    host_data = {
                        'ip': host,
                        'state': host_info.state(),
                        'ports': []
                    }
                    
                    if 'tcp' in host_info:
                        for port, port_info in host_info['tcp'].items():
                            if port_info['state'] == 'open':
                                results['summary']['open_ports_found'] += 1
                                port_data = {
                                    'port': port,
                                    'state': port_info['state'],
                                    'service': port_info.get('name', 'unknown'),
                                    'version': port_info.get('version', ''),
                                    'product': port_info.get('product', ''),
                                    'extrainfo': port_info.get('extrainfo', '')
                                }
                                host_data['ports'].append(port_data)
                    
                    results['hosts'].append(host_data)
                    results['summary']['scanned_hosts'] += 1
                    
                except Exception as e:
                    logger.error(f"Erreur lors du scan de l'hôte {host}: {str(e)}")
                    continue
            
            logger.info(f"Scan de ports terminé: {results['summary']['open_ports_found']} ports ouverts trouvés")
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors du scan de ports: {str(e)}")
            raise

class PortScanner:
    """Scanner de ports spécialisé"""
    
    def __init__(self):
        self.nm = nmap.PortScanner()
    
    def scan_common_ports(self, target: str) -> Dict[str, Any]:
        """
        Scanner les ports communs sur une cible
        
        Args:
            target: Cible à scanner (IP ou domaine)
        
        Returns:
            Résultats du scan
        """
        common_ports = '21,22,23,25,53,80,110,111,135,139,143,443,993,995,1723,3306,3389,5900,8080'
        
        try:
            logger.info(f"Scan des ports communs sur {target}")
            
            self.nm.scan(target, common_ports, arguments='-sS -T4 --version-intensity 3')
            
            results = {
                'target': target,
                'ports': [],
                'summary': {
                    'total_ports': len(common_ports.split(',')),
                    'open_ports': 0,
                    'filtered_ports': 0,
                    'closed_ports': 0
                }
            }
            
            if target in self.nm.all_hosts():
                host_info = self.nm[target]
                
                if 'tcp' in host_info:
                    for port, port_info in host_info['tcp'].items():
                        port_data = {
                            'port': port,
                            'state': port_info['state'],
                            'service': port_info.get('name', 'unknown'),
                            'version': port_info.get('version', ''),
                            'product': port_info.get('product', ''),
                            'extrainfo': port_info.get('extrainfo', '')
                        }
                        
                        results['ports'].append(port_data)
                        
                        if port_info['state'] == 'open':
                            results['summary']['open_ports'] += 1
                        elif port_info['state'] == 'filtered':
                            results['summary']['filtered_ports'] += 1
                        else:
                            results['summary']['closed_ports'] += 1
            
            logger.info(f"Scan des ports communs terminé: {results['summary']['open_ports']} ports ouverts")
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors du scan des ports communs: {str(e)}")
            raise
    
    def scan_port_range(self, target: str, start_port: int, end_port: int) -> Dict[str, Any]:
        """
        Scanner une plage de ports spécifique
        
        Args:
            target: Cible à scanner
            start_port: Port de début
            end_port: Port de fin
        
        Returns:
            Résultats du scan
        """
        port_range = f"{start_port}-{end_port}"
        
        try:
            logger.info(f"Scan de la plage {port_range} sur {target}")
            
            self.nm.scan(target, port_range, arguments='-sS -T4')
            
            results = {
                'target': target,
                'port_range': port_range,
                'ports': [],
                'summary': {
                    'total_ports': end_port - start_port + 1,
                    'open_ports': 0,
                    'filtered_ports': 0,
                    'closed_ports': 0
                }
            }
            
            if target in self.nm.all_hosts():
                host_info = self.nm[target]
                
                if 'tcp' in host_info:
                    for port, port_info in host_info['tcp'].items():
                        port_data = {
                            'port': port,
                            'state': port_info['state'],
                            'service': port_info.get('name', 'unknown'),
                            'version': port_info.get('version', ''),
                            'product': port_info.get('product', ''),
                            'extrainfo': port_info.get('extrainfo', '')
                        }
                        
                        results['ports'].append(port_data)
                        
                        if port_info['state'] == 'open':
                            results['summary']['open_ports'] += 1
                        elif port_info['state'] == 'filtered':
                            results['summary']['filtered_ports'] += 1
                        else:
                            results['summary']['closed_ports'] += 1
            
            logger.info(f"Scan de plage terminé: {results['summary']['open_ports']} ports ouverts")
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors du scan de plage: {str(e)}")
            raise

class ServiceScanner:
    """Scanner de services pour identifier les applications"""
    
    def __init__(self):
        self.nm = nmap.PortScanner()
    
    def identify_services(self, target: str, ports: str = None) -> Dict[str, Any]:
        """
        Identifier les services sur une cible
        
        Args:
            target: Cible à scanner
            ports: Ports à scanner (optionnel)
        
        Returns:
            Résultats de l'identification
        """
        try:
            logger.info(f"Identification des services sur {target}")
            
            # Arguments pour l'identification de services
            arguments = '-sS -sV -O --version-intensity 5'
            if ports:
                scan_target = f"{target}:{ports}"
            else:
                scan_target = target
            
            self.nm.scan(scan_target, arguments=arguments)
            
            results = {
                'target': target,
                'services': [],
                'os_info': {},
                'summary': {
                    'total_services': 0,
                    'identified_services': 0
                }
            }
            
            if target in self.nm.all_hosts():
                host_info = self.nm[target]
                
                # Informations sur le système d'exploitation
                if 'osmatch' in host_info:
                    results['os_info'] = {
                        'matches': host_info['osmatch'],
                        'accuracy': host_info.get('osaccuracy', '')
                    }
                
                # Services identifiés
                if 'tcp' in host_info:
                    for port, port_info in host_info['tcp'].items():
                        if port_info['state'] == 'open':
                            service_data = {
                                'port': port,
                                'service': port_info.get('name', 'unknown'),
                                'product': port_info.get('product', ''),
                                'version': port_info.get('version', ''),
                                'extrainfo': port_info.get('extrainfo', ''),
                                'conf': port_info.get('conf', ''),
                                'cpe': port_info.get('cpe', '')
                            }
                            
                            results['services'].append(service_data)
                            results['summary']['total_services'] += 1
                            
                            if service_data['product'] or service_data['version']:
                                results['summary']['identified_services'] += 1
            
            logger.info(f"Identification des services terminée: {results['summary']['identified_services']} services identifiés")
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors de l'identification des services: {str(e)}")
            raise 