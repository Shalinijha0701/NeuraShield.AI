#!/usr/bin/env python3
import click
import json
import asyncio
from pathlib import Path
from app.neural_shields.neural_code_brain import NeuralCodeBrain
from app.neural_shields.quantum_security_shield import QuantumSecurityShield
from app.neural_shields.adaptive_devops_optimizer import AdaptiveDevOpsOptimizer

@click.group()
def cli():
    """NeuraShield.AI - Self-Learning AI Guardian for Modern DevOps"""
    pass

@cli.command()
@click.option('--path', default='.', help='Path to analyze')
@click.option('--output', help='Output file path')
def analyze(path, output):
    """Run Neural Code Brain analysis"""
    brain = NeuralCodeBrain()
    
    for py_file in Path(path).rglob('*.py'):
        if py_file.is_file():
            code = py_file.read_text(encoding='utf-8', errors='ignore')
            result = brain.analyze_code(code, str(py_file))
            
            if output:
                with open(output, 'w') as f:
                    json.dump(result, f, indent=2)
            else:
                click.echo(f"Trust Score: {result['trust_score']:.2f} - {py_file}")

@cli.command()
@click.option('--path', default='.', help='Path to scan')
@click.option('--output', help='Output file path')
def scan(path, output):
    """Run Quantum Security Shield scan"""
    shield = QuantumSecurityShield()
    
    for py_file in Path(path).rglob('*.py'):
        if py_file.is_file():
            code = py_file.read_text(encoding='utf-8', errors='ignore')
            result = shield.scan_security(code, str(py_file))
            
            if output:
                with open(output, 'w') as f:
                    json.dump(result, f, indent=2)
            else:
                click.echo(f"Security Score: {result['security_score']:.2f} - {py_file}")

@cli.command()
@click.option('--config', help='Pipeline config path')
def optimize(config):
    """Run Adaptive DevOps Optimizer"""
    optimizer = AdaptiveDevOpsOptimizer()
    
    pipeline_config = {
        "id": "cli-pipeline",
        "steps": [
            {"name": "build", "type": "build"},
            {"name": "test", "type": "test"},
            {"name": "deploy", "type": "deploy"}
        ]
    }
    
    result = optimizer.analyze_pipeline(pipeline_config)
    click.echo(f"Efficiency Score: {result['efficiency_score']:.2f}")
    click.echo(f"Optimizations: {len(result['optimizations'])}")

def main():
    cli()

if __name__ == '__main__':
    main()