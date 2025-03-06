"""
APIルートモジュール。

FastAPIのルートとハンドラを定義します。
"""

from __future__ import annotations

import logging
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from app.domain.interfaces.payment_service import PaymentServiceInterface
from app.interfaces.schemas.payment import PaymentRequestSchema, PaymentResponseSchema
from app.interfaces.api.dependencies import get_payment_service
from app.core.errors import ValidationException, PaymentApiException

logger = logging.getLogger(__name__)

# 決済関連のAPIルーターを作成
router = APIRouter(tags=["payment"])


@router.post("/receive", response_model=None)
async def receive_payment(
    payment_request: PaymentRequestSchema,
    payment_service: PaymentServiceInterface = Depends(get_payment_service),
):
    """
    決済リクエストを受信するエンドポイント。

    このエンドポイントは以下の処理を行います：
    1. クライアントからの決済リクエストを受信
    2. 決済サービスを使用してリクエストを処理
    3. 外部APIからのレスポンスをそのまま返却

    Args:
        payment_request: クライアントからの決済リクエスト
        payment_service: 依存性注入された決済サービス

    Returns:
        外部APIからのレスポンスをそのまま返します

    Raises:
        ValidationException: 入力データが無効な場合
        PaymentApiException: 外部APIとの通信中にエラーが発生した場合
        HTTPException: その他のエラーが発生した場合
    """
    try:
        # ステップ1: リクエストの受信をログに記録
        logger.info("決済リクエストを受信しました")
        
        # ステップ2: 決済サービスを使用してリクエストを処理
        logger.info("決済サービスにリクエストを転送します")
        result = await payment_service.process_payment(payment_request.data)

        # 処理結果の確認
        if not result.success:
            # 処理に失敗した場合はエラーをログに記録し、例外をスロー
            logger.error(f"決済処理に失敗しました: {result.error}")
            raise PaymentApiException(
                detail=result.error or "決済処理に失敗しました"
            )

        # ステップ3: 外部APIからのレスポンスをそのまま返却
        logger.info("決済処理が成功しました。レスポンスを返却します")
        return result.data

    except ValidationException as e:
        # バリデーションエラーの処理
        logger.error(f"バリデーションエラー: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail
        )

    except PaymentApiException as e:
        # 外部API通信エラーの処理
        logger.error(f"決済API通信エラー: {e.detail}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=e.detail)

    except Exception as e:
        # 予期しないエラーの処理
        logger.exception(f"予期しないエラーが発生しました: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部サーバーエラー: {str(e)}",
        )
