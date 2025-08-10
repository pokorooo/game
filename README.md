# ナンプレ（数独）完全版アプリ

美しいWebUIとCLIの両方を提供するナンプレ（数独）アプリケーションです。

## 機能

- **3つの難易度**: 簡単（30空欄）、普通（45空欄）、難しい（55空欄）
- **2つのインターフェース**: Webアプリ & CLIアプリ
- **インタラクティブUI**: セルクリック + 数字入力（Web）
- **リアルタイムバリデーション**: 無効な手の検出
- **解答チェック**: 完成時の正解判定
- **ヒント機能**: 困った時のヒント表示
- **勝利アニメーション**: 正解時のセレブレーション効果（Web）
- **レスポンシブデザイン**: PC・タブレット・スマホ対応（Web）

## 技術構成

- **バックエンド**: Flask (Python) - Webアプリ用
- **フロントエンド**: HTML + CSS + JavaScript - Webアプリ用
- **コア**: Python標準ライブラリ - CLI・ロジック
- **スタイル**: モダンなグラデーションデザイン
- **API**: RESTful JSON API

## ファイル構成

```
sudoku_webapp/
├── app.py                 # Flaskアプリケーション（Webアプリ）
├── main.py               # CLIアプリケーション
├── sudoku.py             # ナンプレ生成・解答チェックロジック
├── test_sudoku.py        # 機能テストファイル
├── requirements.txt      # 依存関係
├── templates/
│   └── index.html        # メインHTMLテンプレート
├── static/
│   ├── css/
│   │   └── style.css     # スタイルシート
│   └── js/
│       └── sudoku.js     # フロントエンドJavaScript
└── README.md             # このファイル
```

## 使用方法

### Webアプリ版

#### 1. 必要なライブラリのインストール

```bash
pip3 install -r requirements.txt
```

#### 2. Webアプリの起動

```bash
cd sudoku_webapp
python3 app.py
```

#### 3. Webブラウザでアクセス

- ローカル: http://127.0.0.1:8080/game/
- ローカルネットワーク: http://[your-ip]:8080/game/

### Vercelデプロイ版（推奨）

詳細は `VERCEL_DEPLOYMENT.md` を参照

- 本番環境: https://your-project.vercel.app/game/
- カスタムドメイン: https://pokoroblog.com/game/

### CLIアプリ版

```bash
cd sudoku_webapp
python3 main.py
```

### 機能テスト

```bash
cd sudoku_webapp
python3 test_sudoku.py
```

## 操作方法

1. **新しいゲーム開始**: 難易度を選択して「新しいゲーム」ボタンをクリック
2. **数字入力**: セルをクリックして選択後、数字ボタンまたはキーボードで入力
3. **セルクリア**: セルを選択して「クリア」ボタンまたはDeleteキー
4. **解答チェック**: 完成したら「解答チェック」ボタン
5. **ヒント**: 困った時は「ヒント」ボタン

## 開発者向け

### API エンドポイント

- `POST /new_game` - 新しいゲームを作成
- `POST /make_move` - 数字を入力
- `POST /clear_cell` - セルをクリア
- `POST /check_solution` - 解答をチェック
- `POST /get_hint` - ヒントを取得
- `GET /get_board` - 現在の盤面を取得

### カスタマイズ

- **難易度調整**: `sudoku.py`の`get_cells_to_remove()`メソッド
- **スタイル変更**: `static/css/style.css`
- **UI改良**: `templates/index.html`と`static/js/sudoku.js`

## ライセンス

このプロジェクトはオープンソースです。自由にご利用ください。