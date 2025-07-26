# KoeLink

<div align="center">

🌏 **Language / 言語選択** 🌏

[English](README.md) | [日本語](README_ja.md)

</div>

A tool that translates Japanese audio/video to English audio and generates corresponding scripts.

*KoeLink* (声Link) bridges language barriers, enabling seamless communication regardless of linguistic proficiency.

## Overview

This system can convert Japanese presentation videos/audio into English audio translation with corresponding scripts. It can also be run on Google Colaboratory.

## Features

- **Japanese Speech Recognition**: Automatic transcription using SpeechFlow
- **Text Correction**: Japanese text refinement using ChatGPT
- **Translation**: High-quality Japanese to English translation using DeepL
- **Speech Synthesis**: English audio generation using Genny
- **Audio Segmentation**: Automatic splitting of long audio (approximately 20-minute segments)

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

## Processing Flow

```
Japanese Audio/Video → Speech Recognition → Text Correction → English Translation → English Speech Synthesis → Output
         ↓                    ↓                   ↓                ↓                      ↓
    Input File          SpeechFlow           ChatGPT            DeepL                 Genny
```

## API Services Used

- [SpeechFlow](https://docs.speechmatics.com/flow/flow-api-ref): Real-time speech-to-text API service with live audio streaming capabilities
- [OpenAI](https://platform.openai.com/docs/api-reference): Provides various AI models including GPT for text generation and analysis
- [DeepL](https://github.com/DeepLcom/deepl-python): High-quality language translation API with support for multiple languages
- [Genny](https://github.com/cheekybits/genny): Text-to-speech synthesis service

Each service provides specific functionalities:
- **SpeechFlow**: Handles real-time audio transcription and processing
- **OpenAI**: Offers advanced language models and AI capabilities for text refinement
- **DeepL**: Provides professional-grade translation services
- **Genny**: Facilitates high-quality speech synthesis

## Requirements

Before using this program, you need to:
1. Install the libraries described in `requirements.txt`
2. Set up API keys for all required services
3. Create a `.env` file with your API credentials

If you're running `main.py` in your local environment, the program will automatically load settings from the `.env` file.
If you're using Google Colaboratory with `main.ipynb`, please change the following variables to suit your environment:

- `env_path`
- `context_path`
- `prompt_fix_jp_path` (optional)
- `output_dir`

## License

Please check the terms of service for each API service before use.

---

<div align="center">

🌏 **Language / 言語選択** 🌏

[English](README.md) | [日本語](README_ja.md)

</div>