# ナンプレWebアプリ - Vercelデプロイメントガイド

Vercelを使用して`https://your-project.vercel.app/game/`または`https://pokoroblog.com/game/`でナンプレWebアプリを公開する手順です。

## 🚀 Vercelデプロイメントの利点

- **無料プラン**: 十分な機能とトラフィック
- **自動HTTPS**: SSL証明書は自動設定
- **GitHubと連携**: プッシュで自動デプロイ
- **グローバルCDN**: 高速配信
- **カスタムドメイン対応**: pokoroblog.com対応

## 📋 前提条件

- GitHubアカウント
- Vercelアカウント（GitHubでサインアップ可能）
- ドメイン `pokoroblog.com`（カスタムドメイン使用時）

## 🛠 デプロイメント手順

### 1. GitHubリポジトリの作成

```bash
# プロジェクトルートで初期化
cd sudoku_webapp
git init
git add .
git commit -m "Initial commit: Sudoku Web App for Vercel"

# GitHubリポジトリを作成後
git remote add origin https://github.com/your-username/sudoku-webapp.git
git branch -M main
git push -u origin main
```

### 2. Vercelでのプロジェクト作成

1. **Vercel にログイン**: https://vercel.com
2. **New Project** をクリック
3. **GitHub リポジトリを選択**: `sudoku-webapp`
4. **プロジェクト設定**:
   - Framework Preset: `Other`
   - Root Directory: `./` (デフォルト)
   - Build Command: (空のまま)
   - Output Directory: `public` (自動設定)

### 3. 環境変数の設定

Vercelダッシュボードで：

1. **Settings** → **Environment Variables**
2. 以下を追加：
   ```
   Name: SECRET_KEY
   Value: your-super-secure-secret-key-here
   ```

### 4. カスタムドメインの設定（オプション）

1. **Settings** → **Domains**
2. **Add Domain**: `pokoroblog.com`
3. **DNS設定**（ドメインプロバイダーで）:
   ```
   Type: CNAME
   Name: game (または www)
   Value: your-project.vercel.app
   ```

## 📁 ファイル構成

Vercel用に最適化されたファイル構成：

```
sudoku_webapp/
├── api/
│   └── index.py          # Vercel Functions エントリーポイント
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── sudoku.js
├── templates/
│   └── index.html
├── sudoku.py             # ゲームロジック
├── vercel.json           # Vercel設定
├── requirements.txt      # Python依存関係
└── README.md
```

## 🔧 重要な設定ファイル

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/game/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/",
      "dest": "/api/index.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

### requirements.txt
```
flask==3.1.1
```

## 🎯 デプロイ後のアクセスURL

### 自動生成URL
- **メイン**: https://your-project.vercel.app/game/
- **ブランチ**: https://your-project-git-main-username.vercel.app/game/

### カスタムドメイン（設定後）
- **本番**: https://pokoroblog.com/game/

## 🔄 継続的デプロイメント

GitHubにプッシュすると自動的にデプロイされます：

```bash
# 変更をプッシュ
git add .
git commit -m "Update game features"
git push origin main

# Vercelが自動的に検知してデプロイ
```

## 📊 監視・ログ

### Vercelダッシュボード
1. **Functions** → 実行ログの確認
2. **Analytics** → トラフィック解析
3. **Speed Insights** → パフォーマンス監視

### ローカルでのテスト
```bash
# Vercel CLIのインストール
npm i -g vercel

# ローカルでVercel環境をシミュレーション
vercel dev
```

## 🚨 制限事項・注意点

### Vercelの制限
- **Function実行時間**: 10秒（Hobby Plan）
- **メモリ使用量**: 1024MB（Hobby Plan）
- **同時接続数**: 1000（Hobby Plan）
- **ファイルサイズ**: 50MB（デプロイ単位）

### セッション管理
- サーバーレス環境のため、メモリ内セッションは制限的
- 本格運用時はRedisやデータベースの検討を推奨

## 🛠 トラブルシューティング

### よくある問題

1. **Import Error**
   ```
   エラー: ModuleNotFoundError: No module named 'sudoku'
   解決: api/index.py でのパス設定を確認
   ```

2. **テンプレートが見つからない**
   ```
   エラー: TemplateNotFound
   解決: Flask(template_folder=...) の設定を確認
   ```

3. **静的ファイルが読み込まれない**
   ```
   解決: Flask(static_folder=...) の設定を確認
   ```

### デバッグ方法

```bash
# Vercel Function ログの確認
vercel logs https://your-project.vercel.app

# ローカルでのテスト
vercel dev --debug
```

## 📈 パフォーマンス最適化

### 推奨設定

1. **静的ファイルキャッシュ**: 自動適用
2. **Gzip圧縮**: 自動適用  
3. **CDN配信**: グローバル配信

### 監視項目

- **First Contentful Paint (FCP)**
- **Largest Contentful Paint (LCP)**
- **Cumulative Layout Shift (CLS)**

## 🔒 セキュリティ

Vercel自動適用：
- **HTTPS強制**
- **セキュリティヘッダー**
- **DDoS保護**

## 💰 コスト

- **Hobby Plan**: 無料
  - 100GB帯域幅/月
  - 100 Function実行/日
  - カスタムドメイン対応

- **Pro Plan**: $20/月
  - 1TB帯域幅/月
  - 無制限Function実行
  - 高度なアナリティクス

## 🎉 デプロイ完了

設定完了後、以下のURLでアクセス可能：

- **Vercel URL**: https://your-project.vercel.app/game/
- **カスタムドメイン**: https://pokoroblog.com/game/

おめでとうございます！ナンプレWebアプリがVercelで稼働中です！🎮