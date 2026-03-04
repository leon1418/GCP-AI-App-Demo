resource "google_service_account" "app_sa" {
  account_id   = "${var.app_name}-sa"
  display_name = "Dog Breed Detector Application Service Account"
  description  = "Service account used by the ${var.app_name} application"
}

# GCS object admin - read/write access to storage buckets
resource "google_project_iam_member" "sa_storage_admin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.app_sa.email}"
}

# Firestore datastore user - read/write access to Firestore
resource "google_project_iam_member" "sa_datastore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.app_sa.email}"
}

# Vertex AI platform user - access to Gemini and Vertex AI services
resource "google_project_iam_member" "sa_aiplatform_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.app_sa.email}"
}

# Workload Identity binding - allows the Kubernetes service account to
# impersonate the GCP service account
resource "google_service_account_iam_member" "workload_identity_binding" {
  service_account_id = google_service_account.app_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[default/${var.app_name}-ksa]"

  depends_on = [google_container_cluster.primary]
}
