"""
エラー処理モジュール。

アプリケーション全体で使用するカスタムエラークラスと例外ハンドラを提供します。
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class BaseAppException(Exception):
    """
    アプリケーションの基本例外クラス。

    すべてのカスタム例外の基底クラスとして使用します。
    """

    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "内部サーバーエラーが発生しました",
        headers: Optional[Dict[str, Any]] = None,
    ):
        """
        初期化メソッド。

        Args:
            status_code: HTTPステータスコード
            detail: エラーの詳細メッセージ
            headers: レスポンスに含めるヘッダー
        """
        self.status_code = status_code
        self.detail = detail
        self.headers = headers


class ValidationException(BaseAppException):
    """
    バリデーションエラーの例外クラス。
    """

    def __init__(
        self,
        detail: str = "入力データが無効です",
        headers: Optional[Dict[str, Any]] = None,
    ):
        """
        初期化メソッド。

        Args:
            detail: エラーの詳細メッセージ
            headers: レスポンスに含めるヘッダー
        """
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            headers=headers,
        )


class PaymentApiException(BaseAppException):
    """
    決済API通信エラーの例外クラス。
    """

    def __init__(
        self,
        detail: str = "決済APIとの通信中にエラーが発生しました",
        headers: Optional[Dict[str, Any]] = None,
    ):
        """
        初期化メソッド。

        Args:
            detail: エラーの詳細メッセージ
            headers: レスポンスに含めるヘッダー
        """
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail,
            headers=headers,
        )


async def base_exception_handler(
    request: Request,
    exc: BaseAppException,
) -> JSONResponse:
    """
    BaseAppExceptionのハンドラ。

    Args:
        request: リクエストオブジェクト
        exc: 発生した例外

    Returns:
        JSONResponse: エラーレスポンス
    """
    logger.error(
        f"BaseAppException: {exc.detail}",
        extra={"path": request.url.path, "status_code": exc.status_code},
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """
    RequestValidationErrorのハンドラ。

    Args:
        request: リクエストオブジェクト
        exc: 発生した例外

    Returns:
        JSONResponse: エラーレスポンス
    """
    logger.error(
        f"ValidationError: {exc.errors()}",
        extra={"path": request.url.path},
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


async def general_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    一般的な例外のハンドラ。

    Args:
        request: リクエストオブジェクト
        exc: 発生した例外

    Returns:
        JSONResponse: エラーレスポンス
    """
    logger.error(
        f"UnhandledException: {str(exc)}",
        extra={"path": request.url.path},
        exc_info=True,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "内部サーバーエラーが発生しました"},
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """
    FastAPIアプリケーションに例外ハンドラを設定します。

    Args:
        app: FastAPIアプリケーションインスタンス
    """
    app.add_exception_handler(BaseAppException, base_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
