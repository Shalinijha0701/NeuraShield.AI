import pytest
import asyncio
from app.neural_shields.neural_code_brain import NeuralCodeBrain
from app.neural_shields.quantum_security_shield import QuantumSecurityShield
from app.neural_shields.adaptive_devops_optimizer import AdaptiveDevOpsOptimizer

class TestNeuralCodeBrain:
    def setup_method(self):
        self.code_brain = NeuralCodeBrain()
    
    def test_analyze_simple_code(self):
        code = """
def hello_world():
    print("Hello, World!")
    return "success"
"""
        result = self.code_brain.analyze_code(code, "test.py")
        
        assert "file_path" in result
        assert "bug_probability" in result
        assert "quality_score" in result
        assert "trust_score" in result
        assert 0 <= result["bug_probability"] <= 1
        assert 0 <= result["quality_score"] <= 1
        assert 0 <= result["trust_score"] <= 1
    
    def test_analyze_complex_code(self):
        code = """
def complex_function(a, b, c, d, e, f, g, h):  # Too many parameters
    if a > 0:
        if b > 0:
            if c > 0:
                return a + b + c
            else:
                return a + b
        else:
            return a
    else:
        return 0
"""
        result = self.code_brain.analyze_code(code, "complex.py")
        
        assert result["bug_probability"] > 0.3  # Should detect complexity issues
        assert len(result["issues"]) > 0
    
    def test_syntax_error_handling(self):
        code = "def invalid_syntax(:"
        result = self.code_brain.analyze_code(code, "invalid.py")
        
        assert "error" in result
        assert result["bug_probability"] == 1.0
        assert result["trust_score"] == 0.0

class TestQuantumSecurityShield:
    def setup_method(self):
        self.security_shield = QuantumSecurityShield()
    
    def test_detect_hardcoded_secrets(self):
        code = """
API_KEY = "sk-1234567890abcdef"
password = "super_secret_password"
"""
        result = self.security_shield.scan_security(code, "secrets.py")
        
        assert len(result["secrets_detected"]) >= 2
        assert result["security_score"] < 0.8
        assert result["risk_level"] in ["medium", "high", "critical"]
    
    def test_detect_sql_injection(self):
        code = """
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = '%s'" % user_id
    return execute(query)
"""
        result = self.security_shield.scan_security(code, "sql.py")
        
        assert len(result["vulnerabilities"]) > 0
        assert any(v["type"] == "sql_injection" for v in result["vulnerabilities"])
    
    def test_clean_code_analysis(self):
        code = """
def safe_function():
    return "This is safe code"
"""
        result = self.security_shield.scan_security(code, "safe.py")
        
        assert len(result["vulnerabilities"]) == 0
        assert len(result["secrets_detected"]) == 0
        assert result["security_score"] > 0.8

class TestAdaptiveDevOpsOptimizer:
    def setup_method(self):
        self.optimizer = AdaptiveDevOpsOptimizer()
    
    def test_analyze_simple_pipeline(self):
        pipeline_config = {
            "id": "test-pipeline",
            "steps": [
                {"name": "build", "type": "build"},
                {"name": "test", "type": "test"},
                {"name": "deploy", "type": "deploy"}
            ]
        }
        
        result = self.optimizer.analyze_pipeline(pipeline_config)
        
        assert "pipeline_id" in result
        assert "efficiency_score" in result
        assert "failure_probability" in result
        assert 0 <= result["efficiency_score"] <= 1
        assert 0 <= result["failure_probability"] <= 1
    
    def test_detect_optimization_opportunities(self):
        pipeline_config = {
            "id": "slow-pipeline",
            "steps": [
                {
                    "name": "build", 
                    "type": "build",
                    "docker_image": "node:latest"  # Should suggest pinning version
                },
                {
                    "name": "test", 
                    "type": "test"
                    # Missing timeout and parallel execution
                }
            ]
        }
        
        result = self.optimizer.analyze_pipeline(pipeline_config)
        
        assert len(result["optimizations"]) > 0
        assert any("pin_image_version" in str(opt) for opt in result["optimizations"])
    
    def test_predict_improvements(self):
        pipeline_config = {
            "id": "test-pipeline",
            "steps": [
                {"name": "build", "type": "build"},
                {"name": "test", "type": "test", "parallel": True}
            ]
        }
        
        result = self.optimizer.analyze_pipeline(pipeline_config)
        improvements = result["predicted_improvements"]
        
        assert "build_time_reduction" in improvements
        assert "success_rate_increase" in improvements
        assert "cost_reduction" in improvements

@pytest.mark.asyncio
async def test_integration_all_shields():
    """Test integration of all three neural shields"""
    code = """
def process_user_data(user_input):
    # Potential security issue
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    return execute_query(query)
"""
    
    code_brain = NeuralCodeBrain()
    security_shield = QuantumSecurityShield()
    
    # Run analyses
    code_result = code_brain.analyze_code(code, "integration_test.py")
    security_result = security_shield.scan_security(code, "integration_test.py")
    
    # Verify results
    assert code_result["trust_score"] < 0.8  # Should detect issues
    assert len(security_result["vulnerabilities"]) > 0  # Should find SQL injection
    assert security_result["risk_level"] in ["high", "critical"]

if __name__ == "__main__":
    pytest.main([__file__])