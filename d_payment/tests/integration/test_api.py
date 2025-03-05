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
        assert response.json()["success"] is True
        assert "processed successfully" in response.json()["message"]
        assert response.json()["data"]["responseCode"] == "0000"


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


def test_health_check(client):
    """
    ヘルスチェックエンドポイントをテストします。
    """
    response = client.get("/api/payment/health")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "ok"
