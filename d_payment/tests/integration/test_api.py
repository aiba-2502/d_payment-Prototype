"""
API統合テストモジュール。

APIエンドポイントの統合テストを提供します。
"""

from __future__ import annotations

import pytest
from fastapi import status
from unittest.mock import patch

from app.domain.entities.payment import PaymentResponse
from tests.conftest import MockPaymentService


def test_receive_payment_success(client):
    """
    決済リクエスト受信エンドポイントの成功ケースをテストします。
    """
    # PaymentServiceをモックに置き換え
    mock_service = MockPaymentService(
        PaymentResponse(
            success=True,
            message="Payment request processed successfully",
            data={"responseCode": "0000", "responseMessage": "Success"},
        )
    )

    with patch(
        "app.interfaces.api.dependencies.get_payment_service", return_value=mock_service
    ):
        # リクエストデータ
        request_data = {
            "data": {
                "billingToken": "9000000248250856006510",
                "paymentInfo": {
                    "amount": 3980,
                    "orderNumber": "TEST12345",
                    "description": "テスト決済",
                    "displayContents1": "カスタム表示1",
                    "displayContents2": "カスタム表示2"
                }
            }
        }

        # APIリクエスト実行
        response = client.post("/api/payment/receive", json=request_data)

        # アサーション
        assert response.status_code == status.HTTP_200_OK
        # 外部APIからのレスポンスがそのまま返されるため、
        # レスポンスはmock_serviceのdataフィールドと同じになる
        assert response.json() == {"responseCode": "0000", "responseMessage": "Success"}

        # リクエストデータが正しく処理されたことを確認
        assert mock_service.last_request_data == request_data["data"]


def test_receive_payment_with_minimal_data(client):
    """
    最小限のデータでの決済リクエスト受信をテストします。
    """
    # PaymentServiceをモックに置き換え
    mock_service = MockPaymentService(
        PaymentResponse(
            success=True,
            message="Payment request processed successfully",
            data={"responseCode": "0000", "responseMessage": "Success"},
        )
    )

    with patch(
        "app.interfaces.api.dependencies.get_payment_service", return_value=mock_service
    ):
        # 最小限のリクエストデータ
        request_data = {
            "data": {
                "paymentInfo": {
                    "amount": 3980,
                    "orderNumber": "TEST12345",
                    "description": "テスト決済",
                }
            }
        }

        # APIリクエスト実行
        response = client.post("/api/payment/receive", json=request_data)

        # アサーション
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"responseCode": "0000", "responseMessage": "Success"}

        # リクエストデータが正しく処理されたことを確認
        assert mock_service.last_request_data == request_data["data"]


def test_receive_payment_error(client):
    """
    決済リクエスト受信エンドポイントのエラーケースをテストします。
    """
    # PaymentServiceをモックに置き換え（エラーレスポンスを返す）
    mock_service = MockPaymentService(
        PaymentResponse(
            success=False,
            message="Payment processing error",
            error="External API error",
        )
    )

    with patch(
        "app.interfaces.api.dependencies.get_payment_service", return_value=mock_service
    ):
        # リクエストデータ
        request_data = {
            "data": {
                "paymentInfo": {
                    "amount": 3980,
                    "orderNumber": "TEST12345",
                    "description": "テスト決済",
                }
            }
        }

        # APIリクエスト実行
        response = client.post("/api/payment/receive", json=request_data)

        # アサーション
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        assert "External API error" in response.json()["detail"]
