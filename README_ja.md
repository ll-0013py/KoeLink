# KoeLink

<div align="center">

🌏 **Language / 言語選択** 🌏

[English](README.md) | [日本語](README_ja.md)

</div>

日本語音声・動画を英語音声に翻訳し、対応するスクリプトを生成する包括的なツールです。

*KoeLink*（声Link）は言語の壁を越えて、言語の得意不得意を問わず誰でもコミュニケーションが取れることを目指しています。

## 概要

KoeLinkは、日本語のプレゼンテーション動画や音声を英語音声に翻訳し、対応するスクリプトも出力するモジュール化されたPythonアプリケーションです。進捗状況の追跡機能を備えたユーザーフレンドリーなコマンドラインインターフェースを提供し、ローカル環境とGoogle Colaboratoryの両方で実行可能です。

## 機能

- **日本語音声認識**: SpeechFlow APIを使用した自動文字起こし
- **テキスト修正**: OpenAIのChatGPTによる日本語テキストの改善
- **翻訳**: DeepLによる高品質な日本語から英語への翻訳
- **音声合成**: Genny（Lovo AI）による自然な英語音声生成
- **音声分割**: 長時間音声の自動分割（約20分単位）
- **進捗追跡**: ステップごとのフィードバックとリアルタイム進捗表示
- **エラーハンドリング**: 包括的なエラー処理と検証機能

## 使用方法

### 🏠 ローカル環境での実行（推奨）

1. **環境準備**
   ```bash
   # 必要なライブラリのインストール
   pip install -r requirements.txt
   ```

2. **API設定**
   プロジェクトのルートディレクトリに`.env`ファイルを作成し、以下の情報を入力：
   ```
   SPEECHFLOW_API_KEY_ID="your_api_key_id"
   SPEECHFLOW_API_KEY_SECRET="your_api_key_secret"
   OPENAI_API_KEY="your_openai_api_key"
   GENNY_API_URL="your_genny_api_url"
   GENNY_API_KEY="your_genny_api_key"
   GENNY_SPEAKER="your_speaker_name"
   GENNY_SPEAKER_STYLE="your_speaker_style"
   DEEPL_AUTH_KEY="your_deepl_auth_key"
   ```

3. **実行**
   ```bash
   # ターミナル/コマンドプロンプトで実行
   python main.py
   ```

4. **ファイル指定**
   実行すると、翻訳したい日本語動画/音声ファイルのパスを求められます。
   - ローカルファイルパス：`C:\Users\username\video.mp4`
   - URL：`https://example.com/video.mp4`

5. **出力確認**
   処理完了後、`output`フォルダに以下のファイルが生成されます：
   - 日本語テキスト（完全版）
   - 英語テキスト（分割版）
   - 英語音声ファイル（分割版）

### ☁️ Google Colaboratoryでの実行

1. **ファイルアップロード**
   プロジェクトファイル一式をGoogle Driveにアップロードします。

2. **Colabで実行**
   ```python
   # main.ipynbのすべてのセルを順番に実行
   ```

3. **ファイル指定**
   Google Driveにアップロードしたファイルのパスを入力します。

4. **出力確認**
   処理完了後、`output`フォルダに結果が出力されます。

## 対応ファイル形式

- **音声ファイル**: MP3, WAV, M4A など
- **動画ファイル**: MP4, AVI, MOV など

## 注意事項

### 📁 ファイルの取り扱い
- **ローカル環境**: ローカルファイルパスを直接指定可能
- **Google Colab**: Google Driveにアップロードしたファイルのパスを使用
- **リモートファイル**: 直接アクセス可能なURLも使用可能（GitHubのRAWファイルなど）

### 🎵 音声の分割について
- 英語音声は約20分単位で自動分割されます（聞き手の集中力を考慮）
- 英語テキストと音声ファイルの通し番号は一致しています

### 🔧 技術的な注意点
- OpenAI APIなどの外部APIを使用しているため、仕様変更によりアップデートが必要な場合があります
- 機密情報は`.env`ファイルに保存し、Gitにコミットしないよう注意してください

