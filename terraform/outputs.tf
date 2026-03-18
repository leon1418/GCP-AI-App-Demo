output "cloud_run_url" {
  description = "The URL of the Cloud Run service"
  value       = google_cloud_run_v2_service.app.uri
}

output "gcs_bucket_url" {
  description = "The URL of the GCS bucket"
  value       = google_storage_bucket.app_bucket.url
}

output "service_account_email" {
  description = "The email of the application service account"
  value       = google_service_account.app_sa.email
}

output "artifact_registry_url" {
  description = "The Docker registry URL for the application"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.app.repository_id}"
}
