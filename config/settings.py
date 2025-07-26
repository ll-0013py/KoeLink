"""
Settings and configuration management for VoiceTranslateFlow
"""

import os
from dotenv import load_dotenv


class Settings:
    def __init__(self, env_path=".env"):
        """Initialize settings by loading environment variables"""
        self.env_path = env_path
        self.load_environment()
        self.load_api_keys()
        self.set_default_paths()

    def load_environment(self):
        """Load environment variables from .env file"""
        if os.path.exists(self.env_path):
            load_dotenv(self.env_path)
            print(f"Environment variables loaded from {self.env_path}")
        else:
            print(f"Warning: .env file not found at {self.env_path}")

    def load_api_keys(self):
        """Load API keys from environment variables"""
        self.speechflow_api_key_id = os.getenv("SPEECHFLOW_API_KEY_ID")
        self.speechflow_api_key_secret = os.getenv("SPEECHFLOW_API_KEY_SECRET")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.genny_api_url = os.getenv("GENNY_API_URL")
        self.genny_api_key = os.getenv("GENNY_API_KEY")
        self.genny_speaker = os.getenv("GENNY_SPEAKER")
        self.genny_speaker_style = os.getenv("GENNY_SPEAKER_STYLE")
        self.deepl_auth_key = os.getenv("DEEPL_AUTH_KEY")

    def set_default_paths(self):
        """Set default file paths"""
        self.context_path = os.getenv("CONTEXT_PATH", "./data/context.txt")
        self.prompt_fix_jp_path = os.getenv("PROMPT_FIX_JP_PATH", "./data/prompt_fix_jp.txt")
        self.output_dir = os.getenv("OUTPUT_DIR", "./output")

    def validate_api_keys(self):
        """Validate that all required API keys are present"""
        required_keys = {
            "SpeechFlow API Key ID": self.speechflow_api_key_id,
            "SpeechFlow API Key Secret": self.speechflow_api_key_secret,
            "OpenAI API Key": self.openai_api_key,
            "Genny API URL": self.genny_api_url,
            "Genny API Key": self.genny_api_key,
            "Genny Speaker": self.genny_speaker,
            "Genny Speaker Style": self.genny_speaker_style,
            "DeepL Auth Key": self.deepl_auth_key,
        }
        
        missing_keys = []
        for key_name, key_value in required_keys.items():
            if not key_value:
                missing_keys.append(key_name)
        
        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")
        
        return True

    def validate_files(self):
        """Validate that required files exist"""
        required_files = [
            self.context_path,
            self.prompt_fix_jp_path,
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            raise FileNotFoundError(f"Missing required files: {', '.join(missing_files)}")
        
        return True

    def get_speechflow_config(self):
        """Get SpeechFlow configuration"""
        return {
            "api_key_id": self.speechflow_api_key_id,
            "api_key_secret": self.speechflow_api_key_secret,
        }

    def get_chatgpt_config(self):
        """Get ChatGPT configuration"""
        return {
            "api_key": self.openai_api_key,
            "context_path": self.context_path,
            "prompt_path": self.prompt_fix_jp_path,
        }

    def get_deepl_config(self):
        """Get DeepL configuration"""
        return {
            "auth_key": self.deepl_auth_key,
        }

    def get_genny_config(self):
        """Get Genny configuration"""
        return {
            "api_url": self.genny_api_url,
            "api_key": self.genny_api_key,
            "speaker": self.genny_speaker,
            "speaker_style": self.genny_speaker_style,
            "output_dir": self.output_dir,
        }

    def print_config_summary(self):
        """Print configuration summary (without sensitive information)"""
        print("\n=== Configuration Summary ===")
        print(f"Context file: {self.context_path}")
        print(f"Prompt file: {self.prompt_fix_jp_path}")
        print(f"Output directory: {self.output_dir}")
        print(f"SpeechFlow API: {'✓' if self.speechflow_api_key_id else '✗'}")
        print(f"OpenAI API: {'✓' if self.openai_api_key else '✗'}")
        print(f"Genny API: {'✓' if self.genny_api_key else '✗'}")
        print(f"DeepL API: {'✓' if self.deepl_auth_key else '✗'}")
        print("==============================\n")