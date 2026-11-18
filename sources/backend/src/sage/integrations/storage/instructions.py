import logging
from google.cloud import storage
from sage.config import get_app_config

log = logging.getLogger(__name__)


def read_instructions() -> str:
    config = get_app_config()
    if not config.instructions_bucket:
        return ""
    try:
        client = storage.Client(project=config.project_id)
        blob = client.bucket(config.instructions_bucket).blob(config.instructions_object)
        return blob.download_as_text(encoding="utf-8")
    except Exception:
        log.warning("Impossibile leggere le istruzioni da Storage", exc_info=True)
        return ""