# KoeLink

<div align="center">

🌏 **Language / 言語選択** 🌏

[English](README.md) | [日本語](README_ja.md)

</div>

A comprehensive tool that translates Japanese audio/video to English audio and generates corresponding scripts.

*KoeLink* (声Link) bridges language barriers, enabling seamless communication regardless of linguistic proficiency.

## Overview

KoeLink is a modular Python application that converts Japanese presentation videos/audio into English audio translations with corresponding scripts. It features a user-friendly command-line interface with progress tracking and can be run both locally and on Google Colaboratory.

## Features

- **Japanese Speech Recognition**: Automatic transcription using SpeechFlow API
- **Text Correction**: Japanese text refinement using OpenAI's ChatGPT
- **Translation**: High-quality Japanese to English translation using DeepL
- **Speech Synthesis**: Natural English audio generation using Genny (Lovo AI)
- **Audio Segmentation**: Automatic splitting of long audio (approximately 20-minute segments)
- **Progress Tracking**: Real-time progress indicators with step-by-step feedback
- **Error Handling**: Comprehensive error handling and validation

## Usage

### 🏠 Local Environment (Recommended)

1. **Environment Setup**
   ```bash
   # Install required libraries
   pip install -r requirements.txt
   ```

2. **API Configuration**
   Create a `.env` file in the project root directory and add the following information:
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

3. **Execution**
   ```bash
   # Run in terminal/command prompt
   python main.py
   ```

4. **File Input**
   When executed, you'll be prompted to enter the path to the Japanese video/audio file you want to translate:
   - Local file path: `C:\Users\username\video.mp4`
   - URL: `https://example.com/video.mp4`

5. **Output Verification**
   After processing, the following files will be generated in the `output` folder:
   - Japanese text (complete version)
   - English text (segmented version)
   - English audio files (segmented version)

### ☁️ Google Colaboratory Execution

1. **File Upload**
   Upload the entire project files to Google Drive.

2. **Run in Colab**
   ```python
   # Execute all cells in main.ipynb sequentially
   ```

3. **File Input**
   Enter the path to files uploaded to Google Drive.

4. **Output Verification**
   After processing, results will be output to the `output` folder.

## Supported File Formats

- **Audio Files**: MP3, WAV, M4A, etc.
- **Video Files**: MP4, AVI, MOV, etc.

## Important Notes

### 📁 File Handling
- **Local Environment**: Local file paths can be specified directly
- **Google Colab**: Use paths to files uploaded to Google Drive
- **Remote Files**: Direct access URLs are also supported (e.g., GitHub RAW file links)

### 🎵 Audio Segmentation
- English audio is automatically segmented into approximately 20-minute chunks (considering listener attention span)
- English text and audio file sequence numbers are matched

### 🔧 Technical Considerations
- Uses external APIs such as OpenAI API, so updates may be required due to specification changes
- Store confidential information in `.env` file and avoid committing to Git

### 💡 Troubleshooting
- Report bugs via issues
- Processing may take a long time (depends on audio length)
- Direct YouTube video URLs are not supported

## Project Structure

```
KoeLink/
├── main.py                 # Main application entry point
├── main.ipynb             # Jupyter notebook version for Google Colab
├── requirements.txt       # Python dependencies
├── .env                   # API credentials (create this file)
├── config/
│   ├── __init__.py
│   └── settings.py        # Configuration management
├── modules/
│   ├── __init__.py
│   ├── speechflow_transcription.py  # SpeechFlow integration
│   ├── chatgpt_text_correction.py   # ChatGPT text refinement
│   ├── deepl_translation.py         # DeepL translation
│   └── genny_synthesis.py           # Genny speech synthesis
├── utils/
│   ├── __init__.py
│   └── file_utils.py      # File handling utilities
├── data/
│   ├── context.txt        # ChatGPT context information
│   └── prompt_fix_jp.txt  # Japanese text correction prompt
└── output/                # Generated output files

```

## Processing Flow

```
Japanese Audio/Video → Speech Recognition → Text Correction → English Translation → English Speech Synthesis → Output
         ↓                    ↓                   ↓                ↓                      ↓
    Input File          SpeechFlow           ChatGPT            DeepL                 Genny
```

## API Services Used

- [SpeechFlow](https://docs.speechflow.io/): Professional speech-to-text API service for accurate transcription
- [OpenAI](https://platform.openai.com/docs/api-reference): AI models including GPT-4 for text generation and refinement
- [DeepL](https://www.deepl.com/docs-api): Industry-leading translation API with high accuracy
- [Genny (Lovo AI)](https://docs.genny.lovo.ai/): Advanced text-to-speech synthesis with natural voices

Each service provides specific functionalities:
- **SpeechFlow**: Converts Japanese audio to text with high accuracy
- **OpenAI ChatGPT**: Corrects and refines transcribed Japanese text
- **DeepL**: Provides professional-grade Japanese to English translation
- **Genny**: Generates natural-sounding English speech from text

## Requirements

### System Requirements
- Python 3.8 or higher (3.13 compatible)
- For audio processing: ffmpeg (automatically handled by pydub)

### Python Dependencies
Install all required packages:
```bash
pip install -r requirements.txt
```

Required packages:
- `python-dotenv`: Environment variable management
- `requests`: HTTP requests for API communication
- `pydub`: Audio file manipulation
- `openai`: OpenAI API client
- `deepl`: DeepL translation API client
- `pytz`: Timezone handling
- `audioop-lts`: Audio operations (for Python 3.13+)

### API Keys
You need to obtain API keys from the following services:
1. **SpeechFlow**: [Sign up here](https://speechflow.io/)
2. **OpenAI**: [Get API key](https://platform.openai.com/api-keys)
3. **DeepL**: [Create account](https://www.deepl.com/pro-api)
4. **Genny (Lovo AI)**: [Get started](https://genny.lovo.ai/)

### Configuration Files
1. Create `data/context.txt` with ChatGPT context instructions
2. Create `data/prompt_fix_jp.txt` with Japanese correction prompt template
3. Ensure `output/` directory exists (created automatically)

## License

Please check the terms of service for each API service before use.

---

<div align="center">

🌏 **Language / 言語選択** 🌏

[English](README.md) | [日本語](README_ja.md)

</div>