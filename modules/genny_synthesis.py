"""
Genny text-to-speech synthesis module for VoiceTranslateFlow
"""

import os
import time
from io import BytesIO
from datetime import datetime
import requests
from pydub import AudioSegment


class GennySynthesizer:
    def __init__(self, api_url, api_key, speaker, speaker_style, output_dir="./output"):
        self.api_url = api_url
        self.api_key = api_key
        self.speaker = speaker
        self.speaker_style = speaker_style
        self.output_dir = output_dir
        self.headers = {
            'Accept': 'application/json',
            'X-Api-Key': api_key,
            'Content-Type': 'application/json'
        }

    def split_text(self, text, max_length=500):
        """Split text into chunks within the specified maximum length"""
        chunks = []
        current_chunk = ""
        
        for sentence in text.split(". "):
            if len(current_chunk) + len(sentence) + 1 <= max_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks

    def synthesize_chunk(self, text_chunk, chunk_index, total_chunks):
        """Convert a text chunk to audio using the synthesis API"""
        data = {
            'text': text_chunk,
            'speaker': self.speaker,
            'speakerStyle': self.speaker_style,
            'speed': 1.0
        }
        
        print(f"[{chunk_index + 1}/{total_chunks}] Synthesizing chunk...")
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=data)
            
            if response.status_code in [200, 201]:
                response_json = response.json()
                
                if "data" in response_json and response_json["data"] and "urls" in response_json["data"][0]:
                    audio_url = response_json["data"][0]["urls"][0]
                    audio_response = requests.get(audio_url)
                    
                    if audio_response.status_code == 200:
                        print(f"[{chunk_index + 1}/{total_chunks}] Chunk synthesis succeeded.")
                        return AudioSegment.from_file(BytesIO(audio_response.content), format="wav")
                    else:
                        print(f"[{chunk_index + 1}/{total_chunks}] Failed to download audio. Status code: {audio_response.status_code}")
                        return None
                else:
                    print(f"[{chunk_index + 1}/{total_chunks}] Audio URL not found in response.")
                    return None
            else:
                print(f"[{chunk_index + 1}/{total_chunks}] Failed to synthesize text. Status code: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"[{chunk_index + 1}/{total_chunks}] Error in synthesis: {str(e)}")
            return None

    def concatenate_audios(self, audio_segments):
        """Concatenate multiple audio segments into one"""
        combined_audio = AudioSegment.empty()
        for segment in audio_segments:
            if segment:
                combined_audio += segment
        return combined_audio

    def save_audio(self, audio, filename):
        """Save audio file to output directory"""
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)
        audio.export(filepath, format="wav")
        print(f"Audio file saved as {filepath}")

    def save_script(self, script, filename):
        """Save script text to output directory"""
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(script)
        print(f"Script file saved as {filepath}")

    def synthesize(self, text, timestamp=None):
        """Main synthesis function"""
        print("\n[Text-to-speech process started]")
        
        if not text:
            print("No text to synthesize")
            return
        
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        text_chunks = self.split_text(text)
        total_chunks = len(text_chunks)
        audio_segments = []
        script_content_en = ""
        file_index = 1
        
        for i, chunk in enumerate(text_chunks):
            print(f"Processing chunk {i + 1} of {total_chunks}")
            
            audio_segment = self.synthesize_chunk(chunk, i, total_chunks)
            if audio_segment:
                audio_segments.append(audio_segment)
                script_content_en += f"{chunk}\n\n"
            else:
                print(f"Skipping chunk {i + 1} due to synthesis failure.")
            
            # Save files every 80 chunks or at the end
            if (i + 1) % 80 == 0 or (i + 1) == total_chunks:
                if audio_segments:
                    combined_audio_en = self.concatenate_audios(audio_segments)
                    audio_filename = f"en_audio{file_index}_{timestamp}.wav"
                    self.save_audio(combined_audio_en, audio_filename)
                    audio_segments = []
                
                if script_content_en:
                    script_filename_en = f"en_script{file_index}_{timestamp}.txt"
                    self.save_script(script_content_en, script_filename_en)
                    script_content_en = ""
                
                file_index += 1
                time.sleep(3)  # Wait before the next batch
        
        print("Text-to-speech synthesis completed!")