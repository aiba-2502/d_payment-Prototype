"""
決済サービスのテストモジュール。

決済サービスの単体テストを提供します。
"""

from __future__ import annotations

import pytest
from typing import Dict, Any

from app.application.payment_service import PaymentService
from app.domain.entities.payment import PaymentResponse
from tests.conftest import MockHttpClient


@pytest.mark.asyncio
async def test_process_payment_success():
    """
    決済処理の成功ケースをテストします。
    """
    # モックの準備
    mock_response = {"status": "success", "responseCode": "0000"}
    http_client = MockHttpClient(mock_response)
    payment_service = PaymentService(http_client)

    # テスト対象データ
    request_data = {
        "billingToken": "9000000248250856006510",
        "paymentInfo": {
            "amount": 3980,
            "orderNumber": "TEST12345",
            "description": "テスト決済",
            "displayContents1": "カスタム表示1",
            "displayContents2": "カスタム表示2"
        }
    }

    # テスト実行
    response = await payment_service.process_payment(request_data)

    # アサーション
    assert isinstance(response, PaymentResponse)
    assert response.success is True
    assert "processed successfully" in response.message
    assert response.data == mock_response

    # 変換されたリクエストデータのチェック
    assert "companyCode" in http_client.last_data
    assert "storeCode" in http_client.last_data
    assert "authenticationPass" in http_client.last_data
    assert "regiChargeReqList" in http_client.last_data
    assert http_client.last_data["billingToken"] == "9000000248250856006510"

    # 変換されたリクエストの詳細チェック
    charge_req = http_client.last_data["regiChargeReqList"][0]
    assert charge_req["storeOrderNumber"] == "TEST12345"
    assert charge_req["settlementAmount"] == "3980"
    assert charge_req["displayContents1"] == "カスタム表示1"
    assert charge_req["displayContents2"] == "カスタム表示2"


@pytest.mark.asyncio
async def test_process_payment_with_default_values():
    """
    デフォルト値を使用した決済処理をテストします。
    """
    # モックの準備
    mock_response = {"status": "success", "responseCode": "0000"}
    http_client = MockHttpClient(mock_response)
    payment_service = PaymentService(http_client)

    # 最小限のテスト対象データ
    request_data = {
        "paymentInfo": {
            "amount": 3980,
            "orderNumber": "TEST12345",
            "description": "テスト決済",
        }
    }

    # テスト実行
    response = await payment_service.process_payment(request_data)

    # アサーション
    assert isinstance(response, PaymentResponse)
    assert response.success is True

    # 変換されたリクエストの詳細チェック
    charge_req = http_client.last_data["regiChargeReqList"][0]
    assert charge_req["displayContents1"] == "テスト決済"
    assert charge_req["displayContents2"] == ""
    assert http_client.last_data["billingToken"] == "9000000248250856006510"


@pytest.mark.asyncio
async def test_process_payment_error_handling():
    """
    決済処理のエラーハンドリングをテストします。
    """

    # HTTPクライアントがエラーを返す場合のモック
    class ErrorHttpClient(MockHttpClient):
        async def post(
            self, url: str, data: Dict[str, Any], timeout: int = 30
        ) -> Dict[str, Any]:
            self.last_url = url
            self.last_data = data
            raise Exception("Test exception")

    # モックの準備
    http_client = ErrorHttpClient()
    payment_service = PaymentService(http_client)

    # テスト対象データ
    request_data = {
        "paymentInfo": {
            "amount": 3980,
            "orderNumber": "TEST12345",
            "description": "テスト決済",
        }
    }

    # テスト実行
    response = await payment_service.process_payment(request_data)

    # アサーション
    assert isinstance(response, PaymentResponse)
    assert response.success is False
    assert "error" in response.message.lower()
    assert response.error is not None
    assert "Test exception" in response.error
