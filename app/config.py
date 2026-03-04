from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gcp_project_id: str = ""
    gcs_bucket_name: str = ""
    gcp_region: str = "us-central1"
    gemini_model: str = "gemini-2.0-flash-001"

    model_config = {"env_file": ".env"}


settings = Settings()
