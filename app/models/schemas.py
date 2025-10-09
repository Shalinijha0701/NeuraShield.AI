from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Code Analysis Schemas
class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., description="Source code to analyze")
    file_path: str = Field(..., description="Path to the file being analyzed")
    language: Optional[str] = Field(None, description="Programming language")

class CodeIssue(BaseModel):
    type: str
    message: str
    line: int
    severity: str

class CodeAnalysisResponse(BaseModel):
    file_path: str
    bug_probability: float = Field(..., ge=0, le=1)
    quality_score: float = Field(..., ge=0, le=1)
    trust_score: float = Field(..., ge=0, le=1)
    issues: List[CodeIssue]
    suggestions: List[str]

# Security Analysis Schemas
class SecurityScanRequest(BaseModel):
    code: str = Field(..., description="Source code to scan")
    file_path: str = Field(..., description="Path to the file being scanned")
    dependencies: Optional[List[str]] = Field(None, description="List of dependencies")

class Vulnerability(BaseModel):
    type: str
    severity: str
    line: Optional[int] = None
    message: str
    confidence: Optional[str] = None

class Secret(BaseModel):
    type: str
    line: int
    severity: str
    message: str
    masked_value: str

class DependencyRisk(BaseModel):
    type: str
    package: str
    severity: str
    message: str
    cve_id: Optional[str] = None

class AutoFix(BaseModel):
    vulnerability: str
    fix_type: str
    description: str
    auto_applicable: bool

class SecurityScanResponse(BaseModel):
    file_path: str
    vulnerabilities: List[Vulnerability]
    secrets_detected: List[Secret]
    dependency_risks: List[DependencyRisk]
    security_score: float = Field(..., ge=0, le=1)
    risk_level: str
    auto_fix_suggestions: List[AutoFix]

# Pipeline Analysis Schemas
class PipelineStep(BaseModel):
    name: str
    type: str
    options: Optional[Dict[str, Any]] = None
    timeout: Optional[int] = None
    parallel: Optional[bool] = False

class PipelineConfig(BaseModel):
    id: str
    name: str
    steps: List[PipelineStep]
    triggers: Optional[List[str]] = None

class PipelineAnalysisRequest(BaseModel):
    pipeline_config: PipelineConfig
    historical_data: Optional[List[Dict[str, Any]]] = None

class Optimization(BaseModel):
    type: str
    description: str
    estimated_improvement: str
    implementation: str

class OptimizationGroup(BaseModel):
    step_index: int
    step_name: str
    optimizations: List[Optimization]

class PipelineMetrics(BaseModel):
    build_time: float
    success_rate: float
    resource_usage: Dict[str, float]
    failure_patterns: List[str]
    deployment_time: float

class PredictedImprovements(BaseModel):
    build_time_reduction: float
    success_rate_increase: float
    cost_reduction: float
    reliability_improvement: float

class ConfigChange(BaseModel):
    step_index: int
    changes: Dict[str, Any]

class AutoFixSuggestion(BaseModel):
    optimization: str
    description: str
    auto_applicable: bool
    config_change: ConfigChange

class PipelineAnalysisResponse(BaseModel):
    pipeline_id: str
    current_metrics: PipelineMetrics
    failure_probability: float = Field(..., ge=0, le=1)
    efficiency_score: float = Field(..., ge=0, le=1)
    optimizations: List[OptimizationGroup]
    predicted_improvements: PredictedImprovements
    auto_fix_suggestions: List[AutoFixSuggestion]

# Trust Score Schemas
class TrustScoreComponents(BaseModel):
    code_quality: float = Field(..., ge=0, le=1)
    security_score: float = Field(..., ge=0, le=1)
    pipeline_efficiency: Optional[float] = Field(None, ge=0, le=1)

class TrustScoreResponse(BaseModel):
    file_path: str
    trust_score: float = Field(..., ge=0, le=1)
    components: TrustScoreComponents
    last_updated: datetime

# Dashboard Schemas
class DashboardStats(BaseModel):
    total_analyses: int
    avg_trust_score: float
    vulnerabilities_found: int
    bugs_prevented: int
    pipeline_optimizations: int
    cost_savings_percentage: float

# Webhook Schemas
class GitHubWebhookPayload(BaseModel):
    action: Optional[str] = None
    ref: Optional[str] = None
    repository: Dict[str, Any]
    commits: Optional[List[Dict[str, Any]]] = None
    pull_request: Optional[Dict[str, Any]] = None

# Analysis Service Schemas
class AnalysisResult(BaseModel):
    id: str
    file_path: str
    analysis_type: str
    results: Dict[str, Any]
    trust_score: float
    timestamp: datetime

class PlatformMetrics(BaseModel):
    analyses_today: int
    avg_response_time: float
    success_rate: float
    active_projects: int
    vulnerabilities_blocked: int