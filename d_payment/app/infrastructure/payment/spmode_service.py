"""
spmode決済サービスモジュール。

spmode決済サービスとの連携を実装します。
"""

from __future__ import annotations

import logging
from typing import Dict, Any

from app.domain.interfaces.payment_service import (
    PaymentServiceInterface,
    HttpClientInterface,
)
from app.application.payment_service import PaymentService
from app.infrastructure.http_client import HttpClient

logger = logging.getLogger(__name__)


class SpmodePaymentService:
    """
    spmode決済サービスファクトリ。

    spmode決済サービスのインスタンスを生成します。
    """

    @staticmethod
    def create() -> PaymentServiceInterface:
        """
        spmode決済サービスのインスタンスを生成します。

        Returns:
            PaymentServiceInterface: spmode決済サービスのインスタンス
        """
        http_client = HttpClient()
        return PaymentService(http_client)
