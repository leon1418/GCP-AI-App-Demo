resource "google_container_cluster" "primary" {
  name     = "${var.app_name}-cluster"
  location = var.region

  enable_autopilot = true

  network    = "default"
  subnetwork = "default"

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  release_channel {
    channel = "REGULAR"
  }

  deletion_protection = false

  depends_on = [google_project_service.apis["container.googleapis.com"]]
}
