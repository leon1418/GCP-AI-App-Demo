# GCP AI Dog Breed Detector

Upload a dog photo and get instant breed identification powered by Google Gemini AI.

## Architecture

| Component | Technology |
|-----------|-----------|
| Backend | Python + FastAPI |
| Frontend | Vanilla HTML/CSS/JS |
| AI Model | Gemini 2.0 Flash |
| Auth | Firebase Authentication (Google sign-in) |
| Image Storage | Google Cloud Storage |
| Query History | Firestore |
| Infrastructure | Terraform (Cloud Run) |
| Deployment | Docker + Cloud Run |

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

### Deploy to Cloud Run

```bash
# Provision infrastructure
cd terraform
terraform init
terraform plan
terraform apply

# Build and push Docker image
docker build --platform linux/amd64 -t REGION-docker.pkg.dev/PROJECT_ID/dog-breed-detector/app:v1 .
docker push REGION-docker.pkg.dev/PROJECT_ID/dog-breed-detector/app:v1

# Deploy to Cloud Run
gcloud run deploy dog-breed-detector \
  --image=REGION-docker.pkg.dev/PROJECT_ID/dog-breed-detector/app:v1 \
  --service-account=dog-breed-detector-sa@PROJECT_ID.iam.gserviceaccount.com \
  --set-env-vars="GCP_PROJECT_ID=PROJECT_ID,GCS_BUCKET_NAME=BUCKET_NAME,GCP_REGION=REGION,GEMINI_MODEL=gemini-2.0-flash-001" \
  --port=8000 --allow-unauthenticated --region=REGION
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Web interface |
| POST | `/api/upload` | Upload image for breed detection |
| GET | `/api/history?limit=20` | Session query history |
| DELETE | `/api/history/{query_id}` | Delete a query |
| GET | `/api/health` | Health check |

## Data Flow

```
Upload image → GCS storage → Gemini Vision API → Parse breeds → Save to Firestore → Display results
```
