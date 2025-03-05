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

router = APIRouter(tags=["payment"])


@router.post("/receive", response_model=PaymentResponseSchema)
async def receive_payment(
    payment_request: PaymentRequestSchema,
    payment_service: PaymentServiceInterface = Depends(get_payment_service),
):
    """
    決済リクエストを受信します。

    受信したリクエストを処理し、外部APIに転送します。

    Args:
        payment_request: 決済リクエスト
        payment_service: 決済サービス

    Returns:
        JSONResponse: 処理結果

    Raises:
        ValidationException: 入力データが無効な場合
        PaymentApiException: 外部APIとの通信中にエラーが発生した場合
    """
    try:
        logger.info("Received payment request")

        # 決済リクエストの処理
        result = await payment_service.process_payment(payment_request.data)

        if not result.success:
            # 処理に失敗した場合
            logger.error(f"Payment processing failed: {result.error}")
            raise PaymentApiException(
                detail=result.error or "Payment processing failed"
            )

        # 処理成功
        return PaymentResponseSchema(
            success=True, message=result.message, data=result.data
        )

    except ValidationException as e:
        logger.error(f"Validation error: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail
        )

    except PaymentApiException as e:
        logger.error(f"Payment API error: {e.detail}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=e.detail)

    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.get("/health")
async def health_check():
    """
    ヘルスチェックエンドポイント。

    ロードバランサーのヘルスチェックに使用します。

    Returns:
        dict: ヘルスチェック結果
    """
    return {"status": "ok"}
