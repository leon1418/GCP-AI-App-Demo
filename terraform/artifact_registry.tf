resource "google_artifact_registry_repository" "app" {
  repository_id = var.app_name
  location      = var.region
  format        = "DOCKER"
  description   = "Docker images for ${var.app_name}"
}
