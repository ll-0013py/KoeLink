#!/usr/bin/env python3
"""
KoeLink - Main Application
Converts Japanese audio/video to English audio with scripts
"""

import sys
import os
from datetime import datetime
import pytz

# Fix encoding issues on Windows
if sys.platform == "win32":
    import locale
    # Set UTF-8 mode for Windows console
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from config.settings import Settings
from modules.speechflow_transcription import SpeechFlowTranscriber
from modules.chatgpt_text_correction import ChatGPTTextCorrector
from modules.deepl_translation import DeepLTranslator
from modules.genny_synthesis import GennySynthesizer
from utils.file_utils import (
    get_media_file_path, 
    save_japanese_script, 
    get_timestamp, 
    print_completion_summary
)


class KoeLink:
    def __init__(self, env_path=".env"):
        """Initialize the KoeLink application"""
        self.settings = Settings(env_path)
        self.timestamp = get_timestamp()
        
        # Initialize service components
        self.transcriber = None
        self.corrector = None
        self.translator = None
        self.synthesizer = None
        
        print("KoeLink initialized")

    def setup_services(self):
        """Setup all service components"""
        try:
            # Validate configuration
            self.settings.validate_api_keys()
            self.settings.validate_files()
            self.settings.print_config_summary()
            
            # Initialize services
            speechflow_config = self.settings.get_speechflow_config()
            self.transcriber = SpeechFlowTranscriber(
                speechflow_config["api_key_id"],
                speechflow_config["api_key_secret"]
            )
            
            chatgpt_config = self.settings.get_chatgpt_config()
            self.corrector = ChatGPTTextCorrector(chatgpt_config["api_key"])
            
            deepl_config = self.settings.get_deepl_config()
            self.translator = DeepLTranslator(deepl_config["auth_key"])
            
            genny_config = self.settings.get_genny_config()
            self.synthesizer = GennySynthesizer(
                genny_config["api_url"],
                genny_config["api_key"],
                genny_config["speaker"],
                genny_config["speaker_style"],
                genny_config["output_dir"]
            )
            
            print("All services initialized successfully")
            return True
            
        except Exception as e:
            print(f"Error setting up services: {e}")
            return False

    def process_audio(self, file_path):
        """Process audio file through the complete pipeline"""
        try:
            print(f"\n{'='*50}")
            print("Starting KoeLink processing...")
            print(f"Input file: {file_path}")
            print(f"Timestamp: {self.timestamp}")
            print(f"{'='*50}")
            
            # Step 1: Transcribe Japanese audio
            print("\n🎤 Step 1: Transcribing Japanese audio...")
            original_jp_text = self.transcriber.transcribe(file_path)
            
            if not original_jp_text:
                print("❌ Transcription failed. Aborting process.")
                return False
            
            print(f"✅ Transcription completed. Length: {len(original_jp_text)} characters")
            
            # Step 2: Correct Japanese text
            print("\n🔧 Step 2: Correcting Japanese text...")
            chatgpt_config = self.settings.get_chatgpt_config()
            corrected_jp_text = self.corrector.correct_text(
                original_jp_text,
                chatgpt_config["context_path"],
                chatgpt_config["prompt_path"]
            )
            
            if not corrected_jp_text:
                print("❌ Text correction failed. Aborting process.")
                return False
            
            print(f"✅ Text correction completed. Length: {len(corrected_jp_text)} characters")
            
            # Save Japanese script
            save_japanese_script(corrected_jp_text, self.settings.output_dir, self.timestamp)
            
            # Step 3: Translate to English
            print("\n🌐 Step 3: Translating to English...")
            english_text = self.translator.translate(corrected_jp_text)
            
            if not english_text:
                print("❌ Translation failed. Aborting process.")
                return False
            
            print(f"✅ Translation completed. Length: {len(english_text)} characters")
            
            # Step 4: Generate English speech
            print("\n🔊 Step 4: Generating English speech...")
            self.synthesizer.synthesize(english_text, self.timestamp)
            
            print("✅ Speech synthesis completed")
            
            # Show completion summary
            print_completion_summary(self.settings.output_dir)
            
            return True
            
        except Exception as e:
            print(f"❌ Error during processing: {e}")
            return False

    def run(self):
        """Main application entry point"""
        print("🎯 Welcome to KoeLink!")
        print("This application converts Japanese audio/video to English audio with scripts.")
        print()
        
        # Setup services
        if not self.setup_services():
            print("❌ Failed to initialize services. Please check your configuration.")
            return False
        
        try:
            # Get input file
            file_path = get_media_file_path()
            
            # Process the file
            success = self.process_audio(file_path)
            
            if success:
                print("\n🎉 Processing completed successfully!")
                print(f"📁 Check the output directory: {self.settings.output_dir}")
                print("\n💡 To process another file, run the program again.")
            else:
                print("\n❌ Processing failed. Please check the error messages above.")
                
            return success
            
        except KeyboardInterrupt:
            print("\n\n👋 Process interrupted by user. Goodbye!")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            return False


def main():
    """Main function"""
    # Check for custom .env path
    env_path = sys.argv[1] if len(sys.argv) > 1 else ".env"
    
    # Create and run the application
    app = KoeLink(env_path)
    success = app.run()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()