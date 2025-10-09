from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from app.models.schemas import (
    CodeAnalysisRequest, CodeAnalysisResponse,
    SecurityScanRequest, SecurityScanResponse,
    PipelineAnalysisRequest, PipelineAnalysisResponse,
    TrustScoreResponse
)
from app.neural_shields.neural_code_brain import NeuralCodeBrain
from app.neural_shields.quantum_security_shield import QuantumSecurityShield
from app.neural_shields.adaptive_devops_optimizer import AdaptiveDevOpsOptimizer
from app.services.analysis_service import AnalysisService

router = APIRouter()

# Initialize neural shields
code_brain = NeuralCodeBrain()
security_shield = QuantumSecurityShield()
devops_optimizer = AdaptiveDevOpsOptimizer()
analysis_service = AnalysisService()

@router.post("/analyze/code", response_model=CodeAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """Analyze code using Neural Code Brain"""
    try:
        result = code_brain.analyze_code(request.code, request.file_path)
        return CodeAnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code analysis failed: {str(e)}")

@router.post("/analyze/security", response_model=SecurityScanResponse)
async def scan_security(request: SecurityScanRequest):
    """Scan code for security vulnerabilities using Quantum Security Shield"""
    try:
        result = security_shield.scan_security(
            request.code, 
            request.file_path, 
            request.dependencies
        )
        return SecurityScanResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Security scan failed: {str(e)}")

@router.post("/analyze/pipeline", response_model=PipelineAnalysisResponse)
async def analyze_pipeline(request: PipelineAnalysisRequest):
    """Analyze CI/CD pipeline using Adaptive DevOps Optimizer"""
    try:
        result = devops_optimizer.analyze_pipeline(
            request.pipeline_config.dict(), 
            request.historical_data
        )
        return PipelineAnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline analysis failed: {str(e)}")

@router.post("/analyze/complete")
async def complete_analysis(
    background_tasks: BackgroundTasks,
    code: str,
    file_path: str,
    dependencies: Optional[List[str]] = None,
    pipeline_config: Optional[dict] = None
):
    """Run complete analysis using all three neural shields"""
    try:
        # Run all analyses
        code_result = code_brain.analyze_code(code, file_path)
        security_result = security_shield.scan_security(code, file_path, dependencies)
        
        pipeline_result = None
        if pipeline_config:
            pipeline_result = devops_optimizer.analyze_pipeline(pipeline_config)
        
        # Calculate overall trust score
        trust_score = analysis_service.calculate_overall_trust_score(
            code_result, security_result, pipeline_result
        )
        
        # Store results in background
        background_tasks.add_task(
            analysis_service.store_analysis_results,
            file_path, code_result, security_result, pipeline_result
        )
        
        return {
            "file_path": file_path,
            "code_analysis": code_result,
            "security_analysis": security_result,
            "pipeline_analysis": pipeline_result,
            "overall_trust_score": trust_score,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Complete analysis failed: {str(e)}")

@router.get("/trust-score/{file_path:path}", response_model=TrustScoreResponse)
async def get_trust_score(file_path: str):
    """Get trust score for a specific file"""
    try:
        trust_score = analysis_service.get_trust_score(file_path)
        if trust_score is None:
            raise HTTPException(status_code=404, detail="Trust score not found")
        
        return TrustScoreResponse(
            file_path=file_path,
            trust_score=trust_score["score"],
            components=trust_score["components"],
            last_updated=trust_score["last_updated"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get trust score: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "neural_shields": {
            "code_brain": "active",
            "security_shield": "active",
            "devops_optimizer": "active"
        },
        "version": "1.0.0"
    }

@router.get("/metrics")
async def get_metrics():
    """Get platform metrics"""
    try:
        metrics = analysis_service.get_platform_metrics()
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")

@router.post("/webhook/github")
async def github_webhook(background_tasks: BackgroundTasks, payload: dict):
    """Handle GitHub webhook events"""
    try:
        if payload.get("action") == "opened" or payload.get("ref"):
            # Process push or PR event
            background_tasks.add_task(
                analysis_service.process_github_event, payload
            )
            return {"status": "processing", "message": "Analysis started"}
        
        return {"status": "ignored", "message": "Event not processed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")

@router.get("/dashboard/stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        stats = analysis_service.get_dashboard_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard stats: {str(e)}")