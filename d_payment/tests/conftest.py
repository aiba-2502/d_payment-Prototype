"""
テスト設定モジュール。

pytest用の設定とフィクスチャを提供します。
"""

from __future__ import annotations

import asyncio
import pytest
from typing import Dict, Any, Generator
from fastapi.testclient import TestClient

from app.main import app
from app.domain.interfaces.payment_service import (
    PaymentServiceInterface,
    HttpClientInterface,
)
from app.domain.entities.payment import PaymentResponse


class MockHttpClient(HttpClientInterface):
    """
    HTTPクライアントのモック。

    テスト用にHTTPクライアントの動作をモックします。
    """

    def __init__(self, response_data: Dict[str, Any] = None):
        """
        初期化メソッド。

        Args:
            response_data: モックレスポンスデータ
        """
        self.response_data = response_data or {"status": "success"}
        self.last_url = None
        self.last_data = None

    async def post(
        self, url: str, data: Dict[str, Any], timeout: int = 30
    ) -> Dict[str, Any]:
        """
        POSTリクエストのモック。

        Args:
            url: 送信先URL
            data: 送信データ
            timeout: タイムアウト秒数

        Returns:
            Dict[str, Any]: モックレスポンスデータ
        """
        self.last_url = url
        self.last_data = data
        return self.response_data


class MockPaymentService(PaymentServiceInterface):
    """
    決済サービスのモック。

    テスト用に決済サービスの動作をモックします。
    """

    def __init__(self, response: PaymentResponse = None):
        """
        初期化メソッド。

        Args:
            response: モックレスポンス
        """
        self.response = response or PaymentResponse(
            success=True,
            message="Payment request processed successfully",
            data={"status": "success"},
        )
        self.last_request_data = None

    async def process_payment(self, request_data: Dict[str, Any]) -> PaymentResponse:
        """
        決済リクエスト処理のモック。

        Args:
            request_data: リクエストデータ

        Returns:
            PaymentResponse: モックレスポンス
        """
        self.last_request_data = request_data
        return self.response


@pytest.fixture
def mock_http_client() -> MockHttpClient:
    """
    HTTPクライアントモックのフィクスチャ。

    Returns:
        MockHttpClient: HTTPクライアントモック
    """
    return MockHttpClient()


@pytest.fixture
def mock_payment_service() -> MockPaymentService:
    """
    決済サービスモックのフィクスチャ。

    Returns:
        MockPaymentService: 決済サービスモック
    """
    return MockPaymentService()


@pytest.fixture
def client() -> Generator:
    """
    テストクライアントのフィクスチャ。

    FastAPIのテストクライアントを提供します。

    Returns:
        Generator: テストクライアントのジェネレータ
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def event_loop():
    """
    非同期テスト用のイベントループフィクスチャ。

    セッションスコープでイベントループを提供します。

    Returns:
        asyncio.AbstractEventLoop: イベントループ
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
