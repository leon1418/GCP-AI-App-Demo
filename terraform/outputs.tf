output "gke_cluster_name" {
  description = "The name of the GKE Autopilot cluster"
  value       = google_container_cluster.primary.name
}

output "gke_cluster_endpoint" {
  description = "The endpoint of the GKE Autopilot cluster"
  value       = google_container_cluster.primary.endpoint
  sensitive   = true
}

output "gcs_bucket_url" {
  description = "The URL of the GCS bucket"
  value       = google_storage_bucket.app_bucket.url
}

output "service_account_email" {
  description = "The email of the application service account"
  value       = google_service_account.app_sa.email
}
