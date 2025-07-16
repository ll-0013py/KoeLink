# KoeLink

<div align="center">

🌏 **Language / 言語選択** 🌏

[English](README.md) | [日本語](README_ja.md)

</div>

日本語音声・動画を英語音声に翻訳し、対応するスクリプトを生成するツールです。

*KoeLink*（声Link）は言語の壁を越えて、言語の得意不得意を問わず誰でもコミュニケーションが取れることを目指しています。

## 概要

このシステムは、日本語のプレゼンテーション動画や音声を英語音声に翻訳し、対応するスクリプトも出力します。Google Colaboratoryでも実行可能です。

## 機能

- 日本語音声の自動文字起こし（SpeechFlow）
- 日本語テキストの自動修正（ChatGPT）
- 日本語から英語への翻訳（DeepL）
- 英語音声の自動生成（Genny）
- 長時間音声の自動分割（約20分単位）

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

## 処理フロー

```
日本語音声/動画 → 音声認識 → テキスト修正 → 英語翻訳 → 英語音声生成 → 出力
      ↓              ↓           ↓          ↓           ↓
   入力ファイル    SpeechFlow   ChatGPT    DeepL      Genny
```

## 使用API

- [SpeechFlow](https://docs.speechmatics.com/flow/flow-api-ref): リアルタイム音声認識
- [OpenAI](https://platform.openai.com/docs/api-reference): テキスト修正・生成
- [DeepL](https://github.com/DeepLcom/deepl-python): 高品質翻訳
- [Genny](https://github.com/cheekybits/genny): 音声合成

## ライセンス

使用前に各APIサービスの利用規約をご確認ください。

---

<div align="center">

🌏 **Language / 言語選択** 🌏

[English](README.md) | [日本語](README_ja.md)

</div>