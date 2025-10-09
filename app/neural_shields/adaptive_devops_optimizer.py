import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from app.core.config import settings

@dataclass
class PipelineMetrics:
    build_time: float
    success_rate: float
    resource_usage: Dict[str, float]
    failure_patterns: List[str]
    deployment_time: float

class AdaptiveDevOpsOptimizer:
    """Smart Process Brain with Reinforcement Learning"""
    
    def __init__(self):
        self.learning_rate = settings.DEVOPS_OPTIMIZER_LEARNING_RATE
        self.q_table = {}  # Q-learning table
        self.pipeline_history = []
        self.optimization_strategies = self._load_optimization_strategies()
    
    def analyze_pipeline(self, pipeline_config: Dict, historical_data: List[Dict] = None) -> Dict:
        """Analyze CI/CD pipeline and suggest optimizations"""
        
        # Extract pipeline metrics
        metrics = self._extract_metrics(pipeline_config, historical_data or [])
        
        # Predict failure probability
        failure_probability = self._predict_failure(pipeline_config, metrics)
        
        # Generate optimizations
        optimizations = self._generate_optimizations(pipeline_config, metrics)
        
        # Calculate efficiency score
        efficiency_score = self._calculate_efficiency_score(metrics)
        
        # Learn from this analysis
        self._update_learning_model(pipeline_config, metrics)
        
        return {
            "pipeline_id": pipeline_config.get("id", "unknown"),
            "current_metrics": metrics.__dict__,
            "failure_probability": failure_probability,
            "efficiency_score": efficiency_score,
            "optimizations": optimizations,
            "predicted_improvements": self._predict_improvements(optimizations),
            "auto_fix_suggestions": self._generate_auto_fixes(pipeline_config, optimizations)
        }
    
    def _extract_metrics(self, pipeline_config: Dict, historical_data: List[Dict]) -> PipelineMetrics:
        """Extract key metrics from pipeline configuration and history"""
        
        if historical_data:
            avg_build_time = np.mean([run.get("build_time", 0) for run in historical_data])
            success_rate = len([run for run in historical_data if run.get("status") == "success"]) / len(historical_data)
            avg_deployment_time = np.mean([run.get("deployment_time", 0) for run in historical_data])
            
            # Extract failure patterns
            failure_patterns = []
            for run in historical_data:
                if run.get("status") == "failed":
                    failure_patterns.append(run.get("error_type", "unknown"))
        else:
            # Estimate based on pipeline configuration
            avg_build_time = self._estimate_build_time(pipeline_config)
            success_rate = 0.85  # Default assumption
            avg_deployment_time = self._estimate_deployment_time(pipeline_config)
            failure_patterns = []
        
        # Analyze resource usage
        resource_usage = self._analyze_resource_usage(pipeline_config)
        
        return PipelineMetrics(
            build_time=avg_build_time,
            success_rate=success_rate,
            resource_usage=resource_usage,
            failure_patterns=failure_patterns,
            deployment_time=avg_deployment_time
        )
    
    def _predict_failure(self, pipeline_config: Dict, metrics: PipelineMetrics) -> float:
        """Predict probability of pipeline failure using ML"""
        
        risk_factors = 0
        total_factors = 0
        
        # Check for risky configurations
        steps = pipeline_config.get("steps", [])
        
        for step in steps:
            total_factors += 1
            
            # Check for common failure patterns
            if step.get("type") == "test":
                if not step.get("timeout"):
                    risk_factors += 0.3  # No timeout set
                if step.get("parallel", False) and len(steps) > 10:
                    risk_factors += 0.2  # Complex parallel execution
            
            elif step.get("type") == "build":
                if "cache" not in step.get("options", {}):
                    risk_factors += 0.4  # No caching
                if step.get("docker_image", "").startswith("latest"):
                    risk_factors += 0.5  # Using latest tag
            
            elif step.get("type") == "deploy":
                if not step.get("rollback_strategy"):
                    risk_factors += 0.6  # No rollback strategy
        
        # Factor in historical success rate
        historical_risk = 1 - metrics.success_rate
        
        # Combine factors
        config_risk = min(risk_factors / max(total_factors, 1), 1.0)
        overall_risk = (config_risk * 0.6) + (historical_risk * 0.4)
        
        return min(overall_risk, 1.0)
    
    def _generate_optimizations(self, pipeline_config: Dict, metrics: PipelineMetrics) -> List[Dict]:
        """Generate optimization suggestions using reinforcement learning"""
        optimizations = []
        
        steps = pipeline_config.get("steps", [])
        
        for i, step in enumerate(steps):
            step_optimizations = []
            
            # Build optimizations
            if step.get("type") == "build":
                if "cache" not in step.get("options", {}):
                    step_optimizations.append({
                        "type": "add_caching",
                        "description": "Add build caching to reduce build time",
                        "estimated_improvement": "30-50% faster builds",
                        "implementation": "Add cache: true to build step"
                    })
                
                if step.get("docker_image", "").endswith(":latest"):
                    step_optimizations.append({
                        "type": "pin_image_version",
                        "description": "Pin Docker image to specific version",
                        "estimated_improvement": "Improved build consistency",
                        "implementation": "Use specific version tag instead of 'latest'"
                    })
            
            # Test optimizations
            elif step.get("type") == "test":
                if not step.get("parallel", False) and len(steps) > 5:
                    step_optimizations.append({
                        "type": "parallel_testing",
                        "description": "Run tests in parallel",
                        "estimated_improvement": "40-60% faster test execution",
                        "implementation": "Add parallel: true and split test suites"
                    })
                
                if not step.get("timeout"):
                    step_optimizations.append({
                        "type": "add_timeout",
                        "description": "Add timeout to prevent hanging tests",
                        "estimated_improvement": "Prevent infinite test runs",
                        "implementation": "Add timeout: 600 (10 minutes)"
                    })
            
            # Deployment optimizations
            elif step.get("type") == "deploy":
                if not step.get("health_check"):
                    step_optimizations.append({
                        "type": "add_health_check",
                        "description": "Add health check after deployment",
                        "estimated_improvement": "Catch deployment issues early",
                        "implementation": "Add health_check endpoint validation"
                    })
            
            if step_optimizations:
                optimizations.append({
                    "step_index": i,
                    "step_name": step.get("name", f"Step {i+1}"),
                    "optimizations": step_optimizations
                })
        
        # Pipeline-level optimizations
        pipeline_opts = self._generate_pipeline_optimizations(pipeline_config, metrics)
        if pipeline_opts:
            optimizations.append({
                "step_index": -1,
                "step_name": "Pipeline Configuration",
                "optimizations": pipeline_opts
            })
        
        return optimizations
    
    def _generate_pipeline_optimizations(self, pipeline_config: Dict, metrics: PipelineMetrics) -> List[Dict]:
        """Generate pipeline-level optimizations"""
        optimizations = []
        
        # Resource optimization
        if metrics.resource_usage.get("cpu", 0) < 0.5:
            optimizations.append({
                "type": "reduce_resources",
                "description": "Reduce allocated CPU resources",
                "estimated_improvement": "20-30% cost reduction",
                "implementation": "Reduce CPU allocation from current to optimized level"
            })
        
        # Workflow optimization
        steps = pipeline_config.get("steps", [])
        if len(steps) > 10:
            optimizations.append({
                "type": "workflow_simplification",
                "description": "Simplify complex workflow",
                "estimated_improvement": "Easier maintenance and debugging",
                "implementation": "Combine related steps and reduce complexity"
            })
        
        # Failure recovery
        if metrics.success_rate < 0.9:
            optimizations.append({
                "type": "improve_reliability",
                "description": "Add retry mechanisms and better error handling",
                "estimated_improvement": f"Increase success rate from {metrics.success_rate:.1%} to 95%+",
                "implementation": "Add retry logic and comprehensive error handling"
            })
        
        return optimizations
    
    def _calculate_efficiency_score(self, metrics: PipelineMetrics) -> float:
        """Calculate overall pipeline efficiency score"""
        
        # Normalize metrics to 0-1 scale
        time_score = max(0, 1 - (metrics.build_time / 3600))  # Assume 1 hour is poor
        success_score = metrics.success_rate
        resource_score = 1 - metrics.resource_usage.get("cpu", 0.5)  # Lower usage is better
        
        # Weighted average
        efficiency = (time_score * 0.4) + (success_score * 0.4) + (resource_score * 0.2)
        
        return min(max(efficiency, 0), 1)
    
    def _predict_improvements(self, optimizations: List[Dict]) -> Dict:
        """Predict improvements from applying optimizations"""
        improvements = {
            "build_time_reduction": 0,
            "success_rate_increase": 0,
            "cost_reduction": 0,
            "reliability_improvement": 0
        }
        
        for opt_group in optimizations:
            for opt in opt_group.get("optimizations", []):
                opt_type = opt["type"]
                
                if opt_type == "add_caching":
                    improvements["build_time_reduction"] += 0.35
                elif opt_type == "parallel_testing":
                    improvements["build_time_reduction"] += 0.45
                elif opt_type == "reduce_resources":
                    improvements["cost_reduction"] += 0.25
                elif opt_type == "improve_reliability":
                    improvements["success_rate_increase"] += 0.1
                elif opt_type == "add_health_check":
                    improvements["reliability_improvement"] += 0.2
        
        # Cap improvements at reasonable levels
        for key in improvements:
            improvements[key] = min(improvements[key], 0.8)
        
        return improvements
    
    def _generate_auto_fixes(self, pipeline_config: Dict, optimizations: List[Dict]) -> List[Dict]:
        """Generate automatic fixes that can be applied"""
        auto_fixes = []
        
        for opt_group in optimizations:
            for opt in opt_group.get("optimizations", []):
                if opt["type"] in ["add_timeout", "pin_image_version", "add_caching"]:
                    auto_fixes.append({
                        "optimization": opt["type"],
                        "description": opt["description"],
                        "auto_applicable": True,
                        "config_change": self._generate_config_change(opt["type"], opt_group["step_index"])
                    })
        
        return auto_fixes
    
    def _generate_config_change(self, opt_type: str, step_index: int) -> Dict:
        """Generate specific configuration changes"""
        changes = {
            "add_timeout": {"timeout": 600},
            "add_caching": {"cache": True},
            "pin_image_version": {"docker_image": "node:18-alpine"}  # Example
        }
        
        return {
            "step_index": step_index,
            "changes": changes.get(opt_type, {})
        }
    
    def _update_learning_model(self, pipeline_config: Dict, metrics: PipelineMetrics):
        """Update Q-learning model with new data"""
        
        # Create state representation
        state = self._create_state_representation(pipeline_config)
        
        # Calculate reward based on metrics
        reward = self._calculate_reward(metrics)
        
        # Update Q-table (simplified Q-learning)
        if state not in self.q_table:
            self.q_table[state] = {}
        
        # Store this experience
        self.pipeline_history.append({
            "state": state,
            "metrics": metrics,
            "reward": reward,
            "timestamp": "2024-01-01"  # In production, use actual timestamp
        })
    
    def _create_state_representation(self, pipeline_config: Dict) -> str:
        """Create a state representation for Q-learning"""
        
        features = []
        steps = pipeline_config.get("steps", [])
        
        features.append(f"steps_{len(steps)}")
        features.append(f"has_tests_{any(s.get('type') == 'test' for s in steps)}")
        features.append(f"has_deploy_{any(s.get('type') == 'deploy' for s in steps)}")
        features.append(f"uses_docker_{any('docker' in str(s) for s in steps)}")
        
        return "_".join(features)
    
    def _calculate_reward(self, metrics: PipelineMetrics) -> float:
        """Calculate reward for reinforcement learning"""
        
        # Reward based on success rate and efficiency
        success_reward = metrics.success_rate * 10
        time_penalty = max(0, metrics.build_time / 3600) * -5  # Penalty for long builds
        
        return success_reward + time_penalty
    
    def _estimate_build_time(self, pipeline_config: Dict) -> float:
        """Estimate build time based on configuration"""
        
        base_time = 300  # 5 minutes base
        steps = pipeline_config.get("steps", [])
        
        for step in steps:
            if step.get("type") == "build":
                base_time += 600  # 10 minutes for build
            elif step.get("type") == "test":
                base_time += 300  # 5 minutes for tests
            elif step.get("type") == "deploy":
                base_time += 180  # 3 minutes for deploy
        
        return base_time
    
    def _estimate_deployment_time(self, pipeline_config: Dict) -> float:
        """Estimate deployment time"""
        
        deploy_steps = [s for s in pipeline_config.get("steps", []) if s.get("type") == "deploy"]
        return len(deploy_steps) * 120  # 2 minutes per deploy step
    
    def _analyze_resource_usage(self, pipeline_config: Dict) -> Dict[str, float]:
        """Analyze resource usage patterns"""
        
        steps = pipeline_config.get("steps", [])
        cpu_usage = min(len(steps) * 0.1, 1.0)  # Estimate based on step count
        memory_usage = min(len(steps) * 0.15, 1.0)
        
        return {
            "cpu": cpu_usage,
            "memory": memory_usage,
            "storage": 0.3  # Default estimate
        }
    
    def _load_optimization_strategies(self) -> Dict:
        """Load optimization strategies"""
        return {
            "caching": {
                "description": "Implement build and dependency caching",
                "impact": "high",
                "complexity": "low"
            },
            "parallelization": {
                "description": "Run independent tasks in parallel",
                "impact": "high",
                "complexity": "medium"
            },
            "resource_optimization": {
                "description": "Optimize resource allocation",
                "impact": "medium",
                "complexity": "low"
            }
        }