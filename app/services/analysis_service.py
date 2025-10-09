from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from app.core.database import get_db, get_neo4j_session, redis_client

class AnalysisService:
    """Service for managing analysis results and trust scores"""
    
    def __init__(self):
        self.redis = redis_client
    
    def calculate_overall_trust_score(
        self, 
        code_result: Dict, 
        security_result: Dict, 
        pipeline_result: Optional[Dict] = None
    ) -> float:
        """Calculate overall trust score from all analyses"""
        
        code_trust = code_result.get("trust_score", 0.5)
        security_trust = 1 - (1 - security_result.get("security_score", 0.5))
        
        if pipeline_result:
            pipeline_trust = pipeline_result.get("efficiency_score", 0.5)
            # Weighted average: code 40%, security 40%, pipeline 20%
            overall_trust = (code_trust * 0.4) + (security_trust * 0.4) + (pipeline_trust * 0.2)
        else:
            # Weighted average: code 50%, security 50%
            overall_trust = (code_trust * 0.5) + (security_trust * 0.5)
        
        return min(max(overall_trust, 0), 1)
    
    async def store_analysis_results(
        self,
        file_path: str,
        code_result: Dict,
        security_result: Dict,
        pipeline_result: Optional[Dict] = None
    ):
        """Store analysis results in database and cache"""
        
        # Calculate trust score
        trust_score = self.calculate_overall_trust_score(
            code_result, security_result, pipeline_result
        )
        
        # Store in Redis cache
        cache_key = f"trust_score:{file_path}"
        trust_data = {
            "score": trust_score,
            "components": {
                "code_quality": code_result.get("trust_score", 0.5),
                "security_score": security_result.get("security_score", 0.5),
                "pipeline_efficiency": pipeline_result.get("efficiency_score") if pipeline_result else None
            },
            "last_updated": datetime.now().isoformat()
        }
        
        self.redis.setex(cache_key, 3600, json.dumps(trust_data))  # Cache for 1 hour
        
        # Store detailed results
        results_key = f"analysis_results:{file_path}:{datetime.now().timestamp()}"
        detailed_results = {
            "file_path": file_path,
            "code_analysis": code_result,
            "security_analysis": security_result,
            "pipeline_analysis": pipeline_result,
            "trust_score": trust_score,
            "timestamp": datetime.now().isoformat()
        }
        
        self.redis.setex(results_key, 86400, json.dumps(detailed_results))  # Cache for 24 hours
        
        # Update metrics
        await self._update_metrics(trust_score, security_result, code_result)
    
    def get_trust_score(self, file_path: str) -> Optional[Dict]:
        """Get trust score for a file from cache"""
        
        cache_key = f"trust_score:{file_path}"
        cached_data = self.redis.get(cache_key)
        
        if cached_data:
            return json.loads(cached_data)
        
        return None
    
    def get_platform_metrics(self) -> Dict:
        """Get platform-wide metrics"""
        
        metrics = {
            "analyses_today": self._get_metric("analyses_today", 0),
            "avg_response_time": self._get_metric("avg_response_time", 0.5),
            "success_rate": self._get_metric("success_rate", 0.95),
            "active_projects": self._get_metric("active_projects", 0),
            "vulnerabilities_blocked": self._get_metric("vulnerabilities_blocked", 0)
        }
        
        return metrics
    
    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics"""
        
        stats = {
            "total_analyses": self._get_metric("total_analyses", 0),
            "avg_trust_score": self._get_metric("avg_trust_score", 0.75),
            "vulnerabilities_found": self._get_metric("vulnerabilities_found", 0),
            "bugs_prevented": self._get_metric("bugs_prevented", 0),
            "pipeline_optimizations": self._get_metric("pipeline_optimizations", 0),
            "cost_savings_percentage": self._get_metric("cost_savings_percentage", 0.0)
        }
        
        return stats
    
    async def process_github_event(self, payload: Dict):
        """Process GitHub webhook events"""
        
        try:
            if payload.get("commits"):
                # Process push event
                for commit in payload["commits"]:
                    await self._analyze_commit(commit, payload["repository"])
            
            elif payload.get("pull_request"):
                # Process PR event
                await self._analyze_pull_request(payload["pull_request"], payload["repository"])
            
            # Update metrics
            self._increment_metric("github_events_processed")
            
        except Exception as e:
            print(f"Error processing GitHub event: {e}")
            self._increment_metric("github_events_failed")
    
    async def _analyze_commit(self, commit: Dict, repository: Dict):
        """Analyze a single commit"""
        
        # In a real implementation, this would:
        # 1. Fetch the changed files from GitHub API
        # 2. Run analysis on each file
        # 3. Store results and send notifications if issues found
        
        print(f"Analyzing commit {commit['id']} in {repository['name']}")
        self._increment_metric("commits_analyzed")
    
    async def _analyze_pull_request(self, pr: Dict, repository: Dict):
        """Analyze a pull request"""
        
        # In a real implementation, this would:
        # 1. Fetch PR diff from GitHub API
        # 2. Run analysis on changed files
        # 3. Post review comments if issues found
        
        print(f"Analyzing PR #{pr['number']} in {repository['name']}")
        self._increment_metric("prs_analyzed")
    
    async def _update_metrics(self, trust_score: float, security_result: Dict, code_result: Dict):
        """Update platform metrics"""
        
        # Increment analysis count
        self._increment_metric("total_analyses")
        self._increment_metric("analyses_today")
        
        # Update average trust score
        current_avg = self._get_metric("avg_trust_score", 0.75)
        total_analyses = self._get_metric("total_analyses", 1)
        new_avg = ((current_avg * (total_analyses - 1)) + trust_score) / total_analyses
        self._set_metric("avg_trust_score", new_avg)
        
        # Count vulnerabilities
        vuln_count = len(security_result.get("vulnerabilities", []))
        if vuln_count > 0:
            self._increment_metric("vulnerabilities_found", vuln_count)
        
        # Count potential bugs prevented
        bug_probability = code_result.get("bug_probability", 0)
        if bug_probability > 0.7:  # High bug probability
            self._increment_metric("bugs_prevented")
    
    def _get_metric(self, key: str, default: Any = 0) -> Any:
        """Get metric value from Redis"""
        
        value = self.redis.get(f"metric:{key}")
        if value is None:
            return default
        
        try:
            return float(value) if '.' in value.decode() else int(value)
        except:
            return default
    
    def _set_metric(self, key: str, value: Any):
        """Set metric value in Redis"""
        
        self.redis.set(f"metric:{key}", str(value))
    
    def _increment_metric(self, key: str, amount: int = 1):
        """Increment metric value in Redis"""
        
        self.redis.incr(f"metric:{key}", amount)
    
    def create_code_graph(self, file_path: str, code: str, analysis_results: Dict):
        """Create code relationship graph in Neo4j"""
        
        try:
            with get_neo4j_session() as session:
                # Create file node
                session.run(
                    """
                    MERGE (f:File {path: $file_path})
                    SET f.trust_score = $trust_score,
                        f.last_analyzed = datetime(),
                        f.bug_probability = $bug_probability,
                        f.security_score = $security_score
                    """,
                    file_path=file_path,
                    trust_score=analysis_results.get("trust_score", 0.5),
                    bug_probability=analysis_results.get("bug_probability", 0.5),
                    security_score=analysis_results.get("security_score", 0.5)
                )
                
                # Create vulnerability nodes
                for vuln in analysis_results.get("vulnerabilities", []):
                    session.run(
                        """
                        MATCH (f:File {path: $file_path})
                        CREATE (v:Vulnerability {
                            type: $vuln_type,
                            severity: $severity,
                            line: $line,
                            message: $message
                        })
                        CREATE (f)-[:HAS_VULNERABILITY]->(v)
                        """,
                        file_path=file_path,
                        vuln_type=vuln.get("type"),
                        severity=vuln.get("severity"),
                        line=vuln.get("line"),
                        message=vuln.get("message")
                    )
        
        except Exception as e:
            print(f"Error creating code graph: {e}")
    
    def get_project_health_score(self, project_path: str) -> Dict:
        """Calculate overall project health score"""
        
        try:
            with get_neo4j_session() as session:
                result = session.run(
                    """
                    MATCH (f:File)
                    WHERE f.path STARTS WITH $project_path
                    RETURN 
                        AVG(f.trust_score) as avg_trust_score,
                        COUNT(f) as total_files,
                        AVG(f.security_score) as avg_security_score,
                        AVG(f.bug_probability) as avg_bug_probability
                    """,
                    project_path=project_path
                )
                
                record = result.single()
                if record:
                    return {
                        "project_path": project_path,
                        "health_score": record["avg_trust_score"] or 0.5,
                        "total_files": record["total_files"] or 0,
                        "security_score": record["avg_security_score"] or 0.5,
                        "bug_risk": record["avg_bug_probability"] or 0.5
                    }
        
        except Exception as e:
            print(f"Error calculating project health: {e}")
        
        return {
            "project_path": project_path,
            "health_score": 0.5,
            "total_files": 0,
            "security_score": 0.5,
            "bug_risk": 0.5
        }