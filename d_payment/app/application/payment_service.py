"""
決済サービス実装モジュール。

決済処理のユースケースを実装します。
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Dict, Any, List

from app.core.config import settings
from app.domain.entities.payment import (
    PaymentRequest,
    PaymentResponse,
    RegiChargeRequestItem,
)
from app.domain.interfaces.payment_service import (
    PaymentServiceInterface,
    HttpClientInterface,
)

logger = logging.getLogger(__name__)


class PaymentService(PaymentServiceInterface):
    """
    決済サービスの実装。

    決済処理のユースケースを実装します。
    """

    def __init__(self, http_client: HttpClientInterface):
        """
        初期化メソッド。

        Args:
            http_client: HTTPクライアントインターフェース
        """
        self._http_client = http_client

    async def process_payment(self, request_data: Dict[str, Any]) -> PaymentResponse:
        """
        決済リクエストを処理します。

        受信したリクエストを変換し、外部APIに送信します。

        Args:
            request_data: 受信した決済リクエストデータ

        Returns:
            PaymentResponse: 処理結果
        """
        try:
            logger.info("Processing payment request")

            # 受信データを送信データに変換
            payment_request = self._transform_request(request_data)

            # 送信データの辞書形式への変換
            request_dict = self._payment_request_to_dict(payment_request)

            # 送信データをロギング（機密情報は除く）
            safe_log_data = request_dict.copy()
            if "authenticationPass" in safe_log_data:
                safe_log_data["authenticationPass"] = "****"
            logger.info(f"Transformed request: {safe_log_data}")

            # 外部APIにデータを送信
            response = await self._http_client.post(
                url=settings.PAYMENT_API_URL, data=request_dict
            )

            return PaymentResponse(
                success=True,
                message="Payment request processed successfully",
                data=response,
            )

        except Exception as e:
            logger.exception(f"Error processing payment request: {str(e)}")
            return PaymentResponse(
                success=False, message="Payment processing error", error=str(e)
            )

    def _transform_request(self, request_data: Dict[str, Any]) -> PaymentRequest:
        """
        受信リクエストを送信リクエストに変換します。

        Args:
            request_data: 受信したリクエストデータ

        Returns:
            PaymentRequest: 変換された送信用リクエスト
        """
        # 現在のタイムスタンプをISO 8601形式で生成
        current_timestamp = datetime.now().isoformat(timespec="milliseconds") + "+09:00"

        # リクエストデータから必要な情報を抽出
        # 実際の実装では、受信データの構造に応じて適切にマッピングする必要があります
        amount = str(request_data.get("paymentInfo", {}).get("amount", "0"))
        order_number = request_data.get("paymentInfo", {}).get(
            "orderNumber", "SPNM0000000000000000"
        )
        description = request_data.get("paymentInfo", {}).get("description", "")

        # 決済リクエスト項目の作成
        regi_charge_req_items = [
            RegiChargeRequestItem(
                store_order_number=order_number,
                settlement_amount=amount,
                display_contents1=description[:20],  # 表示内容に制限がある場合を想定
                display_contents2="bbb",
            )
        ]

        # 送信用リクエストの作成
        return PaymentRequest(
            company_code="DCM12345678",
            store_code="TNP00000001",
            authentication_pass="XXXXXXXXXXXXXXXXXXXX",
            transaction_id="transid0000000000001",
            req_timestamp=current_timestamp,
            exec_mode="000",
            billing_token="9000000248250856006510",
            regi_charge_req_list=regi_charge_req_items,
        )

    def _payment_request_to_dict(
        self, payment_request: PaymentRequest
    ) -> Dict[str, Any]:
        """
        PaymentRequestをAPIリクエスト用の辞書に変換します。

        Args:
            payment_request: 送信用リクエスト

        Returns:
            Dict[str, Any]: 変換された辞書
        """
        # RegiChargeRequestItemの変換
        regi_charge_req_list = []
        for item in payment_request.regi_charge_req_list:
            regi_charge_req_list.append(
                {
                    "storeOrderNumber": item.store_order_number,
                    "settlementAmount": item.settlement_amount,
                    "displayContents1": item.display_contents1,
                    "displayContents2": item.display_contents2,
                }
            )

        # PaymentRequestの変換
        return {
            "companyCode": payment_request.company_code,
            "storeCode": payment_request.store_code,
            "authenticationPass": payment_request.authentication_pass,
            "transactionId": payment_request.transaction_id,
            "reqTimestamp": payment_request.req_timestamp,
            "execMode": payment_request.exec_mode,
            "billingToken": payment_request.billing_token,
            "regiChargeReqList": regi_charge_req_list,
        }
