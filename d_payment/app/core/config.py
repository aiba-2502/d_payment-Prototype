"""
アプリケーション設定モジュール。

環境変数から設定を読み込み、アプリケーション全体で使用する設定を提供します。
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    アプリケーション設定クラス。

    環境変数から設定を読み込み、アプリケーション全体で使用する設定を提供します。
    """

    # アプリケーション情報
    APP_NAME: str = "SpModePaymentGateway"
    APP_DESCRIPTION: str = "spmode決済リクエスト変換・転送サービス"
    APP_VERSION: str = "0.1.0"

    # API設定
    API_PREFIX: str = "/api"

    # 環境設定
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # 外部APIの設定
    PAYMENT_API_URL: str = "https://payment1.spmode.ne.jp/api/fes/rksrv/testsrvresource"
    PAYMENT_API_TIMEOUT: int = 30

    # CORSの設定
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 設定ファイルの読み込み
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# 設定インスタンスの作成
settings = Settings()