### 💡 トラブルシューティング
- バグが発生した場合は、issueをお知らせください
- 長時間の処理が必要な場合があります（音声の長さによる）
- YouTube動画のURLは直接対応していません

## プロジェクト構成

```
KoeLink/
├── main.py                 # メインアプリケーションエントリーポイント
├── main.ipynb             # Google Colab用Jupyterノートブック
├── requirements.txt       # Python依存関係
├── .env                   # API認証情報（このファイルを作成）
├── config/
│   ├── __init__.py
│   └── settings.py        # 設定管理
├── modules/
│   ├── __init__.py
│   ├── speechflow_transcription.py  # SpeechFlow統合
│   ├── chatgpt_text_correction.py   # ChatGPTテキスト修正
│   ├── deepl_translation.py         # DeepL翻訳
│   └── genny_synthesis.py           # Genny音声合成
├── utils/
│   ├── __init__.py
│   └── file_utils.py      # ファイル処理ユーティリティ
├── data/
│   ├── context.txt        # ChatGPTコンテキスト情報
│   └── prompt_fix_jp.txt  # 日本語テキスト修正プロンプト
└── output/                # 生成された出力ファイル
```

## 処理フロー

```
日本語音声/動画 → 音声認識 → テキスト修正 → 英語翻訳 → 英語音声生成 → 出力
      ↓              ↓           ↓          ↓           ↓
   入力ファイル    SpeechFlow   ChatGPT    DeepL      Genny
```

## 使用API

- [SpeechFlow](https://docs.speechflow.io/): 高精度な文字起こしのためのプロフェッショナル音声認識APIサービス
- [OpenAI](https://platform.openai.com/docs/api-reference): テキスト生成と改善のためのGPT-4を含むAIモデル
- [DeepL](https://www.deepl.com/docs-api): 高精度な業界最先端の翻訳API
- [Genny (Lovo AI)](https://docs.genny.lovo.ai/): 自然な音声を持つ高度なテキスト読み上げ合成

各サービスは特定の機能を提供します：
- **SpeechFlow**: 日本語音声を高精度でテキストに変換
- **OpenAI ChatGPT**: 文字起こしされた日本語テキストを修正・改善
- **DeepL**: プロフェッショナルレベルの日本語から英語への翻訳を提供
- **Genny**: テキストから自然な英語音声を生成

## 必要な環境

### システム要件
- Python 3.8以上（3.13対応）
- 音声処理用: ffmpeg（pydubが自動的に処理）

### Python依存関係
必要なパッケージをすべてインストール：
```bash
pip install -r requirements.txt
```

必要なパッケージ：
- `python-dotenv`: 環境変数管理
- `requests`: API通信用HTTPリクエスト
- `pydub`: 音声ファイル操作
- `openai`: OpenAI APIクライアント
- `deepl`: DeepL翻訳APIクライアント
- `pytz`: タイムゾーン処理
- `audioop-lts`: 音声操作（Python 3.13以降用）

### APIキー
以下のサービスからAPIキーを取得する必要があります：
1. **SpeechFlow**: [サインアップ](https://speechflow.io/)
2. **OpenAI**: [APIキー取得](https://platform.openai.com/api-keys)
3. **DeepL**: [アカウント作成](https://www.deepl.com/pro-api)
4. **Genny (Lovo AI)**: [開始する](https://genny.lovo.ai/)

### 設定ファイル
1. ChatGPTコンテキスト指示を含む`data/context.txt`を作成
2. 日本語修正プロンプトテンプレートを含む`data/prompt_fix_jp.txt`を作成
3. `output/`ディレクトリが存在することを確認（自動作成される）

## ライセンス

使用前に各APIサービスの利用規約をご確認ください。

---

<div align="center">

🌏 **Language / 言語選択** 🌏

[English](README.md) | [日本語](README_ja.md)

</div>