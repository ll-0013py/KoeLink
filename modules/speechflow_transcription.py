"""
SpeechFlow transcription module for VoiceTranslateFlow
"""

import json
import time
import requests


class SpeechFlowTranscriber:
    def __init__(self, api_key_id, api_key_secret, lang="ja", result_type=1):
        self.api_key_id = api_key_id
        self.api_key_secret = api_key_secret
        self.lang = lang
        self.result_type = result_type
        self.headers = {
            "keyId": self.api_key_id,
            "keySecret": self.api_key_secret
        }
        self.query_result = None

    def create_task(self, file_path):
        """Create a transcription task"""
        create_data = {"lang": self.lang}
        create_url = "https://api.speechflow.io/asr/file/v1/create"
        
        if file_path.startswith('http'):
            create_data['remotePath'] = file_path
            print('Submitting a remote file')
            response = requests.post(create_url, data=create_data, headers=self.headers)
        else:
            print('Submitting a local file')
            create_url += f"?lang={self.lang}"
            with open(file_path, "rb") as file:
                files = {'file': file}
                response = requests.post(create_url, headers=self.headers, files=files)
        
        if response.status_code == 200:
            create_result = response.json()
            print(create_result)
            if create_result["code"] == 10000:
                return create_result["taskId"]
            else:
                print("Create error:", create_result["msg"])
                return None
        else:
            print('Create request failed:', response.status_code)
            return None

    def query_task(self, task_id):
        """Query transcription result"""
        query_url = f"https://api.speechflow.io/asr/file/v1/query?taskId={task_id}&resultType={self.result_type}"
        print('Querying transcription result')
        
        while True:
            response = requests.get(query_url, headers=self.headers)
            if response.status_code == 200:
                self.query_result = response.json()
                if self.query_result["code"] == 11000:
                    print('Transcription completed')
                    return self.query_result
                elif self.query_result["code"] == 11001:
                    print('Waiting for transcription...')
                    time.sleep(5)
                    continue
                else:
                    print("Transcription error:", self.query_result['msg'])
                    return None
            else:
                print('Query request failed:', response.status_code)
                return None

    def extract_text(self, result):
        """Extract text from transcription result"""
        if not result or 'result' not in result:
            return ""
        
        try:
            sentences = json.loads(result['result'])['sentences']
            transcription_texts = [sentence['s'] for sentence in sentences]
            return ' '.join(transcription_texts)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error extracting text: {e}")
            return ""

    def transcribe(self, file_path):
        """Complete transcription process"""
        print("\n[Transcription started]")
        
        task_id = self.create_task(file_path)
        if not task_id:
            return None
        
        result = self.query_task(task_id)
        if not result:
            return None
        
        text = self.extract_text(result)
        print(f"Transcription completed. Text length: {len(text)} characters")
        return text