"""BigQuery client wrapper for querying Zipmend data warehouse."""

import os
from pathlib import Path

from google.cloud import bigquery
from google.oauth2.service_account import Credentials


class BigQueryClient:
    """Thin wrapper around BigQuery with service account auth."""

    SCOPES = [
        "https://www.googleapis.com/auth/bigquery",
    ]

    def __init__(self, project: str | None = None, credentials_path: str | None = None):
        self.project = project or os.environ.get("GCP_PROJECT", "zipmend-2e643")
        self.credentials_path = credentials_path or os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS",
            str(Path(__file__).resolve().parents[2] / ".credentials.json"),
        )
        self._client = None

    @property
    def client(self) -> bigquery.Client:
        if self._client is None:
            credentials = Credentials.from_service_account_file(self.credentials_path, scopes=self.SCOPES)
            self._client = bigquery.Client(project=self.project, credentials=credentials)
        return self._client
