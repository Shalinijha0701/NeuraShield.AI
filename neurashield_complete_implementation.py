#!/usr/bin/env python3
"""
NeuraShield.AI - Complete Implementation
Self-Learning AI Guardian for Modern DevOps
"""

import ast
import os
import json
import hashlib
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import openai
import chromadb
from fastapi import FastAPI, HTTPException
import uvicorn

@dataclass
class CodeChunk:
    content: str
    file_path: str
    function_name: str
    start_line: int
    end_line: int
    complexity: int
    chunk_hash: str

class CodeExtractor:
    """Phase 1: Code Extraction & Processing"""
    
    def extract_from_repository(self, repo_path: str) -> List[CodeChunk]:
        chunks = []
        for py_file in Path(repo_path).rglob("*.py"):
            if "test" in str(py_file):
                continue
            chunks.extend(self._extract_from_file(py_file))
        return chunks
    
    def _extract_from_file(self, file_path: Path) -> List[CodeChunk]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            chunks = []
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    chunk_content = ast.get_source_segment(content, node)
                    if chunk_content and len(chunk_content) > 50:
                        complexity = self._calculate_complexity(node)
                        chunk_hash = hashlib.md5(chunk_content.encode()).hexdigest()
                        
                        chunks.append(CodeChunk(
                            content=chunk_content,
                            file_path=str(file_path),
                            function_name=node.name,
                            start_line=node.lineno,
                            end_line=node.end_lineno or node.lineno,
                            complexity=complexity,
                            chunk_hash=chunk_hash
                        ))
            return chunks
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return []
    
    def _calculate_complexity(self, node: ast.AST) -> int:
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
        return complexity

class EmbeddingGenerator:
    """Phase 1: Generate embeddings for code chunks"""
    
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate_embeddings(self, chunks: List[CodeChunk]) -> List[Dict]:
        embeddings = []
        for chunk in chunks:
            try:
                response = self.client.embeddings.create(
                    model="text-embedding-3-small",
                    input=f"Function: {chunk.function_name}\n{chunk.content}"
                )
                
                embeddings.append({
                    "id": chunk.chunk_hash,
                    "embedding": response.data[0].embedding,
                    "metadata": {
                        "file_path": chunk.file_path,
                        "function_name": chunk.function_name,
                        "complexity": chunk.complexity,
                        "content": chunk.content
                    }
                })
            except Exception as e:
                print(f"Error generating embedding: {e}")
        
        return embeddings

class VectorDatabase:
    """Phase 1: Vector storage and retrieval"""
    
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("neurashield_code")
    
    def store_embeddings(self, embeddings: List[Dict]):
        ids = [emb["id"] for emb in embeddings]
        vectors = [emb["embedding"] for emb in embeddings]
        metadatas = [emb["metadata"] for emb in embeddings]
        
        self.collection.add(
            ids=ids,
            embeddings=vectors,
            metadatas=metadatas
        )
    
    def search_similar(self, query_embedding: List[float], k: int = 5) -> List[Dict]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        similar_chunks = []
        for i in range(len(results["ids"][0])):
            similar_chunks.append({
                "content": results["metadatas"][0][i]["content"],
                "file_path": results["metadatas"][0][i]["file_path"],
                "function_name": results["metadatas"][0][i]["function_name"],
                "distance": results["distances"][0][i]
            })
        
        return similar_chunks

