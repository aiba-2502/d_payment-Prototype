"""
HTTPクライアントモジュール。

外部APIとの通信を担当します。
"""

from __future__ import annotations

import httpx
import logging
from typing import Dict, Any

from app.domain.interfaces.payment_service import HttpClientInterface

logger = logging.getLogger(__name__)


class HttpClient(HttpClientInterface):
    """
    HTTPクライアントの実装。

    外部APIとの通信を担当します。
    """

    async def post(
        self, url: str, data: Dict[str, Any], timeout: int = 30
    ) -> Dict[str, Any]:
        """
        POSTリクエストを送信します。

        Args:
            url: 送信先URL
            data: 送信データ
            timeout: タイムアウト秒数

        Returns:
            Dict[str, Any]: レスポンスデータ

        Raises:
            Exception: リクエスト送信中にエラーが発生した場合
        """
        try:
            logger.info(f"Sending POST request to {url}")
            logger.debug(f"Request data: {data}")

            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    url,
                    json=data,
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                )

                # レスポンスのステータスコードをチェック
                response.raise_for_status()

                # JSONレスポンスを解析
                response_data = response.json()
                logger.debug(f"Response data: {response_data}")

                return response_data

        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
            )
            # エラーレスポンスがJSONの場合は解析を試みる
            try:
                error_data = e.response.json()
                logger.error(f"Error details: {error_data}")
                return {
                    "success": False,
                    "status_code": e.response.status_code,
                    "error": error_data,
                }
            except Exception:
                return {
                    "success": False,
                    "status_code": e.response.status_code,
                    "error": e.response.text,
                }

        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {str(e)}")
            return {"success": False, "error": f"Request error: {str(e)}"}

        except Exception as e:
            logger.exception(f"Unexpected error during API request: {str(e)}")
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
