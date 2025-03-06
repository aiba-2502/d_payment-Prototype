"""
決済スキーマモジュール。

決済リクエスト・レスポンスのスキーマを定義します。
このモジュールでは、APIで使用するデータの構造を定義しています。
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class RegiChargeRequestItemSchema(BaseModel):
    """
    決済リクエスト項目のスキーマ。
    
    外部APIに送信する決済リクエストの明細項目を定義します。
    """

    storeOrderNumber: str = Field(..., description="店舗注文番号 - 注文を識別するための番号")
    settlementAmount: str = Field(..., description="決済金額 - 決済する金額（文字列形式）")
    displayContents1: str = Field(..., description="表示内容1 - 決済画面に表示する内容（商品名など）")
    displayContents2: str = Field(..., description="表示内容2 - 決済画面に表示する追加情報")


class DPaymentSchema(BaseModel):
    """
    外部APIに送信する決済リクエストスキーマ。
    
    外部決済APIに送信するリクエストの全体構造を定義します。
    """

    companyCode: str = Field(..., description="会社コード - 決済会社を識別するコード")
    storeCode: str = Field(..., description="店舗コード - 店舗を識別するコード")
    authenticationPass: str = Field(..., description="認証パスワード - API認証用のパスワード")
    transactionId: str = Field(..., description="トランザクションID - 取引を識別するID")
    reqTimestamp: str = Field(..., description="リクエストタイムスタンプ - リクエスト送信時刻（ISO 8601形式）")
    execMode: str = Field(..., description="実行モード - 決済処理のモード（本番/テストなど）")
    billingToken: str = Field(..., description="請求トークン - 決済に使用するトークン")
    regiChargeReqList: List[RegiChargeRequestItemSchema] = Field(
        ..., description="決済リクエストリスト - 決済明細項目のリスト"
    )


class PaymentRequestSchema(BaseModel):
    """
    受信する決済リクエストスキーマ。

    クライアントからのリクエストを受け取るための柔軟なスキーマです。
    任意の形式のデータを受け取ることができます。
    
    主な項目:
    - billingToken: 請求トークン
    - paymentInfo: 決済情報（amount, orderNumber, description, displayContents1, displayContents2）
    """

    data: Dict[str, Any] = Field(..., description="受信したリクエストデータ - クライアントから送信されたデータ")

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "billingToken": "9000000248250856006510",
                    "paymentInfo": {
                        "amount": 3980,
                        "orderNumber": "ORDER12345",
                        "description": "商品購入",
                        "displayContents1": "商品購入",
                        "displayContents2": "オンラインストア"
                    }
                }
            }
        }


class PaymentResponseSchema(BaseModel):
    """
    決済レスポンススキーマ。

    APIレスポンスとして返すデータ構造を定義します。
    現在は外部APIからのレスポンスをそのまま返すため、このスキーマは直接使用されていません。
    """

    success: bool = Field(..., description="処理成功フラグ - 処理が成功したかどうか")
    message: str = Field(..., description="レスポンスメッセージ - 処理結果の説明")
    data: Optional[Dict[str, Any]] = Field(None, description="レスポンスデータ - 外部APIからのレスポンスデータ")
    error: Optional[str] = Field(None, description="エラーメッセージ - エラーが発生した場合のメッセージ")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "決済リクエストが正常に処理されました",
                "data": {"responseCode": "0000", "responseMessage": "Success"},
            }
        }
