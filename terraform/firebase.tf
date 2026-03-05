resource "google_firebase_project" "default" {
  provider = google-beta
  project  = var.project_id
}

resource "google_firebase_web_app" "default" {
  provider     = google-beta
  project      = var.project_id
  display_name = "Dog Breed Detector"

  depends_on = [google_firebase_project.default]
}

resource "google_identity_platform_config" "default" {
  provider = google-beta
  project  = var.project_id

  authorized_domains = [
    "localhost",
    "${var.project_id}.firebaseapp.com",
    "${var.project_id}.web.app",
    "34.68.95.255",
    "34.68.95.255.nip.io",
  ]

  sign_in {
    allow_duplicate_emails = false
  }

  depends_on = [google_firebase_project.default]
}

resource "google_identity_platform_default_supported_idp_config" "google" {
  provider      = google-beta
  project       = var.project_id
  enabled       = true
  idp_id        = "google.com"
  client_id     = var.firebase_google_client_id
  client_secret = var.firebase_google_client_secret

  depends_on = [google_identity_platform_config.default]
}
