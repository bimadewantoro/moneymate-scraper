"""Receipt parsing service — converts raw Gmail messages into Transaction models.

This module will contain source-specific parsers for:
- Gojek receipts
- Grab receipts
- Bank transfer confirmations (BCA, Mandiri, etc.)

TODO: Implement parsers in a future iteration.
"""

from __future__ import annotations

import logging
from typing import Any

from moneymate_scraper.models.transaction import Transaction

logger = logging.getLogger(__name__)


class ReceiptParser:
    """Parses raw Gmail message payloads into structured Transaction objects."""

    def parse(self, raw_message: dict[str, Any]) -> Transaction | None:
        """Attempt to parse a raw Gmail message into a Transaction.

        Args:
            raw_message: A full Gmail message dict (format="full").

        Returns:
            A ``Transaction`` if parsing succeeds, or ``None`` if the
            message format is unrecognised.
        """
        # TODO: Implement source detection and per-source parsing logic.
        logger.warning(
            "ReceiptParser.parse() is not yet implemented. "
            "Skipping message id=%s",
            raw_message.get("id", "unknown"),
        )
        return None
