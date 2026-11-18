resource "google_storage_bucket" "instructions" {
  name                        = "${var.resource_prefix}-instructions"
  project                     = var.project_id
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = true
}

resource "google_storage_bucket_iam_member" "sage_run_reads_instructions" {
  bucket = google_storage_bucket.instructions.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.sage_run.email}"
}