"""
決済エンティティモジュール。

決済リクエスト・レスポンスの基本構造を定義します。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional


@dataclass
class RegiChargeRequestItem:
    """
    決済リクエスト項目のエンティティ。
    """

    store_order_number: str
    settlement_amount: str
    display_contents1: str
    display_contents2: str


@dataclass
class PaymentRequest:
    """
    決済リクエストのエンティティ。

    外部APIに送信するリクエストデータを表現します。
    """

    company_code: str
    store_code: str
    authentication_pass: str
    transaction_id: str
    req_timestamp: str
    exec_mode: str
    billing_token: str
    regi_charge_req_list: List[RegiChargeRequestItem]


@dataclass
class PaymentResponse:
    """
    決済レスポンスのエンティティ。

    外部APIからのレスポンスデータを表現します。
    """

    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
