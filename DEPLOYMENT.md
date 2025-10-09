# NeuraShield.AI Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+
- Neo4j 5.13+

### Local Development Setup

1. **Clone and Setup Environment**
```bash
git clone <repository-url>
cd NeuraShield.AI
cp .env.example .env
# Edit .env with your configuration
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Start Infrastructure**
```bash
docker-compose up -d postgres redis neo4j
```

4. **Run Application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. **Start Frontend**
```bash
cd frontend
npm install
npm run dev
```

## 🐳 Docker Deployment

### Full Stack Deployment
```bash
docker-compose up -d
```

### Production Deployment
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## ☁️ Cloud Deployment

### AWS ECS Deployment

1. **Build and Push Images**
```bash
# Build application image
docker build -t neurashield-api .
docker tag neurashield-api:latest <account-id>.dkr.ecr.<region>.amazonaws.com/neurashield-api:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/neurashield-api:latest

# Build frontend image
cd frontend
docker build -t neurashield-frontend .
docker tag neurashield-frontend:latest <account-id>.dkr.ecr.<region>.amazonaws.com/neurashield-frontend:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/neurashield-frontend:latest
```

2. **Deploy Infrastructure**
```bash
# Use provided CloudFormation templates
aws cloudformation create-stack \
  --stack-name neurashield-infrastructure \
  --template-body file://infrastructure/aws/infrastructure.yml \
  --parameters ParameterKey=Environment,ParameterValue=production
```

3. **Deploy Application**
```bash
aws ecs update-service \
  --cluster neurashield-cluster \
  --service neurashield-api-service \
  --force-new-deployment
```

### Kubernetes Deployment

1. **Apply Kubernetes Manifests**
```bash
kubectl apply -f k8s/namespace.yml
kubectl apply -f k8s/configmap.yml
kubectl apply -f k8s/secrets.yml
kubectl apply -f k8s/postgres.yml
kubectl apply -f k8s/redis.yml
kubectl apply -f k8s/neo4j.yml
kubectl apply -f k8s/api.yml
kubectl apply -f k8s/frontend.yml
kubectl apply -f k8s/ingress.yml
```

2. **Verify Deployment**
```bash
kubectl get pods -n neurashield
kubectl get services -n neurashield
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@localhost:5432/neurashield` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `NEO4J_URI` | Neo4j connection URI | `bolt://localhost:7687` |
| `HUGGINGFACE_TOKEN` | HuggingFace API token | None |
| `PINECONE_API_KEY` | Pinecone API key | None |
| `SECRET_KEY` | JWT secret key | Random generated |

### Neural Shields Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `CODE_BRAIN_MODEL` | CodeBERT model name | `microsoft/codebert-base` |
| `SECURITY_SHIELD_THRESHOLD` | Security risk threshold | `0.7` |
| `DEVOPS_OPTIMIZER_LEARNING_RATE` | RL learning rate | `0.001` |

## 🔐 Security Setup

### SSL/TLS Configuration
```bash
# Generate SSL certificates
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Configure nginx with SSL
cp nginx/ssl.conf /etc/nginx/sites-available/neurashield
ln -s /etc/nginx/sites-available/neurashield /etc/nginx/sites-enabled/
```

### Database Security
```sql
-- Create dedicated database user
CREATE USER neurashield_app WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE neurashield TO neurashield_app;
GRANT USAGE ON SCHEMA public TO neurashield_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO neurashield_app;
```

## 📊 Monitoring Setup

### Prometheus Configuration
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'neurashield-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### Grafana Dashboards
- Import provided dashboard: `monitoring/grafana/neurashield-dashboard.json`
- Configure data source: Prometheus endpoint
- Set up alerts for critical metrics

## 🔄 CI/CD Integration

### GitHub Actions
```yaml
# Already configured in .github/workflows/neurashield-analysis.yml
# Customize for your repository and deployment targets
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    stages {
        stage('NeuraShield Analysis') {
            steps {
                sh 'neurashield analyze code --path .'
                sh 'neurashield scan security --path .'
                sh 'neurashield optimize pipeline --config Jenkinsfile'
            }
        }
        
        stage('Deploy') {
            when { branch 'main' }
            steps {
                sh 'docker-compose -f docker-compose.prod.yml up -d'
            }
        }
    }
}
```

## 🧪 Testing

### Run Tests
```bash
# Unit tests
pytest tests/

# Integration tests
pytest tests/integration/

# Load tests
locust -f tests/load/locustfile.py --host=http://localhost:8000
```

### Health Checks
```bash
# API health check
curl http://localhost:8000/health

# Database connectivity
curl http://localhost:8000/api/v1/health/db

# Neural shields status
curl http://localhost:8000/api/v1/health/shields
```

## 📈 Scaling

### Horizontal Scaling
```bash
# Scale API instances
docker-compose up -d --scale neurashield-api=3

# Scale Celery workers
docker-compose up -d --scale celery-worker=5
```

### Database Scaling
```sql
-- Read replicas for PostgreSQL
-- Configure in docker-compose.yml or cloud provider

-- Redis clustering
-- Configure Redis Cluster for high availability
```

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Issues**
```bash
# Check database status
docker-compose logs postgres

# Test connection
psql -h localhost -U postgres -d neurashield
```

2. **Memory Issues**
```bash
# Monitor memory usage
docker stats

# Increase memory limits in docker-compose.yml
```

3. **Model Loading Issues**
```bash
# Check HuggingFace token
echo $HUGGINGFACE_TOKEN

# Clear model cache
rm -rf ~/.cache/huggingface/
```

## 📞 Support

- **Documentation**: [docs.neurashield.ai](https://docs.neurashield.ai)
- **Issues**: [GitHub Issues](https://github.com/neurashield/neurashield-ai/issues)
- **Community**: [Discord Server](https://discord.gg/neurashield)
- **Email**: support@neurashield.ai