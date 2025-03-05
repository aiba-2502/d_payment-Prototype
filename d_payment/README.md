# SpMode Payment Gateway

## プロジェクト概要

SpMode Payment Gatewayは、クライアントからの決済リクエストを受信し、適切な形式に変換して外部決済APIに転送するサービスです。クリーンアーキテクチャに基づいて設計されており、各レイヤーが明確に分離されています。

## 主な機能

1. クライアントからのデータ受信
2. 受信データの変換処理
3. 外部決済APIへのデータ送信
4. エラーハンドリングとロギング

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
2. **アプリケーション層** - ユースケース
3. **インフラ層** - 外部サービスとの連携
4. **インターフェース層** - API定義
5. **コア** - 設定、例外処理など

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

2. 仮想環境の作成と有効化
```bash
python -m venv venv
source venv/bin/activate  # Linuxの場合
.\venv\Scripts\activate   # Windowsの場合
```

3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

4. 環境変数の設定
`.env.example`ファイルを`.env`にコピーし、必要な環境変数を設定してください。

5. アプリケーションの実行

#### 直接実行（開発モード）
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Docker Composeを使用する場合
```bash
docker-compose up --build
```

## APIドキュメント
アプリケーション起動後、以下のURLでSwagger UIとReDocにアクセスできます：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## ヘルスチェック
アプリケーションの状態を確認するには：
```bash
curl http://localhost:8000/api/health
```