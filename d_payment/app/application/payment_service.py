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

        このメソッドは以下の手順で処理を行います：
        1. 受信したリクエストデータを外部API用の形式に変換
        2. 外部APIにデータを送信
        3. 外部APIからのレスポンスをそのまま返す

        Args:
            request_data: 受信した決済リクエストデータ

        Returns:
            PaymentResponse: 処理結果
        """
        try:
            logger.info("決済リクエストの処理を開始します")

            # ステップ1: 受信データを外部API用の形式に変換
            payment_request = self._transform_request(request_data)
            request_dict = self._payment_request_to_dict(payment_request)

            # 送信データをロギング（機密情報は除く）
            safe_log_data = request_dict.copy()
            if "authenticationPass" in safe_log_data:
                safe_log_data["authenticationPass"] = "****"
            logger.info(f"変換されたリクエスト: {safe_log_data}")

            # ステップ2: 外部APIにデータを送信
            logger.info(f"外部API {settings.PAYMENT_API_URL} にリクエストを送信します")
            response = await self._http_client.post(
                url=settings.PAYMENT_API_URL, data=request_dict
            )
            logger.info("外部APIからレスポンスを受信しました")

            # ステップ3: 外部APIからのレスポンスをそのまま返す
            return PaymentResponse(
                success=True,
                message="決済リクエストが正常に処理されました",
                data=response,
            )

        except Exception as e:
            logger.exception(f"決済リクエスト処理中にエラーが発生しました: {str(e)}")
            return PaymentResponse(
                success=False, message="決済処理エラー", error=str(e)
            )

    def _transform_request(self, request_data: Dict[str, Any]) -> PaymentRequest:
        """
        受信リクエストを外部API用のリクエストに変換します。

        Args:
            request_data: 受信したリクエストデータ

        Returns:
            PaymentRequest: 変換された外部API用リクエスト
        """
        # 現在のタイムスタンプをISO 8601形式で生成（日本時間）
        current_timestamp = datetime.now().isoformat(timespec="milliseconds") + "+09:00"

        # リクエストデータから必要な情報を抽出
        payment_info = request_data.get("paymentInfo", {})
        
        # 基本情報の取得（デフォルト値付き）
        amount = str(payment_info.get("amount", "0"))
        order_number = payment_info.get("orderNumber", "SPNM0000000000000000")
        description = payment_info.get("description", "")
        
        # 表示内容の取得（デフォルト値付き）
        # displayContents1が指定されていない場合は、descriptionを使用
        display_contents1 = payment_info.get("displayContents1", description[:20])
        display_contents2 = payment_info.get("displayContents2", "")
        
        # 請求トークンの取得（デフォルト値付き）
        billing_token = request_data.get("billingToken", "9000000248250856006510")

        # 決済リクエスト項目の作成
        regi_charge_req_items = [
            RegiChargeRequestItem(
                store_order_number=order_number,
                settlement_amount=amount,
                display_contents1=display_contents1,
                display_contents2=display_contents2,
            )
        ]

        # 外部API用リクエストの作成
        return PaymentRequest(
            company_code=settings.PAYMENT_COMPANY_CODE,
            store_code=settings.PAYMENT_STORE_CODE,
            authentication_pass=settings.PAYMENT_AUTHENTICATION_PASS,
            transaction_id="transid0000000000001",
            req_timestamp=current_timestamp,  # 現在時刻を自動設定
            exec_mode="000",
            billing_token=billing_token,
            regi_charge_req_list=regi_charge_req_items,
        )

    def _payment_request_to_dict(
        self, payment_request: PaymentRequest
    ) -> Dict[str, Any]:
        """
        PaymentRequestオブジェクトを外部API用の辞書形式に変換します。

        Args:
            payment_request: 送信用リクエストオブジェクト

        Returns:
            Dict[str, Any]: 外部API用の辞書形式データ
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
