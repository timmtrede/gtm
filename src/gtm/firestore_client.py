"""Firestore client wrapper for accessing GTM server container data."""

import os
from pathlib import Path

from google.cloud import firestore
from google.oauth2.service_account import Credentials


class FirestoreClient:
    """Thin wrapper around Firestore with service account auth."""

    SCOPES = [
        "https://www.googleapis.com/auth/datastore",
    ]

    def __init__(self, project: str | None = None, credentials_path: str | None = None):
        self.project = project or os.environ.get("GCP_PROJECT", "zipmend-2e643")
        self.credentials_path = credentials_path or os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS",
            str(Path(__file__).resolve().parents[2] / ".credentials.json"),
        )
        self._db = None

    @property
    def db(self) -> firestore.Client:
        if self._db is None:
            credentials = Credentials.from_service_account_file(self.credentials_path, scopes=self.SCOPES)
            self._db = firestore.Client(project=self.project, credentials=credentials)
        return self._db
