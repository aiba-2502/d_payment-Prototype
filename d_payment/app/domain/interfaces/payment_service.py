"""
決済サービスインターフェースモジュール。

決済サービスのインターフェースを定義します。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Any

from app.domain.entities.payment import PaymentRequest, PaymentResponse


class PaymentServiceInterface(ABC):
    """
    決済サービスインターフェース。

    決済処理のためのインターフェースを定義します。
    """

    @abstractmethod
    async def process_payment(self, request_data: Dict[str, Any]) -> PaymentResponse:
        """
        決済リクエストを処理します。

        Args:
            request_data: 受信した決済リクエストデータ

        Returns:
            PaymentResponse: 処理結果
        """
        pass


class HttpClientInterface(ABC):
    """
    HTTPクライアントインターフェース。

    外部APIとの通信を行うためのインターフェースを定義します。
    """

    @abstractmethod
    async def post(
        self, url: str, data: Dict[str, Any], timeout: int = 30
    ) -> Dict[str, Any]:
        """
        POSTリクエストを送信します。

        Args:
            url: 送信先URL
            data: 送信データ
            timeout: タイムアウト秒数

        Returns:
            Dict[str, Any]: レスポンスデータ
        """
        pass
