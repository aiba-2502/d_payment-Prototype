"""
API依存性モジュール。

FastAPIの依存性注入で使用する依存関係を定義します。
"""

from __future__ import annotations

from fastapi import Depends

from app.domain.interfaces.payment_service import PaymentServiceInterface
from app.infrastructure.payment.spmode_service import SpmodePaymentService


def get_payment_service() -> PaymentServiceInterface:
    """
    決済サービスを取得します。

    依存性注入で使用します。

    Returns:
        PaymentServiceInterface: 決済サービスのインスタンス
    """
    return SpmodePaymentService.create()
