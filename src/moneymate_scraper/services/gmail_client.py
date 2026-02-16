"""Gmail API client with OAuth 2.0 authentication.

Handles the full Google OAuth flow:
1. Looks for a cached ``token.json`` for headless/automated runs.
2. If the token is expired, refreshes it automatically.
3. If no token exists, launches a local browser-based consent flow
   using ``credentials.json`` (downloaded from Google Cloud Console).

Security: Uses the **read-only** Gmail scope to protect the inbox.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource

from moneymate_scraper.config import settings

logger = logging.getLogger(__name__)

# Read-only scope — we never modify the user's mailbox.
SCOPES: list[str] = ["https://www.googleapis.com/auth/gmail.readonly"]


class GmailClient:
    """Thin wrapper around the Gmail API with automatic OAuth handling."""

    def __init__(
        self,
        credentials_path: Path | None = None,
        token_path: Path | None = None,
    ) -> None:
        self._credentials_path = credentials_path or settings.google_credentials_path
        self._token_path = token_path or settings.google_token_path
        self._service: Resource | None = None

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def authenticate(self) -> None:
        """Run the OAuth 2.0 flow and build the Gmail API service.

        * If ``token.json`` exists and is valid, reuse it.
        * If the token is expired but has a refresh token, refresh it.
        * Otherwise, launch the local consent flow via ``credentials.json``.
        """
        creds: Credentials | None = None

        # 1. Try loading cached token
        if self._token_path.exists():
            logger.info("Loading cached token from %s", self._token_path)
            creds = Credentials.from_authorized_user_file(
                str(self._token_path), SCOPES
            )

        # 2. Refresh or run full auth flow
        if creds and creds.expired and creds.refresh_token:
            logger.info("Token expired — refreshing…")
            creds.refresh(Request())
        elif not creds or not creds.valid:
            if not self._credentials_path.exists():
                raise FileNotFoundError(
                    f"OAuth credentials file not found at "
                    f"'{self._credentials_path}'. Download it from the "
                    f"Google Cloud Console and place it in the project root."
                )
            logger.info(
                "No valid token found — launching browser consent flow…"
            )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(self._credentials_path), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # 3. Persist the token for future runs
        if creds:
            self._token_path.write_text(creds.to_json())
            logger.info("Token saved to %s", self._token_path)

        # 4. Build the API service
        self._service = build("gmail", "v1", credentials=creds)
        logger.info("Gmail API service initialised successfully.")

    # ------------------------------------------------------------------
    # API helpers
    # ------------------------------------------------------------------

    @property
    def service(self) -> Resource:
        """Return the authenticated Gmail API resource.

        Raises:
            RuntimeError: If ``authenticate()`` has not been called yet.
        """
        if self._service is None:
            raise RuntimeError(
                "GmailClient is not authenticated. "
                "Call authenticate() first."
            )
        return self._service

    def fetch_recent_receipts(
        self,
        query: str = "from:(gojek OR grab OR bca OR mandiri) subject:(receipt OR bukti OR transfer)",
        max_results: int = 20,
    ) -> list[dict[str, Any]]:
        """Fetch recent receipt emails matching the given query.

        This is a placeholder that returns raw Gmail message metadata.
        The actual parsing logic will be implemented in ``receipt_parser.py``.

        Args:
            query: Gmail search query string.
            max_results: Maximum number of messages to retrieve.

        Returns:
            A list of raw Gmail message dicts (id, threadId, snippet, etc.).
        """
        logger.info("Searching Gmail with query: %s", query)
        results = (
            self.service.users()
            .messages()
            .list(userId="me", q=query, maxResults=max_results)
            .execute()
        )

        messages: list[dict[str, Any]] = results.get("messages", [])
        if not messages:
            logger.info("No receipt emails found.")
            return []

        logger.info("Found %d receipt email(s).", len(messages))

        # Fetch full message details for each hit
        detailed_messages: list[dict[str, Any]] = []
        for msg in messages:
            full_msg = (
                self.service.users()
                .messages()
                .get(userId="me", id=msg["id"], format="full")
                .execute()
            )
            detailed_messages.append(full_msg)

        return detailed_messages