class RAGAnalyzer:
    """Phase 2: RAG-based code analysis"""
    
    def __init__(self, api_key: str, vector_db: VectorDatabase):
        self.client = openai.OpenAI(api_key=api_key)
        self.vector_db = vector_db
        self.embedding_gen = EmbeddingGenerator(api_key)
    
    def analyze_code(self, code: str, analysis_type: str = "security") -> Dict:
        # Generate query embedding
        query_response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=code
        )
        query_embedding = query_response.data[0].embedding
        
        # Retrieve similar patterns
        similar_patterns = self.vector_db.search_similar(query_embedding, k=3)
        
        # Generate analysis prompt
        if analysis_type == "security":
            return self._security_analysis(code, similar_patterns)
        elif analysis_type == "optimization":
            return self._optimization_analysis(code, similar_patterns)
        else:
            return self._bug_detection(code, similar_patterns)
    
    def _security_analysis(self, code: str, patterns: List[Dict]) -> Dict:
        context = "\n".join([f"Similar pattern: {p['content'][:200]}..." for p in patterns])
        
        prompt = f"""
Analyze this code for security vulnerabilities using Chain-of-Thought reasoning:

CODE TO ANALYZE:
{code}

SIMILAR PATTERNS FROM CODEBASE:
{context}

ANALYSIS STEPS:
1. Identify vulnerability type (SQL injection, XSS, buffer overflow, etc.)
2. Assess exploitability (easy/moderate/hard)
3. Determine impact on CIA (Confidentiality, Integrity, Availability)
4. Calculate CVSS Base Score (0-10)
5. Provide specific fix with code example

Return JSON format:
{{
    "vulnerabilities": [{{
        "type": "vulnerability_type",
        "severity": "low|medium|high|critical",
        "cvss_score": 0.0,
        "description": "detailed description",
        "fix": "code fix example"
    }}],
    "overall_score": 0.0,
    "recommendation": "action needed"
}}
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except:
            return {"error": "Failed to parse analysis", "raw_response": response.choices[0].message.content}
    
    def _optimization_analysis(self, code: str, patterns: List[Dict]) -> Dict:
        context = "\n".join([f"Pattern: {p['content'][:200]}..." for p in patterns])
        
        prompt = f"""
Analyze this code for optimization opportunities:

CODE: {code}
SIMILAR PATTERNS: {context}

Provide JSON with:
- Time complexity analysis
- Space complexity analysis  
- Optimization suggestions
- Refactored code example
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except:
            return {"error": "Failed to parse optimization", "raw_response": response.choices[0].message.content}
    
    def _bug_detection(self, code: str, patterns: List[Dict]) -> Dict:
        context = "\n".join([f"Pattern: {p['content'][:200]}..." for p in patterns])
        
        prompt = f"""
Detect potential bugs in this code:

CODE: {code}
SIMILAR PATTERNS: {context}

Return JSON with bug predictions, confidence scores, and fixes.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except:
            return {"error": "Failed to parse bugs", "raw_response": response.choices[0].message.content}

# Phase 3: FastAPI Integration
app = FastAPI(title="NeuraShield.AI", description="Self-Learning AI Guardian")

# Global instances
vector_db = VectorDatabase()
analyzer = None

@app.on_event("startup")
async def startup():
    global analyzer
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        analyzer = RAGAnalyzer(api_key, vector_db)

@app.post("/analyze/security")
async def analyze_security(code: str):
    if not analyzer:
        raise HTTPException(400, "OpenAI API key not configured")
    
    result = analyzer.analyze_code(code, "security")
    return result

@app.post("/analyze/optimization")
async def analyze_optimization(code: str):
    if not analyzer:
        raise HTTPException(400, "OpenAI API key not configured")
    
    result = analyzer.analyze_code(code, "optimization")
    return result

@app.post("/analyze/bugs")
async def analyze_bugs(code: str):
    if not analyzer:
        raise HTTPException(400, "OpenAI API key not configured")
    
    result = analyzer.analyze_code(code, "bugs")
    return result

@app.post("/train/repository")
async def train_repository(repo_path: str):
    """Train NeuraShield on a code repository"""
    if not analyzer:
        raise HTTPException(400, "OpenAI API key not configured")
    
    try:
        # Extract code chunks
        extractor = CodeExtractor()
        chunks = extractor.extract_from_repository(repo_path)
        
        # Generate embeddings
        embedding_gen = EmbeddingGenerator(os.getenv("OPENAI_API_KEY"))
        embeddings = embedding_gen.generate_embeddings(chunks)
        
        # Store in vector database
        vector_db.store_embeddings(embeddings)
        
        return {
            "status": "success",
            "chunks_processed": len(chunks),
            "embeddings_stored": len(embeddings)
        }
    except Exception as e:
        raise HTTPException(500, f"Training failed: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "NeuraShield.AI - Self-Learning AI Guardian",
        "version": "1.0.0",
        "status": "active",
        "endpoints": ["/analyze/security", "/analyze/optimization", "/analyze/bugs", "/train/repository"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)