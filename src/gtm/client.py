"""GTM API client wrapper."""

import os
import time

import google.auth
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GTMClient:
    """Thin wrapper around the GTM API v2 with retry logic."""

    SCOPES = [
        "https://www.googleapis.com/auth/tagmanager.readonly",
        "https://www.googleapis.com/auth/tagmanager.edit.containers",
        "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
        "https://www.googleapis.com/auth/tagmanager.publish",
    ]

    def __init__(self, account_id: str | None = None):
        self.account_id = account_id or os.environ.get("GTM_ACCOUNT_ID", "6002017930")
        self._service = None

    @property
    def service(self):
        if self._service is None:
            credentials, _ = google.auth.default(scopes=self.SCOPES)
            credentials.refresh(Request())
            self._service = build("tagmanager", "v2", credentials=credentials)
        return self._service

    @property
    def account_path(self) -> str:
        return f"accounts/{self.account_id}"

    def execute_with_retry(self, request, max_retries: int = 3):
        """Execute an API request with exponential backoff on rate limits."""
        for attempt in range(max_retries):
            try:
                return request.execute()
            except HttpError as e:
                if e.resp.status == 429 and attempt < max_retries - 1:
                    wait = 2 ** (attempt + 1)
                    time.sleep(wait)
                    continue
                raise
