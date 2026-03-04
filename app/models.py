from pydantic import BaseModel


class DetectedDog(BaseModel):
    breed: str
    confidence: str
    description: str
    breed_info: str = ""


class AnalysisResults(BaseModel):
    detected_dogs: list[DetectedDog]
    no_dogs_detected: bool = False


class UploadResponse(BaseModel):
    query_id: str
    image_url: str
    results: AnalysisResults


class HistoryItem(BaseModel):
    query_id: str
    image_url: str
    results: AnalysisResults
    timestamp: str


class HistoryResponse(BaseModel):
    items: list[HistoryItem]


class HealthResponse(BaseModel):
    status: str = "ok"
