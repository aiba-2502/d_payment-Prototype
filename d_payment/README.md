# D Payment Gateway

## プロジェクト概要

D Payment Gatewayは、クライアントからの決済リクエストを受信し、適切な形式に変換して外部決済APIに転送するサービスです。クリーンアーキテクチャに基づいて設計されており、各レイヤーが明確に分離されています。

## 主な機能

1. クライアントからのデータ受信
2. 受信データの変換処理
3. 外部決済APIへのデータ送信
4. 外部APIからのレスポンスをそのまま返却
5. エラーハンドリングとロギング

## 技術スタック

- Python 3.13+
- FastAPI
- Pydantic
- httpx
- Docker & Docker Compose
- Nginx (ロードバランサー)

## アーキテクチャ

このプロジェクトはクリーンアーキテクチャに基づいて設計されており、以下のレイヤーで構成されています：

1. **ドメイン層** - ビジネスルールとエンティティ
   - `app/domain/` - エンティティとインターフェースの定義

2. **アプリケーション層** - ユースケース
   - `app/application/` - ビジネスロジックの実装

3. **インフラ層** - 外部サービスとの連携
   - `app/infrastructure/` - 外部APIとの通信実装

4. **インターフェース層** - API定義
   - `app/interfaces/` - APIエンドポイントとスキーマ定義

5. **コア** - 設定、例外処理など
   - `app/core/` - 共通設定と例外処理

## 開発環境のセットアップ

### 前提条件

- Docker
- Docker Compose
- Make (オプション)

### セットアップ手順

1. リポジトリをクローン
```bash
git clone <repository-url>
cd d_payment
```

2. 環境変数の設定
`.env.example`ファイルを`.env`にコピーし、必要な環境変数を設定してください。

```bash
cp .env.example .env
# .envファイルを編集して必要な設定を行う
```

3. アプリケーションの実行

#### Docker Composeを使用する場合
```bash
# アプリケーションのビルドと起動
docker-compose up --build

# または、バックグラウンドで実行
docker-compose up -d --build
```

#### Makeコマンドを使用する場合
```bash
# アプリケーションのビルド
make build

# アプリケーションの起動
make up

# ログの確認
make logs
```

## テスト実行

### ローカル環境でのテスト実行
```bash
# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Linuxの場合
.\venv\Scripts\activate   # Windowsの場合

# 依存関係のインストール
pip install -r requirements.txt

# テスト実行
make test
```

### Docker環境でのテスト実行
```bash
# Docker環境でテストを実行
make docker-test
```

## API使用方法

### 決済リクエストの送信

#### エンドポイント
```
POST /api/payment/receive
```

#### リクエスト例
```json
{
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
```

#### 最小限のリクエスト例
```json
{
  "data": {
    "paymentInfo": {
      "amount": 3980,
      "orderNumber": "ORDER12345",
      "description": "商品購入"
    }
  }
}
```

#### リクエストパラメータの説明

| パラメータ | 必須 | 説明 |
|------------|------|------|
| billingToken | いいえ | 決済に使用するトークン。指定しない場合はデフォルト値が使用されます。 |
| paymentInfo.amount | はい | 決済金額 |
| paymentInfo.orderNumber | はい | 注文番号 |
| paymentInfo.description | はい | 決済の説明 |
| paymentInfo.displayContents1 | いいえ | 決済画面に表示する内容。指定しない場合はdescriptionが使用されます。 |
| paymentInfo.displayContents2 | いいえ | 決済画面に表示する追加情報 |

#### レスポンス
外部APIからのレスポンスがそのまま返されます。

## APIドキュメント
アプリケーション起動後、以下のURLでSwagger UIとReDocにアクセスできます：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## プロジェクト構造

```
d_payment/
├── app/                    # アプリケーションコード
│   ├── application/        # アプリケーション層（ユースケース）
│   ├── core/               # コア機能（設定、例外処理）
│   ├── domain/             # ドメイン層（エンティティ、インターフェース）
│   ├── infrastructure/     # インフラ層（外部サービス連携）
│   ├── interfaces/         # インターフェース層（API定義）
│   └── main.py             # アプリケーションのエントリーポイント
├── tests/                  # テストコード
│   ├── integration/        # 統合テスト
│   ├── unit/               # 単体テスト
│   └── conftest.py         # テスト設定
├── docker-compose.yml      # Docker Compose設定
├── Dockerfile              # Dockerイメージ定義
├── Makefile                # Makeコマンド定義
├── requirements.txt        # Pythonパッケージ依存関係
└── README.md               # プロジェクト説明
```