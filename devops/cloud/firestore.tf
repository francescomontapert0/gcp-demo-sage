resource "google_firestore_database" "sage" {
  project         = var.project_id
  name            = var.resource_prefix   # il codice usa il prefisso come nome del database
  location_id     = var.region
  type            = "FIRESTORE_NATIVE"
  deletion_policy = "DELETE"
  depends_on      = [google_project_service.apis]
}

resource "google_firestore_index" "chunks_embedding" {
  project     = var.project_id
  database    = google_firestore_database.sage.name
  collection  = "chunks"
  query_scope = "COLLECTION"

  fields {
    field_path = "embedding"
    vector_config {
      dimension = 768
      flat {}
    }
  }

  lifecycle {
    ignore_changes = [fields]
  }
}