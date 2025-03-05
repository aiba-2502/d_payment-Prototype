"""
決済スキーマモジュール。

決済リクエスト・レスポンスのスキーマを定義します。
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class RegiChargeRequestItemSchema(BaseModel):
    """
    決済リクエスト項目のスキーマ。
    """

    storeOrderNumber: str = Field(..., description="店舗注文番号")
    settlementAmount: str = Field(..., description="決済金額")
    displayContents1: str = Field(..., description="表示内容1")
    displayContents2: str = Field(..., description="表示内容2")


class SpModePaymentSchema(BaseModel):
    """
    外部APIに送信する決済リクエストスキーマ。
    """

    companyCode: str = Field(..., description="会社コード")
    storeCode: str = Field(..., description="店舗コード")
    authenticationPass: str = Field(..., description="認証パスワード")
    transactionId: str = Field(..., description="トランザクションID")
    reqTimestamp: str = Field(..., description="リクエストタイムスタンプ")
    execMode: str = Field(..., description="実行モード")
    billingToken: str = Field(..., description="請求トークン")
    regiChargeReqList: List[RegiChargeRequestItemSchema] = Field(
        ..., description="決済リクエストリスト"
    )


class PaymentRequestSchema(BaseModel):
    """
    受信する決済リクエストスキーマ。

    任意の形式のデータを受け取るための柔軟なスキーマです。
    """

    data: Dict[str, Any] = Field(..., description="受信したリクエストデータ")

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "userInfo": {"userId": "user123", "name": "山田太郎"},
                    "paymentInfo": {
                        "amount": 3980,
                        "orderNumber": "ORDER12345",
                        "description": "商品購入",
                    },
                }
            }
        }


class PaymentResponseSchema(BaseModel):
    """
    決済レスポンススキーマ。

    APIレスポンスとして返すデータ構造を定義します。
    """

    success: bool = Field(..., description="処理成功フラグ")
    message: str = Field(..., description="レスポンスメッセージ")
    data: Optional[Dict[str, Any]] = Field(None, description="レスポンスデータ")
    error: Optional[str] = Field(None, description="エラーメッセージ")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Payment request processed successfully",
                "data": {"responseCode": "0000", "responseMessage": "Success"},
            }
        }
