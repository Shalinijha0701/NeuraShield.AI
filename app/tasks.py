from celery import current_app as celery_app
from app.neural_shields.neural_code_brain import NeuralCodeBrain
from app.neural_shields.quantum_security_shield import QuantumSecurityShield
from app.neural_shields.adaptive_devops_optimizer import AdaptiveDevOpsOptimizer

@celery_app.task
def analyze_code_task(code: str, file_path: str):
    """Background task for code analysis"""
    brain = NeuralCodeBrain()
    return brain.analyze_code(code, file_path)

@celery_app.task
def scan_security_task(code: str, file_path: str, dependencies: list = None):
    """Background task for security scanning"""
    shield = QuantumSecurityShield()
    return shield.scan_security(code, file_path, dependencies)

@celery_app.task
def optimize_pipeline_task(pipeline_config: dict, historical_data: list = None):
    """Background task for pipeline optimization"""
    optimizer = AdaptiveDevOpsOptimizer()
    return optimizer.analyze_pipeline(pipeline_config, historical_data)