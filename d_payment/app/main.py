"""
メインアプリケーションモジュール。

FastAPIアプリケーションのエントリーポイントとなるモジュールです。
ルーティング、ミドルウェア、イベントハンドラなどの設定を行います。
"""

from __future__ import annotations

import logging
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.errors import setup_exception_handlers
from app.interfaces.api.routes import router as api_router

# ロギングの設定
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# FastAPIアプリケーションの作成
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORSの設定
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# リクエスト処理時間を計測するミドルウェア
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# ルーターの設定
app.include_router(api_router, prefix=settings.API_PREFIX)

# 例外ハンドラの設定
setup_exception_handlers(app)


@app.get("/")
async def root():
    """
    ルートエンドポイント。

    Returns:
        dict: 基本的な情報を含む辞書
    """
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
    }


@app.on_event("startup")
async def startup_event():
    """
    アプリケーション起動時のイベントハンドラ。

    リソースの初期化などを行います。
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    アプリケーション終了時のイベントハンドラ。

    リソースのクリーンアップなどを行います。
    """
    logger.info(f"Shutting down {settings.APP_NAME}")
