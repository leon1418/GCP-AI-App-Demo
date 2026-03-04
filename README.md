# GCP AI Dog Breed Detector

Upload a dog photo and get instant breed identification powered by Google Gemini AI.

## Architecture

| Component | Technology |
|-----------|-----------|
| Backend | Python + FastAPI |
| Frontend | Vanilla HTML/CSS/JS |
| AI Model | Gemini 2.0 Flash |
| Image Storage | Google Cloud Storage |
| Query History | Firestore |
| Infrastructure | Terraform (GKE Autopilot) |
| Deployment | Docker + Kubernetes |

## Quick Start

### Prerequisites

- Python 3.12+, [uv](https://github.com/astral-sh/uv)
- GCP project with Gemini API, GCS, and Firestore enabled
- `gcloud` CLI authenticated

### Local Development

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your GCP project ID and bucket name

# Run dev server
uv run uvicorn app.main:app --reload
```

Open http://localhost:8000

### Deploy to GKE

```bash
# Provision infrastructure
cd terraform
terraform init
terraform plan -var="project_id=YOUR_PROJECT" -var="gcs_bucket_name=YOUR_BUCKET"
terraform apply

# Build and push Docker image
docker build -t gcr.io/YOUR_PROJECT/dog-breed-detector .
docker push gcr.io/YOUR_PROJECT/dog-breed-detector

# Update kubernetes/configmap.yaml with your values, then:
kubectl apply -f kubernetes/
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Web interface |
| POST | `/api/upload` | Upload image for breed detection |
| GET | `/api/history?limit=20` | Session query history |
| GET | `/api/health` | Health check |

## Data Flow

```
Upload image → GCS storage → Gemini Vision API → Parse breeds → Save to Firestore → Display results
```
