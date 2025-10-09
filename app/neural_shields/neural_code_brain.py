import ast
import torch
from transformers import AutoTokenizer, AutoModel
from typing import Dict, List, Tuple
from app.core.config import settings

class NeuralCodeBrain:
    """AI Code Reviewer + Bug Predictor"""
    
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(settings.CODE_BRAIN_MODEL)
        self.model = AutoModel.from_pretrained(settings.CODE_BRAIN_MODEL)
        self.bug_patterns = self._load_bug_patterns()
    
    def analyze_code(self, code: str, file_path: str) -> Dict:
        """Analyze code for bugs, quality issues, and style violations"""
        try:
            # Parse AST
            tree = ast.parse(code)
            
            # Get code embeddings
            embeddings = self._get_code_embeddings(code)
            
            # Predict bug probability
            bug_probability = self._predict_bugs(tree, embeddings)
            
            # Analyze code quality
            quality_score = self._analyze_quality(tree, code)
            
            # Check for common patterns
            pattern_issues = self._check_patterns(tree)
            
            return {
                "file_path": file_path,
                "bug_probability": bug_probability,
                "quality_score": quality_score,
                "issues": pattern_issues,
                "suggestions": self._generate_suggestions(pattern_issues),
                "trust_score": self._calculate_trust_score(bug_probability, quality_score)
            }
        except SyntaxError as e:
            return {
                "file_path": file_path,
                "error": f"Syntax error: {str(e)}",
                "bug_probability": 1.0,
                "quality_score": 0.0,
                "trust_score": 0.0
            }
    
    def _get_code_embeddings(self, code: str) -> torch.Tensor:
        """Generate code embeddings using CodeBERT"""
        inputs = self.tokenizer(code, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)
    
    def _predict_bugs(self, tree: ast.AST, embeddings: torch.Tensor) -> float:
        """Predict probability of bugs in the code"""
        risk_factors = 0
        total_checks = 0
        
        for node in ast.walk(tree):
            total_checks += 1
            
            # Check for risky patterns
            if isinstance(node, ast.FunctionDef):
                if len(node.args.args) > 7:  # Too many parameters
                    risk_factors += 1
                if len([n for n in ast.walk(node) if isinstance(n, ast.Return)]) > 5:  # Multiple returns
                    risk_factors += 1
            
            elif isinstance(node, ast.Try):
                if not node.handlers:  # Try without except
                    risk_factors += 2
            
            elif isinstance(node, ast.While):
                # Check for potential infinite loops
                has_break = any(isinstance(n, ast.Break) for n in ast.walk(node))
                if not has_break:
                    risk_factors += 1
        
        return min(risk_factors / max(total_checks * 0.1, 1), 1.0)
    
    def _analyze_quality(self, tree: ast.AST, code: str) -> float:
        """Analyze code quality metrics"""
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Basic metrics
        complexity_score = self._calculate_complexity(tree)
        readability_score = self._calculate_readability(lines)
        documentation_score = self._calculate_documentation(tree, lines)
        
        return (complexity_score + readability_score + documentation_score) / 3
    
    def _calculate_complexity(self, tree: ast.AST) -> float:
        """Calculate cyclomatic complexity"""
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
        return max(0, 1 - (complexity - 10) / 20)  # Normalize to 0-1
    
    def _calculate_readability(self, lines: List[str]) -> float:
        """Calculate readability score"""
        if not lines:
            return 0.0
        
        avg_line_length = sum(len(line) for line in lines) / len(lines)
        long_lines = sum(1 for line in lines if len(line) > 100)
        
        readability = 1.0 - (long_lines / len(lines)) - max(0, (avg_line_length - 80) / 200)
        return max(0, readability)
    
    def _calculate_documentation(self, tree: ast.AST, lines: List[str]) -> float:
        """Calculate documentation score"""
        docstrings = 0
        functions = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                functions += 1
                if (ast.get_docstring(node)):
                    docstrings += 1
        
        if functions == 0:
            return 1.0
        
        return docstrings / functions
    
    def _check_patterns(self, tree: ast.AST) -> List[Dict]:
        """Check for common anti-patterns"""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check for too many parameters
                if len(node.args.args) > 5:
                    issues.append({
                        "type": "complexity",
                        "message": f"Function '{node.name}' has too many parameters ({len(node.args.args)})",
                        "line": node.lineno,
                        "severity": "medium"
                    })
                
                # Check for missing docstring
                if not ast.get_docstring(node):
                    issues.append({
                        "type": "documentation",
                        "message": f"Function '{node.name}' missing docstring",
                        "line": node.lineno,
                        "severity": "low"
                    })
        
        return issues
    
    def _generate_suggestions(self, issues: List[Dict]) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        for issue in issues:
            if issue["type"] == "complexity":
                suggestions.append("Consider breaking down complex functions into smaller ones")
            elif issue["type"] == "documentation":
                suggestions.append("Add docstrings to improve code documentation")
        
        return list(set(suggestions))  # Remove duplicates
    
    def _calculate_trust_score(self, bug_probability: float, quality_score: float) -> float:
        """Calculate overall trust score"""
        return (1 - bug_probability) * 0.6 + quality_score * 0.4
    
    def _load_bug_patterns(self) -> Dict:
        """Load known bug patterns"""
        return {
            "sql_injection": r"execute\s*\(\s*['\"].*%.*['\"]",
            "hardcoded_secrets": r"(password|secret|key)\s*=\s*['\"][^'\"]+['\"]",
            "unsafe_eval": r"eval\s*\(",
        }