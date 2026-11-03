resource "google_storage_bucket" "sage_docs" {
  name                     = "${var.resource_prefix}-sage-docs"
  location                 = var.region
  force_destroy            = true
  public_access_prevention = "enforced"

  uniform_bucket_level_access = true

  force_destroy = True
}