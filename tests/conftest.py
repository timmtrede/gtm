"""Shared test fixtures."""

from unittest.mock import MagicMock, patch

import pytest

from gtm.client import GTMClient


@pytest.fixture
def mock_service():
    """Mock the GTM API service."""
    with patch.object(GTMClient, "service", new_callable=lambda: property(lambda self: MagicMock())) as mock:
        yield mock


@pytest.fixture
def client():
    """Create a GTMClient with a mocked service."""
    c = GTMClient(account_id="6002017930")
    c._service = MagicMock()
    return c
