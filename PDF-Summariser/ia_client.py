from openai import OpenAI
from tkinter import messagebox
import tkinter as tk
#https://platform.openai.com/docs/api-reference/introduction
#https://platform.openai.com/docs/overview
#https://github.com/openai/openai-python
#https://ollama.com/

class IAClient:
    def __init__(self, api_key, ia_model, base_url, language, document):
        self.api_key = api_key
        self.ia_model = ia_model
        self.base_url = base_url
        self.language = language
        self.document = document

    def get_ai_client(self):
        print(f"The model used is : {self.ia_model} and the url is : {self.base_url}")
    def create_bot(self):
        """Initialize the client with the API infromation."""
        try:
            client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key
            )
            return client
        except Exception as e:
            raise ValueError(f"Erreur lors de l'initialisation du client OpenAI : {e}")
    
    def parameter_prompt(self, number_max_word):
        try:
            if number_max_word > 0:
                number_word = f" in maximum {number_max_word} words "
            else:
                number_word=""
            prompt=[     
                        # With the system role, it works way much better with the online models (I don't know why)
                        {"role": "system", "content": f"""You are a bot with 2 main tasks. The primary is to receive texts summarize and translate texts. 
                                                        These summaries should help you understand the text. You receive texts that were previously in PDF files,
                                                        but have now been converted into text files. So the user might talk about document or file. 
                                                        If there are chapters, you don't have to name them one by one,
                                                        but summarize the whole text. You must not give your opinion or interpret in your own way.
                                                        You have to start your sentence by "Here is a word summary in {number_word} words : " in {self.language}.
                                                        Your summarize must absolutly be in {self.language.upper()}. 
                                                        You must not exceed the word count. Do not write more than {number_word}.
                                                        Your secondary task is to be a chatbot and you have to answer in {self.language.upper()}
                                                        Here is the pdf file {self.document}""" },
                        # With the user role, it works way much better with some locals models (I don't know why)
                        # But it should be deleted for performance reasons. I left it in the base code though.
                        {"role": "user", "content": f"""Summarize the following text (the pdf file) in maximum {number_word} words and translate 
                                                        it in {self.language} :\n{self.document}.
                                                        Please summarize this text in {self.language.upper()} and in maximum {number_word}.""" }
                        # Note : AI have better answers when it is asked in english simply because they are coded in english 
            ]
            return prompt
        except Exception as e:
            ValueError(f"Erreur de l'initianlisation du prompt : {e}")

    def generate_summary(self, client, ia_model, prompt, text_box):
        stream = client.chat.completions.create(
                    model=ia_model,
                    messages=prompt,
                    temperature=0,
                    #max_tokens=1000,
                    stream=True,
        )
        summary = ''
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                text_part = chunk.choices[0].delta.content
                # Add text into the textbox
                text_box.insert(tk.END, text_part)
                text_box.yview("end")
                # Refresh the textbox 
                text_box.update()
                summary += text_part
                
        if not summary:
            messagebox.showerror("Error", "L'application n'a pas pu traiter de document.")
            return None
        else:
           return summary