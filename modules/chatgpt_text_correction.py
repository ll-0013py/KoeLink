"""
ChatGPT text correction module for VoiceTranslateFlow
"""

from openai import OpenAI


class ChatGPTTextCorrector:
    def __init__(self, api_key, model="gpt-4o", max_tokens=800, max_requests=40):
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.max_requests = max_requests
        self.client = OpenAI(api_key=api_key)

    def load_context(self, context_path):
        """Load context from file"""
        try:
            with open(context_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Context file not found: {context_path}")
            return ""

    def load_prompt(self, prompt_path, script_text):
        """Load and format prompt with script text"""
        try:
            with open(prompt_path, 'r', encoding='utf-8') as file:
                prompt_template = file.read()
            return prompt_template.format(script_var=script_text)
        except FileNotFoundError:
            print(f"Prompt file not found: {prompt_path}")
            return f"Please correct the following Japanese text: {script_text}"

    def correct_text(self, text, context_path, prompt_path):
        """Correct Japanese text using ChatGPT"""
        print("\n[ChatGPT text correction started]")
        
        context = self.load_context(context_path)
        prompt = self.load_prompt(prompt_path, text)
        
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
        
        complete_response = ""
        request_count = 0
        
        try:
            while request_count < self.max_requests:
                request_count += 1
                print(f"\n[Request {request_count}] Sending API request...")
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.3,
                    max_tokens=self.max_tokens
                )
                
                content = response.choices[0].message.content
                complete_response += content
                
                print(f"[Request {request_count}] Received {len(content)} tokens.")
                print(f"[Total tokens so far] {len(complete_response)} tokens collected.")
                
                # Check if response is complete
                if len(content) < self.max_tokens * 0.8:
                    print(f"[Completed] Full response generated with {len(complete_response)} tokens.")
                    break
                
                # Add the latest response to message history
                messages.append({"role": "assistant", "content": content})
                print(f"[Request {request_count}] Continuing to request additional content...")
            
            if request_count >= self.max_requests:
                print("[Warning] Maximum request count reached, response may be incomplete.")
            
            return complete_response
            
        except Exception as e:
            print(f"Error in ChatGPT text correction: {str(e)}")
            return None