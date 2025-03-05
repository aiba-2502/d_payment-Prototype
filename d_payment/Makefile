.PHONY: up down build logs test lint format shell help

# デフォルトのターゲット
.DEFAULT_GOAL := help

# コンテナ名
APP_CONTAINER = app
NGINX_CONTAINER = nginx

# ヘルプコマンド
help: ## このヘルプを表示
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Docker関連コマンド
up: ## アプリケーションを起動
	docker-compose up -d

down: ## アプリケーションを停止
	docker-compose down

build: ## Dockerイメージをビルド
	docker-compose build

logs: ## アプリケーションのログを表示
	docker-compose logs -f

# 開発関連コマンド
test: ## テストを実行
	docker-compose exec $(APP_CONTAINER) pytest

lint: ## コードの静的解析を実行
	docker-compose exec $(APP_CONTAINER) flake8 app tests
	docker-compose exec $(APP_CONTAINER) mypy app tests

format: ## コードのフォーマットを実行
	docker-compose exec $(APP_CONTAINER) black app tests
	docker-compose exec $(APP_CONTAINER) isort app tests

shell: ## アプリケーションコンテナでシェルを起動
	docker-compose exec $(APP_CONTAINER) /bin/bash

# クリーンアップコマンド
clean: ## 一時ファイルやキャッシュを削除
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +