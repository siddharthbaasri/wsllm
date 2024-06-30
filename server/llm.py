import os
from groq import Groq
from prompt import system_message, user_message


class Groq_llm():
    def __init__(self):
        self.model = "llama3-8b-8192"        
        self.client = Groq(
            api_key = os.getenv('GROQ_API_KEY'),
        )
    
    def getFinalAnswer(self, userQuestion, search_results):
        stream = self.client.chat.completions.create(
            messages = [
                {
                    "role": "system", 
                    "content": system_message
                },
                {
                    "role": "user", 
                    "content": user_message.format(formatted_results = search_results, user_query = userQuestion)
                },
            ],             
            model= self.model,
            stream = False,
            # frequency_penalty=0.5,
            #temperature=0.2
        )
        return stream.choices[0].message.content
