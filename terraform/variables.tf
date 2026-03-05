variable "project_id" {
  description = "The GCP project ID to deploy resources into"
  type        = string
}

variable "region" {
  description = "The GCP region for resource deployment"
  type        = string
  default     = "us-central1"
}

variable "app_name" {
  description = "The application name used for resource naming"
  type        = string
  default     = "dog-breed-detector"
}

variable "gcs_bucket_name" {
  description = "The globally unique name for the GCS bucket"
  type        = string
}

variable "firebase_google_client_id" {
  description = "OAuth 2.0 client ID for Firebase Google sign-in"
  type        = string
}

variable "firebase_google_client_secret" {
  description = "OAuth 2.0 client secret for Firebase Google sign-in"
  type        = string
  sensitive   = true
}
