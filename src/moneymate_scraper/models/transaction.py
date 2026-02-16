"""Transaction data models for parsed receipts."""

from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class TransactionSource(str, Enum):
    """Supported receipt sources."""

    GOJEK = "gojek"
    GRAB = "grab"
    BANK_TRANSFER = "bank_transfer"
    UNKNOWN = "unknown"


class Transaction(BaseModel):
    """A single parsed transaction extracted from an email receipt."""

    source: TransactionSource = TransactionSource.UNKNOWN
    description: str = Field(..., min_length=1, description="Transaction description")
    amount: Decimal = Field(..., description="Transaction amount in original currency")
    currency: str = Field(default="IDR", max_length=3, description="ISO 4217 currency code")
    transaction_date: datetime = Field(..., description="When the transaction occurred")
    email_id: str = Field(..., description="Gmail message ID for traceability")
    raw_subject: str = Field(default="", description="Original email subject line")

    class Config:
        """Pydantic model configuration."""

        json_encoders = {Decimal: str}
