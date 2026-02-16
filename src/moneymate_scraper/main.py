"""MoneyMate Scraper — entry point.

Usage:
    python -m moneymate_scraper.main
"""

from __future__ import annotations

import logging
import sys

from moneymate_scraper.config import settings
from moneymate_scraper.services.gmail_client import GmailClient
from moneymate_scraper.services.receipt_parser import ReceiptParser


def setup_logging() -> None:
    """Configure root logger based on the LOG_LEVEL setting."""
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )


def main() -> None:
    """Authenticate with Gmail, fetch receipts, and parse them."""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("🚀 MoneyMate Scraper starting…")

    # 1. Authenticate
    client = GmailClient()
    client.authenticate()

    # 2. Fetch recent receipt emails
    raw_messages = client.fetch_recent_receipts()
    logger.info("Fetched %d raw message(s).", len(raw_messages))

    # 3. Parse each message (placeholder for now)
    parser = ReceiptParser()
    for msg in raw_messages:
        transaction = parser.parse(msg)
        if transaction:
            logger.info("Parsed transaction: %s", transaction.model_dump_json())

    logger.info("✅ Done.")


if __name__ == "__main__":
    main()
