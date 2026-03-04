import json

from google import genai
from google.genai.types import Part

from app.config import settings
from app.models import AnalysisResults, DetectedDog

PROMPT = """Analyze this image and identify any dog breeds present.

Return your response as valid JSON with this exact structure:
{
  "detected_dogs": [
    {
      "breed": "Breed Name",
      "confidence": "high|medium|low",
      "description": "Brief description of the dog in the image",
      "breed_info": "2-3 sentence introduction about this breed: origin, temperament, and notable traits"
    }
  ],
  "no_dogs_detected": false
}

If no dogs are detected in the image, return:
{
  "detected_dogs": [],
  "no_dogs_detected": true
}

Return ONLY the JSON, no other text."""


def get_client() -> genai.Client:
    return genai.Client(vertexai=True, project=settings.gcp_project_id, location=settings.gcp_region)


def analyze_image(gcs_uri: str) -> AnalysisResults:
    """Send image to Gemini for breed analysis."""
    client = get_client()

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=[
            Part.from_uri(file_uri=gcs_uri, mime_type="image/jpeg"),
            PROMPT,
        ],
    )

    return _parse_response(response.text)


def _parse_response(text: str) -> AnalysisResults:
    """Parse Gemini's JSON response into AnalysisResults."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
        cleaned = cleaned.rsplit("```", 1)[0]
    cleaned = cleaned.strip()

    data = json.loads(cleaned)

    dogs = [DetectedDog(**dog) for dog in data.get("detected_dogs", [])]
    return AnalysisResults(
        detected_dogs=dogs,
        no_dogs_detected=data.get("no_dogs_detected", len(dogs) == 0),
    )
