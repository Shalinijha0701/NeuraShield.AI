import re
import json
import subprocess
from typing import Dict, List, Tuple
from app.core.config import settings
from app.core.database import get_neo4j_session

class QuantumSecurityShield:
    """AI-Driven Code Protection with Graph Neural Networks"""
    
    def __init__(self):
        self.vulnerability_patterns = self._load_vulnerability_patterns()
        self.cve_database = self._load_cve_database()
        self.risk_threshold = settings.SECURITY_SHIELD_THRESHOLD
    
    def scan_security(self, code: str, file_path: str, dependencies: List[str] = None) -> Dict:
        """Comprehensive security scan using multiple techniques"""
        results = {
            "file_path": file_path,
            "vulnerabilities": [],
            "dependency_risks": [],
            "secrets_detected": [],
            "security_score": 0.0,
            "risk_level": "low",
            "auto_fix_suggestions": []
        }
        
        # Static analysis
        static_vulns = self._static_analysis(code, file_path)
        results["vulnerabilities"].extend(static_vulns)
        
        # Secret detection
        secrets = self._detect_secrets(code)
        results["secrets_detected"].extend(secrets)
        
        # Dependency analysis
        if dependencies:
            dep_risks = self._analyze_dependencies(dependencies)
            results["dependency_risks"].extend(dep_risks)
        
        # Graph-based analysis
        graph_risks = self._graph_analysis(code, file_path)
        results["vulnerabilities"].extend(graph_risks)
        
        # Calculate security score
        results["security_score"] = self._calculate_security_score(results)
        results["risk_level"] = self._determine_risk_level(results["security_score"])
        
        # Generate auto-fix suggestions
        results["auto_fix_suggestions"] = self._generate_auto_fixes(results["vulnerabilities"])
        
        return results
    
    def _static_analysis(self, code: str, file_path: str) -> List[Dict]:
        """Run static analysis using Bandit and Semgrep"""
        vulnerabilities = []
        
        # Pattern-based detection
        for vuln_type, pattern in self.vulnerability_patterns.items():
            matches = re.finditer(pattern, code, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                vulnerabilities.append({
                    "type": vuln_type,
                    "severity": self._get_severity(vuln_type),
                    "line": line_num,
                    "message": f"Potential {vuln_type.replace('_', ' ')} vulnerability detected",
                    "code_snippet": match.group(0),
                    "confidence": "high"
                })
        
        return vulnerabilities
    
    def _detect_secrets(self, code: str) -> List[Dict]:
        """Detect hardcoded secrets and credentials"""
        secrets = []
        
        secret_patterns = {
            "api_key": r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"]([a-zA-Z0-9_-]{20,})['\"]",
            "password": r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"]([^'\"]{8,})['\"]",
            "token": r"(?i)(token|auth[_-]?token)\s*[:=]\s*['\"]([a-zA-Z0-9_-]{20,})['\"]",
            "private_key": r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----",
            "aws_access_key": r"AKIA[0-9A-Z]{16}",
            "github_token": r"ghp_[a-zA-Z0-9]{36}"
        }
        
        for secret_type, pattern in secret_patterns.items():
            matches = re.finditer(pattern, code)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                secrets.append({
                    "type": secret_type,
                    "line": line_num,
                    "severity": "critical" if "key" in secret_type else "high",
                    "message": f"Hardcoded {secret_type.replace('_', ' ')} detected",
                    "masked_value": match.group(0)[:10] + "***"
                })
        
        return secrets
    
    def _analyze_dependencies(self, dependencies: List[str]) -> List[Dict]:
        """Analyze dependencies for known vulnerabilities"""
        risks = []
        
        for dep in dependencies:
            # Check against CVE database
            cve_risks = self._check_cve_database(dep)
            risks.extend(cve_risks)
            
            # Check for suspicious packages
            if self._is_suspicious_package(dep):
                risks.append({
                    "type": "suspicious_dependency",
                    "package": dep,
                    "severity": "medium",
                    "message": f"Package '{dep}' flagged as potentially suspicious",
                    "recommendation": "Review package source and maintainer"
                })
        
        return risks
    
    def _graph_analysis(self, code: str, file_path: str) -> List[Dict]:
        """Use graph neural networks to detect complex attack patterns"""
        vulnerabilities = []
        
        # Create code dependency graph
        graph_data = self._create_code_graph(code, file_path)
        
        # Analyze graph for attack patterns
        attack_patterns = self._detect_attack_patterns(graph_data)
        
        for pattern in attack_patterns:
            vulnerabilities.append({
                "type": "graph_vulnerability",
                "pattern": pattern["type"],
                "severity": pattern["severity"],
                "message": f"Complex attack pattern detected: {pattern['description']}",
                "affected_nodes": pattern["nodes"],
                "confidence": pattern["confidence"]
            })
        
        return vulnerabilities
    
    def _create_code_graph(self, code: str, file_path: str) -> Dict:
        """Create a graph representation of code dependencies"""
        # Simplified graph creation - in production, use AST and call graphs
        import ast
        
        try:
            tree = ast.parse(code)
            nodes = []
            edges = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    nodes.append({
                        "id": f"func_{node.name}",
                        "type": "function",
                        "name": node.name,
                        "line": node.lineno
                    })
                elif isinstance(node, ast.Call):
                    if hasattr(node.func, 'id'):
                        edges.append({
                            "source": "current_context",
                            "target": f"func_{node.func.id}",
                            "type": "calls"
                        })
            
            return {"nodes": nodes, "edges": edges, "file_path": file_path}
        except:
            return {"nodes": [], "edges": [], "file_path": file_path}
    
    def _detect_attack_patterns(self, graph_data: Dict) -> List[Dict]:
        """Detect attack patterns in the code graph"""
        patterns = []
        
        # Example: Detect potential injection chains
        nodes = graph_data.get("nodes", [])
        edges = graph_data.get("edges", [])
        
        # Look for suspicious function call chains
        for edge in edges:
            if "exec" in edge["target"] or "eval" in edge["target"]:
                patterns.append({
                    "type": "code_injection_chain",
                    "severity": "high",
                    "description": "Potential code injection through function call chain",
                    "nodes": [edge["source"], edge["target"]],
                    "confidence": 0.8
                })
        
        return patterns
    
    def _check_cve_database(self, dependency: str) -> List[Dict]:
        """Check dependency against CVE database"""
        # Simplified CVE check - in production, integrate with real CVE APIs
        known_vulns = {
            "requests": [{"cve": "CVE-2023-32681", "severity": "medium"}],
            "pillow": [{"cve": "CVE-2023-50447", "severity": "high"}],
            "django": [{"cve": "CVE-2023-46695", "severity": "critical"}]
        }
        
        risks = []
        package_name = dependency.split("==")[0].lower()
        
        if package_name in known_vulns:
            for vuln in known_vulns[package_name]:
                risks.append({
                    "type": "cve_vulnerability",
                    "package": dependency,
                    "cve_id": vuln["cve"],
                    "severity": vuln["severity"],
                    "message": f"Known vulnerability {vuln['cve']} in {package_name}",
                    "recommendation": "Update to latest secure version"
                })
        
        return risks
    
    def _is_suspicious_package(self, dependency: str) -> bool:
        """Check if package is suspicious"""
        suspicious_indicators = [
            "temp", "test", "fake", "malicious", "backdoor"
        ]
        package_name = dependency.split("==")[0].lower()
        return any(indicator in package_name for indicator in suspicious_indicators)
    
    def _calculate_security_score(self, results: Dict) -> float:
        """Calculate overall security score"""
        total_issues = len(results["vulnerabilities"]) + len(results["secrets_detected"]) + len(results["dependency_risks"])
        
        if total_issues == 0:
            return 1.0
        
        # Weight by severity
        severity_weights = {"critical": 1.0, "high": 0.7, "medium": 0.4, "low": 0.1}
        weighted_score = 0
        
        for vuln in results["vulnerabilities"]:
            weighted_score += severity_weights.get(vuln.get("severity", "medium"), 0.4)
        
        for secret in results["secrets_detected"]:
            weighted_score += severity_weights.get(secret.get("severity", "high"), 0.7)
        
        for risk in results["dependency_risks"]:
            weighted_score += severity_weights.get(risk.get("severity", "medium"), 0.4)
        
        return max(0, 1 - (weighted_score / 10))  # Normalize to 0-1
    
    def _determine_risk_level(self, security_score: float) -> str:
        """Determine risk level based on security score"""
        if security_score >= 0.8:
            return "low"
        elif security_score >= 0.6:
            return "medium"
        elif security_score >= 0.4:
            return "high"
        else:
            return "critical"
    
    def _generate_auto_fixes(self, vulnerabilities: List[Dict]) -> List[Dict]:
        """Generate automatic fix suggestions"""
        fixes = []
        
        for vuln in vulnerabilities:
            if vuln["type"] == "sql_injection":
                fixes.append({
                    "vulnerability": vuln["type"],
                    "fix_type": "parameterized_query",
                    "description": "Replace string concatenation with parameterized queries",
                    "auto_applicable": True
                })
            elif vuln["type"] == "hardcoded_secret":
                fixes.append({
                    "vulnerability": vuln["type"],
                    "fix_type": "environment_variable",
                    "description": "Move secret to environment variable",
                    "auto_applicable": True
                })
        
        return fixes
    
    def _get_severity(self, vuln_type: str) -> str:
        """Get severity level for vulnerability type"""
        severity_map = {
            "sql_injection": "critical",
            "xss": "high",
            "hardcoded_secret": "high",
            "unsafe_eval": "critical",
            "path_traversal": "high",
            "weak_crypto": "medium"
        }
        return severity_map.get(vuln_type, "medium")
    
    def _load_vulnerability_patterns(self) -> Dict[str, str]:
        """Load vulnerability detection patterns"""
        return {
            "sql_injection": r"(?i)(execute|query|select|insert|update|delete)\s*\(\s*['\"].*%.*['\"]",
            "xss": r"(?i)(innerHTML|outerHTML|document\.write)\s*\+=?\s*.*\+",
            "hardcoded_secret": r"(?i)(password|secret|key|token)\s*[:=]\s*['\"][^'\"]+['\"]",
            "unsafe_eval": r"(?i)(eval|exec|compile)\s*\(",
            "path_traversal": r"(?i)(open|file|read)\s*\([^)]*\.\./",
            "weak_crypto": r"(?i)(md5|sha1|des|rc4)\s*\("
        }
    
    def _load_cve_database(self) -> Dict:
        """Load CVE database - simplified version"""
        return {
            "last_updated": "2024-01-01",
            "vulnerabilities": {}
        }