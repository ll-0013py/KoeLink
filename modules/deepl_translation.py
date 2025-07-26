"""
DeepL translation module for VoiceTranslateFlow
"""

import deepl


class DeepLTranslator:
    def __init__(self, auth_key, target_lang="EN-US", max_chunk_size=50000):
        self.auth_key = auth_key
        self.target_lang = target_lang
        self.max_chunk_size = max_chunk_size
        self.translator = deepl.Translator(auth_key)

    def split_text(self, text):
        """Split text into chunks for translation"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + self.max_chunk_size, len(text))
            
            # Adjust end to the last period (。) within the chunk, if possible
            if end < len(text) and "。" in text[start:end]:
                end = text.rfind("。", start, end) + 1
            elif end == len(text):
                end = len(text)
            
            chunks.append(text[start:end])
            start = end
        
        return chunks

    def translate(self, text):
        """Translate Japanese text to English"""
        print("\n[Translation started]")
        
        if not text:
            print("No text to translate")
            return ""
        
        chunks = self.split_text(text)
        translated_texts = []
        translated_chars = 0
        
        try:
            for chunk in chunks:
                if chunk.strip():  # Skip empty chunks
                    result = self.translator.translate_text(chunk, target_lang=self.target_lang)
                    translated_texts.append(result.text)
                    
                    translated_chars += len(chunk)
                    print(f"Translated {translated_chars} / {len(text)} characters")
                else:
                    translated_texts.append("")
            
            final_translation = ''.join(translated_texts)
            print(f"Translation completed. Output length: {len(final_translation)} characters")
            return final_translation
            
        except Exception as e:
            print(f"Error in translation: {str(e)}")
            return None