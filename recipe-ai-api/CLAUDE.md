# recipe-ai-api

## プロジェクト概要

ルールベースのレシピ自動生成 REST API（v3）。
AI APIを使わず、Claudeの料理知識とWeb上の人気レシピ分析で構築した大規模データベースにより、食材・調味料・調理テンプレートの組み合わせから実用的なレシピを自動生成する。

## ディレクトリ構成

```
recipe-ai-api/
├── recipe_api_app.py          # アプリケーション本体（単一ファイル構成）
├── deploy-files.txt           # デプロイ対象ファイル一覧
├── .claude/CLAUDE.local.md    # サーバー情報（Git管理外）
└── CLAUDE.md                  # 本ファイル
```

### recipe_api_app.py の構造

| セクション | 行範囲 | 役割 |
|---|---|---|
| 食材データベース | `PROTEINS`, `VEGETABLES` | タンパク質(30種+)・野菜(40種+)の栄養・下処理・調理法データ |
| 味付けセット | `SEASONINGS` | 和食・中華・洋食・エスニック等 20種の味付けパターン |
| 調理テンプレート | `TEMPLATES` | 炒める・煮る等の調理法別レシピテンプレート |
| 相性ルール | `GOOD_PAIRINGS` | 食材×調味料の相性パターン |
| 定番料理 | `NAMED_RECIPES` | 肉じゃが・唐揚げ等の定番料理テンプレート |
| `FuzzyMatcher` | あいまい検索 | 食材名のエイリアス・あいまいマッチング |
| `RecipeEngine` | レシピ生成エンジン | 食材選択・味付け決定・テンプレート適用のコアロジック |
| `AppAdapter` | アプリ連携アダプタ | モバイルアプリのリクエスト/レスポンス形式変換 |
| `RecipeAPIHandler` | HTTPハンドラ | GET/POST エンドポイントの処理 |

## 使用技術・ライブラリ

- **Python 3** （標準ライブラリのみ、外部依存なし）
  - `http.server` — HTTPServer, BaseHTTPRequestHandler
  - `json`, `random`, `re`, `urllib.parse`

## サーバー構成

### ローカル開発

- ポート: **8001**
- バインド: `0.0.0.0`

### VPS（本番）

> サーバーのIPアドレス・ユーザー名・デプロイ先パス等の詳細は `.claude/CLAUDE.local.md` を参照（Git管理外）

## APIエンドポイント

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/` | API情報・統計 |
| GET | `/generate` | レシピ生成（`?protein=&vegetable=&style=&method=&recipe=&count=N`） |
| GET | `/named` | 定番料理一覧 |
| GET | `/ingredients` | 食材一覧 |
| GET | `/search?q=` | 食材あいまい検索 |
| POST | `/generate` | JSONボディで条件指定して生成 |
| POST | `/api/recipes/generate` | モバイルアプリ連携用（3件生成） |

## ビルド・デプロイ手順

外部依存がないため、ビルド不要。具体的なデプロイコマンドは `.claude/CLAUDE.local.md` を参照。

## 開発時の注意事項

- **単一ファイル構成**: 全ロジックが `recipe_api_app.py` に含まれる（約1750行）
- **外部依存なし**: pip install 不要。Python標準ライブラリのみ使用
- **CORS**: `Access-Control-Allow-Origin: *` で全オリジン許可済み
- **ログ出力**: `log_message` をオーバーライドして標準ログを無効化している
- **.envファイル**: 使用していない（設定値はソース内にハードコード）

## コミットルール

- コミットは「コミットして」と指示があった時のみ行う
- コミットの前に必ず変更内容に以下の機密情報が含まれていないか確認する
  - APIキー・トークン
  - パスワード
  - 個人情報（メールアドレス・電話番号等）
  - サーバーのIPアドレス・接続情報
  - .envファイルの内容
- 機密情報が含まれる場合は作業を中断してその旨を報告する
- 機密情報が含まれない場合のみコミットを実行する
- コミットメッセージは以下の形式で日本語で書く
  - バグ修正：`fix: 内容`
  - 新機能：`feat: 内容`
  - リファクタリング：`refactor: 内容`
  - その他：`chore: 内容`
- コミット後は自動でpushまで行う

## よく使うコマンド

```bash
# ローカル起動
python recipe_api_app.py

# 動作確認
curl http://localhost:8001/
curl http://localhost:8001/generate?protein=鶏むね肉&vegetable=キャベツ
curl http://localhost:8001/generate?recipe=肉じゃが
curl http://localhost:8001/named
curl http://localhost:8001/search?q=ぶたにく

# アプリ連携エンドポイントのテスト
curl -X POST http://localhost:8001/api/recipes/generate \
  -H "Content-Type: application/json" \
  -d '{"season":"春","category":"和食","freeText":"鶏肉でさっぱり"}'
```
